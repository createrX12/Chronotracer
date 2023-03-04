# coding=utf-8
"""
@author B1lli
@date 2023年01月28日 11:24:59
@File:interface.py
"""
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QFileDialog)
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from PyQt5 import QtWidgets
from pic_to_HEVC import *
from modules.ocr.paddle_ocr import *
from screenshot import *
from modules.utils.logger import *
from log_process import *
from search import *
global func_lst
# noinspection PyRedeclaration
func_lst = ['organize_photos', 'recognize_text', 'generate_video','screenshot']

class CLR_Thread(QThread):
    signal = pyqtSignal(str)

    def __init__(self,func=None):
        super().__init__()
        self.function = func

    @log_error
    def run(self):
        self.signal.emit ( "进程运行中" )
        self.function()
        self.signal.emit("进程结束")

    def stop(self):
        self.signal.emit ( "进程结束" )
        self.terminate()


class CLR_interface( QMainWindow ):
    def __init__(self):
        super().__init__()
        # 总体对象
        # self.setStyleSheet ( "QPushButton{border: none; background-color: white; color: black;} QPushButton:hover{background-color: #1DC9A0; color: white;} QPushButton:pressed{background-color: #169c86; color: black;}" )
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle("溯时计")
        self.layout = QVBoxLayout()
        self.thread = None
        self.progress_signal = QtCore.pyqtSignal(int)

        # 路径输入框和浏览文件夹
        # self.path_input = QLineEdit()
        # self.path_input.setPlaceholderText("在此输入路径")
        # self.browse_button = QPushButton("浏览")
        # self.browse_button.clicked.connect(self.browse)
        # self.path_layout = QHBoxLayout ()
        # self.path_layout.addWidget ( self.path_input )
        # self.path_layout.addWidget ( self.browse_button )
        # self.layout.addLayout ( self.path_layout )

        self.group_box = QGroupBox()
        self.group_box.setLayout(self.layout)
        self.setCentralWidget(self.group_box)

        # 功能按钮
        # self.organize_photos_button = QPushButton ( "整理图片" )
        # self.organize_photos_button.clicked.connect ( self.organize_photos )
        # self.layout.addWidget ( self.organize_photos_button )
        #
        # self.recognize_text_button = QPushButton ( "文本识别" )
        # # self.recognize_text_button.setEnabled ( False )
        # self.recognize_text_button.clicked.connect ( self.recognize_text )
        # self.layout.addWidget ( self.recognize_text_button )
        #
        # self.generate_video_button = QPushButton ( "将图片压缩为视频" )
        # self.generate_video_button.clicked.connect ( self.generate_video )
        # self.layout.addWidget ( self.generate_video_button )

        self.process_monitor_button = QPushButton ( "进程监控" )
        self.process_monitor_button.clicked.connect ( self.monitor_process )
        self.process_monitor_label = QLabel ( '进程监控停止' )
        self.process_monitor_layout = QHBoxLayout ()
        self.process_monitor_layout.addWidget(self.process_monitor_button)
        self.process_monitor_layout.addWidget ( self.process_monitor_label )
        self.layout.addLayout ( self.process_monitor_layout )

        self.screenshot_button = QPushButton ( "持续屏幕截图" )
        self.screenshot_interval_input = QLineEdit ()
        self.screenshot_interval_input.setPlaceholderText ( "输入截图时间间隔" )
        self.screenshot_path_input = QLineEdit ()
        self.screenshot_path_input.setPlaceholderText("输入截图保存路径")
        self.screenshot_label = QLabel ( '屏幕截图停止' )
        self.screenshot_layout = QHBoxLayout()
        self.screenshot_layout.addWidget (self.screenshot_path_input)
        self.screenshot_layout.addWidget (self.screenshot_interval_input)
        self.screenshot_layout.addWidget (self.screenshot_button)
        self.screenshot_layout.addWidget(self.screenshot_label)
        self.screenshot_button.clicked.connect ( self.screenshot )
        self.layout.addLayout ( self.screenshot_layout )

        self.search_button = QPushButton ( "搜索" )
        self.search_text_input = QLineEdit ()
        self.search_text_input.setPlaceholderText ( "输入搜索文本" )
        self.search_date_input = QLineEdit ()
        self.search_date_input.setPlaceholderText( "输入搜索日期（留空以搜索全部）" )
        self.search_label = QLabel ( '搜索停止' )
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget ( self.search_date_input )
        self.search_layout.addWidget ( self.search_text_input )
        self.search_layout.addWidget ( self.search_button )
        self.search_layout.addWidget( self.search_label )
        self.search_button.clicked.connect ( self.search )
        self.layout.addLayout ( self.search_layout )

        self.stop_button = QPushButton("停止进程")
        self.stop_button.clicked.connect ( self.stop_thread )
        self.layout.addWidget ( self.stop_button )
        self.stop_button.setEnabled ( False )

        # 进度条
        self.progress_bar = QtWidgets.QProgressBar ( self )
        self.layout.addWidget(self.progress_bar)
        organizer.progress_signal.connect ( self.progress_bar.setValue )


        # 状态标签
        self.label = QLabel('')
        self.layout.addWidget ( self.label )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))

        # 画背景
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Draw rounded rectangles for all controls
        for control in self.findChildren((QLineEdit, QPushButton, QLabel)):
            painter.drawRoundedRect(control.geometry(), 10, 10)

    def browse(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.path_input.setText(path)

    def update_label(self, text):
        self.label.setText(text)

    def organize_photos(self) :
        path = self.path_input.text ()
        self.thread = CLR_Thread (lambda : organize_photos(path))
        self.thread.signal.connect ( self.update_label )
        self.thread.start()
        self.stop_button.setEnabled ( True )

    def recognize_text(self) :
        path = self.path_input.text ()
        self.thread = CLR_Thread (lambda : recognize_text(path))
        self.thread.signal.connect ( self.update_label )
        self.thread.start()

    def generate_video(self) :
        path = self.path_input.text ()
        self.thread = CLR_Thread (lambda : generate_video(path))
        self.thread.signal.connect ( self.update_label )
        self.thread.start()
        self.stop_button.setEnabled ( True )

    def monitor_process(self) :
        self.process_monitor_label.setText ( '进程监控正在运行' )
        self.thread = CLR_Thread (process_monitor)
        self.thread.signal.connect ( self.update_label )
        self.thread.start()
        self.stop_button.setEnabled ( True )

    def screenshot(self) :
        self.screenshot_label.setText('屏幕截图正在运行')
        interval = self.screenshot_interval_input.text ()
        path = self.screenshot_path_input.text ()
        self.thread = CLR_Thread (lambda : screenshot(path,interval))
        self.thread.signal.connect ( self.update_label )
        self.thread.start()
        self.stop_button.setEnabled(True)

    def search(self) :
        self.search_label.setText( '搜索正在运行' )
        pic_text = self.search_text_input.text ()
        pic_date = self.search_date_input.text ()
        search_pic ( pic_text, pic_date )
        # self.thread = CLR_Thread (lambda : )
        # self.thread.signal.connect ( self.update_label )
        # self.thread.start()
        # self.stop_button.setEnabled(True)

    def stop_thread(self):
        self.thread.stop()
        self.process_monitor_label.setText ( '进程监控停止' )
        self.search_label.setText( '屏幕截图停止' )
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(100)


if __name__ == '__main__':
    app = QApplication([])
    window = CLR_interface()
    window.show()
    app.exec_()



