from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='en') # need to run only once to load model into memory
img_path = 'test9.png'
result = ocr.ocr(img_path, det=False, cls=False)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)