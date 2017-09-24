
# -*- coding: <utf-8> -*-

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from datetime import datetime
from csv import DictReader

'''
功能:画测试集中投标价和赢标价的走势图
'''

date = '12'
path = '../../data/'

x = []
y1 = []
y2 = []
fi = open(path + 'test.csv', 'r')
for row in DictReader(fi):
    x1 = int(row['hour'])
    bidprice = int(row['bidprice'])
    payprice = int(row['payprice'])
    x.append(x1)
    y1.append(bidprice)
    y2.append(payprice)

y1.sort()
y2.sort()

pl.plot(x, y1, label='bidprice', color='r')

pl.plot(x, y2, label='payprice', color='b')   # 折线图
# T = np.arctan2(x, y2)

plt.legend(loc='upper left')

# pl.xticks(x)  # 设置x轴刻度
plt.ylim(0, 400)
plt.title('bidprice-payprice')
plt.xlabel('Time')
plt.ylabel('Money')
plt.grid(True)  # 添加网格
plt.show()

