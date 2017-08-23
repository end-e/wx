# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/18 8:50'
import pandas as pd
import numpy as np
import datetime

data = [{'SaleValue': float('6.90'), 'DiscValue': float('1.09'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('5.30'), 'DiscValue': float('0.84'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('3.24'), 'DiscValue': float('0.51'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('2.28'), 'DiscValue': float('0.36'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('0.63'), 'DiscValue': float('0.10'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('1.73'), 'DiscValue': float('0.27'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('4.88'), 'DiscValue': float('0.77'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('15.49'), 'DiscValue': float('2.46'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('0.30'), 'DiscValue': float('0.07'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('7.90'), 'DiscValue': float('1.25'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('17.46'), 'DiscValue': float('2.77'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('13.50'), 'DiscValue': float('2.14'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('4.50'), 'DiscValue': float('0.71'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('6.50'), 'DiscValue': float('1.03'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('12.80'), 'DiscValue': float('2.03'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('4.23'), 'DiscValue': float('0.67'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('18.50'), 'DiscValue': float('2.93'), 'ListNo': 257970,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)},
        {'SaleValue': float('16.00'), 'DiscValue': float('0.00'), 'ListNo': 150794,
         'SDate': datetime.datetime(2017, 7, 15, 0, 0)}]

# dates = pd.date_range('20130101', periods=6)
# df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

# print(df.loc['20130102':'20130104',['A','B']])


# s = pd.Series([1,1,2,3,5])
# print(s)

# df2=pd.DataFrame(np.random.randn(6,4), columns=list('ABCD'))
# df2['sumAB'] = pd.Series(df2['A'] + df2['B'], index=df2.index)
# df2['10A'] = pd.Series(df2['A']*10, index=df2.index)
# print(df2.sum())

# df = pd.DataFrame(data)
# res = df.groupby('ListNo').sum()
# print(res.values)
# df.to_excel('pandas.xlsx',sheet_name='Sheet1')
# res = pd.read_excel('pandas.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
# print(res)




if __name__ == '__main__':
    # import xlrd,xlwt
    #
    # book = xlrd.open_workbook('pandas.xlsx')
    # sheet = book.sheet_by_index(0)
    # nc = sheet.ncols
    # sheet.put_cell(0,nc,xlrd.XL_CELL_TEXT,u'总分',None)


    # import time
    # def countdown(n):
    #     while n > 0:
    #         print('T-minus', n)
    #         n -= 1
    #         time.sleep(5)
    #
    #
    # # Create and launch a thread
    # from threading import Thread
    #
    # t = Thread(target=countdown, args=(10,))
    # t.start()
    # if t.is_alive():
    #     print('Still running')
    # else:
    #     print('Completed')

    # from threading import Thread, Event
    # from queue import Queue
    # import time
    # def countdown(n, q):
    #     print('countdown starting')
    #     # started_evt.set()
    #     while n > 0:
    #         print('T-minus', n)
    #         n -= 1
    #         q.put(n)
    #         time.sleep(1)
    # # Create the event object that will be used to signal startup
    # # started_evt = Event()
    # # Launch the thread and pass the startup event
    # print('Launching countdown')
    # q = Queue()
    # t = Thread(target=countdown, args=(3, q))
    # t.start()
    # q.join()
    # print(q.get())

    from concurrent.futures import ThreadPoolExecutor
    def echo_data(data):
        print(data)
    pool = ThreadPoolExecutor(10)
    for i in range(1,10):
        pool.submit(echo_data,i)



