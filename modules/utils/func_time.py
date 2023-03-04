# coding=utf-8
"""
@author B1lli
@date 2023年01月26日 23:53:53
@File:func_time.py
"""
import time

def time_it(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f'共耗时约{round(end-start,2)}秒')
        return result
    return wrapper