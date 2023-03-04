# coding=utf-8
"""
@author B1lli
@date 2023年01月26日 23:10:47
@File:main.py
"""
import sys
from interface import *
import timeit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CLR_interface()
    ex.show()
    sys.exit(app.exec_())

