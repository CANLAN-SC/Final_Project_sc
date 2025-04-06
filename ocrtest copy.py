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

# 应用阈值处理
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 获取图像尺寸并提取 ROI (感兴趣区域)
h, w = thresh.shape
roi = thresh[int(0.21*h):int(0.79*h), int(0.34*w):int(0.66*w)]
'''
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 1. 高斯模糊去除轻微噪声
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 2. 自适应阈值或 Otsu 阈值
# Otsu 二值化效果更稳妥，因为图像背景非常干净
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 3. 腐蚀 + 膨胀去掉小噪点（可选）
kernel = np.ones((3, 3), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# 4. 裁剪 ROI（你之前的做法可以保留）
h, w = thresh.shape
roi = thresh[int(0.15*h):int(0.80*h), int(0.20*w):int(0.80*w)]
'''
# 显示 ROI 以便检查
cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 使用 pytesseract 识别数字
#custom_config = r'--oem 3 --psm 7 outputbase digits'
custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789'
recognized_text = pytesseract.image_to_string(roi, config=custom_config)

print("OCR Number:", recognized_text.strip())
