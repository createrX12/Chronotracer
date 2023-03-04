# coding=utf-8
"""
@author B1lli
@date 2023年01月26日 22:06:57
@File:screenshot.py
"""
import subprocess
import datetime
import os
import time
from modules.ocr.paddle_ocr import *
from modules.utils.multiprocesser import *

@background_thread
def screenshot(path = r'F:\ComputerLifeRecoder\screenshots',interval = 2) :
    ori_path = path
    if not os.path.exists ( ori_path ) :
        os.mkdir ( ori_path )
    pdocr_module = Pdocr()
    seq = 0

    while True:
        seq+=1
        start_time = time.time ()
        #获取当前日期时间
        now = datetime.datetime.now ()
        date = now.strftime ( "%Y-%m-%d" )
        folder_path = os.path.join(path,date)
        if not os.path.exists ( folder_path ) :
            os.mkdir ( folder_path )
        path = os.path.join ( ori_path, date )
        date_time = now.strftime ( "%Y-%m-%d_%H-%M-%S" )

        #给每个屏幕截图并存储到电脑里
        filename = f"{path}/{date_time}.png"
        subprocess.call ( ["ffmpeg", "-f", "gdigrab", "-framerate", "2", "-i", "desktop", "-vframes", "1", filename] )

        #获取截图分辨率
        p = subprocess.Popen (
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of",
             "csv=s=x:p=0", filename], stdout=subprocess.PIPE )

        out, err = p.communicate ()
        resolution = out.decode ( "utf-8" ).strip ()
        path_newname = f"{path}/{date_time}_{resolution}.png"
        os.rename ( filename, path_newname )
        pdocr_module.realtime_recognize(path_newname,date,resolution,seq)
        while float(time.time () - start_time) < float(interval) :
            time.sleep ( 0.1 )


if __name__ == '__main__':
    screenshot(r'F:\ComputerLifeRecoder\screenshots',2)
