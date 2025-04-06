#!/usr/bin/env python
import rospy
import cv2
import pytesseract
from sensor_msgs.msg import Image
from std_msgs.msg import Int32, Bool
from cv_bridge import CvBridge
from collections import Counter

class PreBridgeOCRNode:
    def __init__(self):
        rospy.init_node("pre_bridge_ocr_node")
        self.bridge = CvBridge()
        self.ocr_results = []
        self.pre_bridge_complete = False
        self.ocr_enabled = False
        
        image_topic = rospy.get_param("~image_topic", "/front/image_raw")
        
        self.image_sub = rospy.Subscriber(image_topic, Image, self.image_callback)
        self.ocr_trigger_sub = rospy.Subscriber("/ocr_trigger", Bool, self.ocr_trigger_callback)
        self.bridge_unlock_sub = rospy.Subscriber("/cmd_open_bridge", Bool, self.bridge_unlock_callback)
        
        self.digit_pub = rospy.Publisher("/recognized_digit", Int32, queue_size=1)
        self.mode_digit_pub = rospy.Publisher("/mode_digit", Int32, queue_size=1)
        self.preprocessed_image_pub = rospy.Publisher("/ocr_preprocessed_image", Image, queue_size=1)
        
        rospy.loginfo("Pre-bridge OCR node started, waiting for OCR triggers and bridge unlock signal.")
    
    def ocr_trigger_callback(self, msg):
        if not self.pre_bridge_complete and msg.data:
            self.ocr_enabled = True
            rospy.loginfo("OCR trigger received, will process next image for OCR.")
    
    def bridge_unlock_callback(self, msg):
        if not self.pre_bridge_complete and msg.data:
            rospy.loginfo("Bridge unlock signal received, calculating min frequency digit.")
            if self.ocr_results:
                counter = Counter(self.ocr_results)
                min_digit = min(counter, key=counter.get)
                rospy.loginfo("Min frequency digit is: %d", min_digit)
                self.mode_digit_pub.publish(min_digit)
            else:
                rospy.logwarn("No OCR results collected, cannot compute min frequency digit.")
            self.pre_bridge_complete = True
    
    def image_callback(self, msg):
        if not self.ocr_enabled or self.pre_bridge_complete:
            return
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            rospy.logerr("CvBridge Error: %s", e)
            return
        
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        h, w = thresh.shape
        roi = thresh[int(0.15*h):int(0.80*h), int(0.10*w):int(0.70*w)]

        roi_image_msg = self.bridge.cv2_to_imgmsg(roi, encoding="mono8")
        self.preprocessed_image_pub.publish(roi_image_msg)

        custom_config = r'--psm 10 -c tessedit_char_whitelist=0123456789'
        ocr_text = pytesseract.image_to_string(roi, config=custom_config).strip()
        
        # 仅识别单个数字（个位数）
        if len(ocr_text) == 1 and ocr_text.isdigit():
            digit = int(ocr_text)
            rospy.loginfo("Recognized single digit: %d", digit)
            self.digit_pub.publish(digit)
            self.ocr_results.append(digit)
        else:
            rospy.loginfo("OCR did not recognize a valid single digit. OCR result: '%s'", ocr_text)
        
        self.ocr_enabled = False

if __name__ == '__main__':
    try:
        node = PreBridgeOCRNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
