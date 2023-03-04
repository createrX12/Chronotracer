# coding=utf-8
"""
@author B1lli
@date 2023年01月26日 18:47:02
@File:paddle_ocr.py
"""
import os
import time
import json
from modules.utils.func_time import *

# import cv2
# import os
# import paddlehub as hub
# @time_it
# def pdocr(path=f'F:\ComputerLifeRecoder\screenshots'):
#     # 待预测图片
#     os.environ['CUDA_VISIBLE_DEVICES'] = '0'
#     ocr = hub.Module ( name="chinese_ocr_db_crnn_server", enable_mkldnn=True )  # mkldnn加速仅在CPU下有效
#     for root, dirs, files in os.walk ( path ) :
#         for file in files:
#             file_path = os.path.join ( root, file )
#             pdocr_rec(file_path,ocr)
#
# def pdocr_rec(file_path,ocr=None):
#     ocr = hub.Module ( name="chinese_ocr_db_crnn_server", enable_mkldnn=True )
#     results = ocr.recognize_text (
#         images=[cv2.imread ( file_path )],  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
#         use_gpu=True,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
#         output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
#         visualization=True,  # 是否将识别结果保存为图片文件；
#         box_thresh=0.5,  # 检测文本框置信度的阈值；
#         text_thresh=0.5 )  # 识别中文文本置信度的阈值；
#
#     for result in results :
#         data = result['data']
#         save_path = result['save_path']
#         for infomation in data :
#             print ( infomation['text'] )
import shutil
from paddleocr import PaddleOCR
from modules.utils.logger import *
from modules.db.save_to_sqlite import *
from modules.pic_to_HEVC import organize_photos

def update_seq_log(date, resolution):
    s = 0
    try:
        # 打开 seq_log.json 文件
        with open('seq_log.json', 'r') as f:
            seq_log = json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，则新建一个空的 seq_log
        seq_log = []

    # 遍历 seq_log，查找符合 date 和 resolution 的行
    found = False
    for item in seq_log:
        if item['date'] == date and item['resolution'] == resolution:
            # 如果找到了，则将 s 赋值为该行的 seq，并将 seq 增加 1
            s = item['seq']
            item['seq'] += 1
            found = True
            break

    if not found:
        # 如果没找到，则添加一行，seq 设为 1
        s = 1
        seq_log.append({'date': date, 'resolution': resolution, 'seq': s})


    # 将 seq_log 写入文件
    with open('seq_log.json', 'w') as f:
        json.dump(seq_log, f, indent=4)

    return s

@log_error
@time_it
class Pdocr( object ):

    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
        self.sqlite_writer = Sqlite_interact()

    def recognize_text(self, photo_path=r"D:\ManicTime_Screenshots\2023-01-25\2023-01-25_22-09-23_08-00_1920_1080_18130_0.jpg"):
        # 多语言语种可以通过修改lang参数进行切换
        # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
        result = self.ocr.ocr( photo_path, cls=True )
        return result[0] # 单次只识别一张，如果识别多张请去掉这个[0]
        # for line in result:
        #     for box in line:
        #         print(box)
        #         print('_________________')
        #         print(box[1][0])

    def save_photo_to_sqlite(self,result,photo_path,pic_seq=None):
        for box in result :
            pic_text = box[1][0]
            pic_ctime = os.path.getctime ( photo_path )
            pic_box = box[0]
            data_confidence = box[1][1]
            pic_date = dir[:10]
            pic_resolution = dir[-9 :]
            pic_recognized_time = int ( round ( time.time () ) )
            self.sqlite_writer.write_to_db ( 'pic_data',
                                             {'pic_text' : pic_text, 'pic_ctime' : pic_ctime, 'pic_box' : pic_box,
                                              'data_confidence' : data_confidence, 'pic_seq' : pic_seq,
                                              'pic_date' : pic_date, 'pic_resolution' : pic_resolution,
                                              'pic_recognized_time' : pic_recognized_time} )

    def batch_recognize(self,path=None) :
        '''
        :param path: 包含分辨率文件夹的路径:
        :return:
        '''
        if not path :
            path = input ( "输入要识别图片所在的文件夹们的路径(如D:\ManicTime_Screenshots\\2023-01-27): " )
        # 检查路径下是否有文件夹，如果没有则整理图片
        if not os.walk ( path, topdown=True ).__next__ ()[1] :
            print ( "无文件夹，调用整理图片进程" )
            organize_photos ( path )
        for root, dirs, files in os.walk ( path, topdown=True ) :
            for dir in dirs :
                images_path = os.path.join ( root, dir )
                for _,_,photos in os.walk(images_path):
                    photos.sort(key=lambda x: int(x.split('.')[0]))
                    for photo in photos:
                        photo_path = os.path.join ( images_path, photo )
                        result = self.recognize_text(photo_path)
                        for box in result:
                            pic_text = box[1][0]
                            pic_ctime = os.path.getctime(photo_path)
                            pic_box = box[0]
                            data_confidence = box[1][1]
                            pic_seq = int(photo[:-4])
                            pic_date = dir[:10]
                            pic_resolution = dir[-9:]
                            pic_recognized_time = int(round(time.time()))
                            self.sqlite_writer.write_to_db('pic_data',{'pic_text':pic_text,'pic_ctime':pic_ctime,'pic_box':pic_box,'data_confidence':data_confidence,'pic_seq':pic_seq,'pic_date':pic_date,'pic_resolution':pic_resolution,'pic_recognized_time':pic_recognized_time})
                        # save_photo_to_sqlite(result)
                        os.remove(photo_path)

    def realtime_recognize(self,photo_path,pic_date,pic_resolution,pic_seq = 0):
        result = self.recognize_text(photo_path)
        for box in result :
            pic_text = box[1][0]
            pic_box = box[0]
            data_confidence = box[1][1]
            pic_ctime = os.path.getctime ( photo_path )
            # pic_date = dir[:10]
            # pic_resolution = dir[-9 :]
            pic_recognized_time = int ( round ( time.time () ) )
            # pic_seq = update_seq_log(pic_date,pic_resolution)
            self.sqlite_writer.write_to_db ( 'pic_data',
                                             {'pic_text' : pic_text, 'pic_ctime' : pic_ctime, 'pic_box' : pic_box,
                                              'data_confidence' : data_confidence, 'pic_seq' : pic_seq,
                                              'pic_date' : pic_date, 'pic_resolution' : pic_resolution,
                                              'pic_recognized_time' : pic_recognized_time} )



if __name__ == '__main__':
    recognizer = Pdocr ()
    for path in [rf'D:\ManicTime_Screenshots\2023-{i}' for i in ['02-24','02-25','02-26','02-27','02-28','03-01']]:
        try:
            recognizer.batch_recognize ( path )
            # time.sleep(7200)
        finally:
            if not os.walk ( path, topdown=True ):
                print(f'{path}文件夹识别完毕，跳过')
                continue
            else:
                recognizer.batch_recognize(path)



