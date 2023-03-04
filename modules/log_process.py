# coding=utf-8
"""
@author B1lli
@date 2023年02月02日 23:47:42
@File:log_process.py
"""
# import psutil
# import time
# from db.save_to_sqlite import *
#
# while True :
#     process_list = []
#     for process in psutil.process_iter ( ['pid', 'name'] ) :
#         process_list.append ( process.info )
#     db_dic =  { 'time':round(time.time()), 'process' : process_list }
#     write_to_db('process',db_dic )
#
#     # with open ( 'process_list.txt', 'w' ) as file :
#     #     for process in process_list :
#     #         file.write ( str ( process ) + '\n' )
#
#     time.sleep ( 10 )

import win32gui
import win32process
import time
import psutil
from db.save_to_sqlite import *
from modules.utils.multiprocesser import *



def get_taskbar_process() :
    taskbar_apps = []

    def callback(hwnd, extra) :
        if win32gui.IsWindowVisible ( hwnd ) and win32gui.IsIconic ( hwnd ) == 0 :
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            taskbar_apps.append((hwnd, win32gui.GetWindowText(hwnd), psutil.Process(pid).exe()))
        return True

    win32gui.EnumWindows ( callback, None )
    return taskbar_apps

def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return (hwnd,win32gui.GetWindowText(hwnd), psutil.Process(pid).exe())

@background_thread
def process_monitor():
    '''
    监控任务栏应用与活动窗口，每秒刷新一次
    对于任务栏应用，检查任务栏内任何应用的标题变化，并以此判断应用的开启与关闭，将进程名，id，路径，时间写入taskbar_process表
    对于活动窗口，每秒刷新一次，监测当前活动窗口，将进程名，id，路径，时间写入数据库
    :return:
    '''
    sqlite_conn = Sqlite_interact()
    previous_taskbar_process = get_taskbar_process ()
    previous_active_process = get_active_window()

    while True:
        try:
            current_active_process = get_active_window()
            current_taskbar_process = get_taskbar_process ()
            new_process = [process for process in current_taskbar_process if process not in previous_taskbar_process]
            closed_process = [process for process in previous_taskbar_process if process not in current_taskbar_process]

            if current_active_process != previous_active_process:
                sqlite_conn.write_to_db ( 'active_process', {'process_name' : current_active_process[1], 'process_id' : current_active_process[0],
                                                          'process_path' : current_active_process[2], 'active_start_time' : time.time ()} )

            for process in new_process :
                if process[1] != '':
                    print ( f'[{time.ctime ()}] New process: {process}' )
                    process_id = process[0]
                    process_name = process[1]
                    process_path = process[2]
                    sqlite_conn.write_to_db ( 'taskbar_process', {'process_name':process_name,'process_id':process_id,'process_path':process_path,'start_time':time.time()} )

            for process in closed_process :
                if process[1] != '':
                    print ( f'[{time.ctime ()}] Closed process: {process}' )
                    process_id = process[0]
                    process_name = process[1]
                    process_path = process[2]
                    sqlite_conn.write_to_db ( 'taskbar_process', {'process_name':process_name,'process_id':process_id,'process_path':process_path,'end_time':time.time()} )

            previous_taskbar_process = current_taskbar_process
            previous_active_process = current_active_process
            time.sleep ( 1 )
        except Exception as e:
            print(e)
            time.sleep(2)




if __name__ == '__main__':
    process_monitor()

