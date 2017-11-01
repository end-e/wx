# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/11/1 14:02'
import signal

def time_limit(interval):
    def wraps(func):
        def handler(signum, frame):
            raise RuntimeError()
        def deco(*args, **kwargs):
            signal.signal(signal.SIGCHLD, handler)
            signal.alarm(interval)
            res = func(*args, **kwargs)
            signal.alarm(0)
            return res
        return deco
    return wraps

class TimeoutError(Exception):
    pass

# def time_limit(interval):
#     def wraps(func):
#         def handler(signum, frame):
#             raise TimeoutError()
#         def deco(*args, **kwargs):
#             signal.signal('', handler)
#             signal.alarm(interval)
#             try:
#                 res = func(*args, **kwargs)
#             except TimeoutError as exc:
#                 res = ''
#             finally:
#                 signal.alarm(0)
#                 signal.signal(signal.SIGALRM, signal.SIG_DFL)
#             # res = func(*args, **kwargs)
#             # signal.alarm(0)
#             return res
#         return deco
#     return wraps