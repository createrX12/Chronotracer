# coding=utf-8
"""
@author B1lli
@date 2023年02月02日 19:06:49
@File:opencv_ocr.py
"""
import cv2
import os
import json
from modules.utils.func_time import *

@time_it
def recognize_text(folder_path=None):
    '''
    识别文件夹内的图片，并将图片的文本信息与图片创建时间放入ocr_results.json
    !本功能尚未开发完成，预期是将图片压缩后所在帧位置和图片文本识别出的对应信息放入文件内
    :param folder_path: 要识别的图片所在文件夹路径
    :return:
    '''
    folder_path = input("输入要识别的图片所在文件夹路径: ")
    results = {}
    use_cuda = False
    try:
        pytesseract.get_tesseract_version()
        pytesseract.get_oem()
        use_cuda = True
        print('目前使用CUDA进行运算')
    except Exception as e:
        print(e)
        print('调用CUDA失败')
        pass
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                image = cv2.imread(file_path)
                if use_cuda:
                    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                    text = pytesseract.image_to_string(image, lang = 'chi_sim+eng+num+symbols', config='--oem 0 --psm 6')
                else:
                    text = pytesseract.image_to_string(image, lang = 'chi_sim+eng+num+symbols')
                create_time = os.path.getctime(file_path)
                results[file_path] = {
                    "create_time":create_time,
                    "text":text
                }
    results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['create_time'])}
    #保存路径
    with open("ocr_results.json", "w") as f:
        json.dump(results, f)