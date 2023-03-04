import os
import shutil
from PIL import Image
from modules.utils.func_time import *
from modules.utils.logger import *
from PyQt5 import QtCore
import subprocess

#用于和interface发送图片处理进度
class Organizer(QtCore.QObject):
    progress_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(Organizer, self).__init__(parent)

organizer = Organizer()

@log_error
@time_it
def organize_photos(path=None) :
    '''
    将图片从文件夹内复制出来
    按照分辨率复制进不同文件夹
    按照时间顺序给图片编号
    :param path: 包含图片的路径:
    :return:
    '''
    #用于跟踪处理进度，并返回给进度条的变量
    total_files = 0
    processed_files = 0
    if not path:
        path = input("输入待整理图片文件夹路径: ")

    if path == 'D:\ManicTime_Screenshots':
        print('不要输入根目录，会删除所有图片')
        return

    resolutions = {}
    #筛选图片文件，仅仅保留非thumbnail（缩略图）的文件
    for root, dirs, files in os.walk ( path ) :
        for file in files :
            file_path = os.path.join ( root, file )
            if 'thumbnail' in file :
                continue
            #识别图片分辨率，并放入对应分辨率的文件夹内
            with Image.open ( file_path ) as img :
                width, height = img.size
                resolution = f"{width}x{height}"
                if resolution not in resolutions :
                    resolutions[resolution] = []
                resolutions[resolution].append ( file_path )


    #创建分辨率文件夹
    resolution_dirs = []
    for resolution, files in resolutions.items () :
        resolution_dir = os.path.join ( path, f"{path[-10:]}_{resolution}" )
        os.makedirs ( resolution_dir, exist_ok=True )
        #移动对应图片到对应文件夹内
        for i, file in enumerate ( sorted ( files, key=lambda x : os.path.getctime ( x ) ) ) :
            new_name = f"{i}.jpg"
            new_path = os.path.join ( resolution_dir, new_name )
            shutil.copy ( file, new_path )
            resolution_dirs.append ( resolution_dir )

            #进度条
            progress = int(i / len(files) * 100)
            organizer.progress_signal.emit(progress)

    organizer.progress_signal.emit( 100 )
    return resolution_dirs

#用于将图片压缩为视频
@log_error
@time_it
def generate_video(path=None) :
    '''
    将各个分辨率文件夹内编号好的图片分别压缩为视频
    如果输入的路径下没有分辨率文件夹，只有图片，则会自动调用organize_photos生成分辨率文件夹
    :param path: 包含分辨率文件夹的路径:
    :return:
    '''
    if not path:
        path = input("输入要整合成视频的图片所在的文件夹们的路径(如D:\ManicTime_Screenshots\\2023-01-27): ")
    # 检查路径下是否有文件夹，如果没有则整理图片
    if not os.walk(path,topdown=True).__next__()[1] :
        print ( "无文件夹，调用整理图片进程" )
        organize_photos (path)
    for root, dirs, files in os.walk ( path ,topdown=True) :
        for dir in dirs :
            video_name = f"{dir}.mp4"
            video_path = os.path.join(os.path.dirname(root), video_name)
            images_path = os.path.join ( root, dir )
            command = f"ffmpeg -y -framerate 30 -i {images_path}/%d.jpg -c:v hevc_nvenc -b:v 10M -y {video_path}"
            process = subprocess.Popen(command, shell=True)
            process.wait()
            shutil.rmtree ( images_path )

if __name__ == '__main__':
    for path in [rf'D:\ManicTime_Screenshots\2023-02-{i}' for i in [f'{i}' for i in range(19,29)]]:
        # print(path)
        generate_video ( path )

