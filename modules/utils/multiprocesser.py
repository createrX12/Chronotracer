# coding=utf-8
"""
@author B1lli
@date 2023年02月05日 16:48:09
@File:multiprocesser.py
"""



# import queue
#
#
#
# class NewThread(object):
#     # __init__ : 不再接收被装饰函数，而是接收传入参数.
#     # __call__ ：接收被装饰函数，实现装饰逻辑.
#
#     def __init__(self, max_thread=500):
#         self.max_thread = max_thread
#
#     def __call__(self, func):  # 接受函数
#         from functools import wraps
#
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         while True:
#             # 获取已启动此函数线程的数量
#             func_thread_active_count = len([i for i in threading.enumerate() if i.name == func.__name__])
#
#             if func_thread_active_count <= self.max_thread:
#                 # 待执行功能
#                 # func(*args, **kwargs)
#                 thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=func.__name__)
#                 # 把主线程设置为守护线程，主线程执行结束了，就不管子线程是否完成,一并和主线程退出
#                 # thread.setDaemon(True)
#                 thread.start()
#                 # 子线程调用join()方法，使主线程等待子线程运行完毕之后才退出，与thread.setDaemon(True)相反
#                 # thread.join()
#                 break
#             # else:
#             #     time.sleep(0.01)
#         return wrapper  # 返回函数
#
#
# @NewThread.wrapper
# def foo(sleep_time):
#     while True:
#         num = random.randint(1, 100)
#         print ( num )
#         time.sleep(sleep_time)
#
# @NewThread
# def zoo( sleep_time):
#     while True:
#         num = q.get () / 2 + 8
#         time.sleep(sleep_time)
#
#
# if __name__ == '__main__':
#
#     t1 = time.time()
#     foo(1)
#     t2 = time.time()
#     print('运行耗时：' + str(round(t2 - t1, 2)) + ' s')  # 50.19s

# import queue
# import threading
# import time
#
# class CommunicationThread(object):
#     def __init__(self, communication_queue=None, max_thread=500):
#         self.communication_queue = communication_queue or queue.Queue()
#         self.max_thread = max_thread
#
#     def __call__(self, func):
#         from functools import wraps
#
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             while True:
#                 func_thread_active_count = len([i for i in threading.enumerate() if i.name == func.__name__])
#
#                 if func_thread_active_count <= self.max_thread:
#                     def target_func(*args, **kwargs):
#                         result = func(*args, **kwargs)
#                         self.communication_queue.put(result)
#
#                     thread = threading.Thread(target=target_func, args=args, kwargs=kwargs, name=func.__name__)
#                     thread.start()
#                     break
#                 # else:
#                 #     time.sleep(0.01)
#
#         return wrapper
#
# @CommunicationThread(max_thread=3)
# def func1(arg1, arg2):
#     time.sleep(1)
#     return arg1 + arg2
#
# @CommunicationThread(max_thread=3)
# def func2(arg1, arg2):
#     time.sleep(2)
#     return arg1 * arg2
#
#
# if __name__ == '__main__' :
#     for i in range ( 5 ) :
#         func1 ( i, i + 1, queue=queue )
#     for i in range ( 5 ) :
#         func2 ( i, i + 1, queue=queue )
#
#     while not queue.empty () :
#         result = queue.get ()
#         print ( result )

import threading
import time

def background_thread(func) :
    def callf(*args, **kwargs) :
        t = threading.Thread ( target=func, args=(*args,), kwargs=kwargs )
        t.start ()
        # t.join()  # 不等待子线程结束
        return  # 不需要子线程函数执行结果

    return callf


# @background_thread
# def demo_thr(sleep, name) :
#     print ( 'in demo_thr' )
#     print ( 'Hi, ', name )
#     time.sleep ( sleep )
#     print ( 'end demo_thr' )
#     return 'demo_thr 执行完成'
#     pass
#
#
# if __name__ == '__main__' :
#     demo_thr ( 5, 'Caspar' )