import cv2
import numpy as np
import pytesseract

# 配置 pytesseract 路径 (WINDOWS需要)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# 读取图像
image_path = 'test9.png'  # 替换为你的图像路径
image = cv2.imread(image_path)

# 转换为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

h, w = gray.shape
roi = gray[int(0.21*h):int(0.79*h), int(0.34*w):int(0.66*w)]

# 显示 ROI 以便检查
cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 使用 pytesseract 识别数字
#custom_config = r'--oem 3 --psm 7 outputbase digits'
custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789'
recognized_text = pytesseract.image_to_string(roi, config=custom_config)

print("OCR Number:", recognized_text.strip())
