### 使用说明：

环境配置：

~~~python
pip install pytesseract
~~~

```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

```
sudo vi /etc/apt/sources.list

Copy the first line "deb http://archive.ubuntu.com/ubuntu bionic main" and paste it as shown below on the next line.
If you are using a different release of ubuntu, then replace bionic with the respective release name.

deb http://archive.ubuntu.com/ubuntu bionic universe
```

![image-20250324150204789](https://raw.githubusercontent.com/CANLAN-SC/picturesMKD/main/image-20250324150204789.png)

1. **触发与订阅**
   - 通过订阅 `/ocr_trigger` (Bool) 话题控制OCR采集，只有收到True信号后，下一帧图像才进行OCR识别。
   - 通过订阅 `/cmd_open_bridge` (Bool) 话题，在收到桥梁解锁信号（True消息）后，停止采集OCR结果，并统计已收集的数字。
2. **OCR识别**
   - 使用 `pytesseract` 对图像中心的ROI区域进行OCR识别，配置参数 `--psm 10 -c tessedit_char_whitelist=0123456789` 仅识别单个数字。
   - 识别有效后，将数字保存到列表中，并发布到 `/recognized_digit` 话题供调试观察。
3. **统计出现次数最少的数字**
   - 在桥梁解锁回调函数中，通过 `collections.Counter` 对所有识别结果进行统计，
   - 利用 `min(counter, key=counter.get)` 计算出出现次数最少的数字，并发布到 `/mode_digit` 话题。