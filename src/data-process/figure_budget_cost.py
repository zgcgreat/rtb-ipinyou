# coding=utf-8

import numpy as np
import pylab as pl

'''
功能:画预算和实际花费的走势图
'''

path = '../../output/rtb-result/'


def figure(filename):
    x = np.arange(0, 12)
    y1 = []
    y2 = []
    file = open(path + filename + '.xls', 'r')
    next(file)
    # next(file)
    for line in file:
        y11 = line.split('\t\t')[0]
        y1.append(y11)
        y22 = line.split('\t\t')[1]
        y2.append(y22)
    file.close()

    if len(y1) < 12:
        for i in range(len(y1), 12):
            y1.append(0)
            y2.append(0)

    pl.plot(x, y1, label='budget', color='r')
    pl.plot(x, y1, 'o')

    pl.plot(x, y2, label='spend', color='b')
    pl.plot(x, y2, 'o')

    pl.legend(loc='best')
    # pl.legend([plot1, plot2], ('budget', 'spend'), loc = 1)

    pl.xticks(x)  # 设置x轴刻度
    pl.title('{0}'.format(filename))
    pl.xlim(0)
    pl.ylim(0)
    pl.xlabel('Time')
    pl.ylabel('Money')
    pl.grid(True)  # 添加网格
    # pl.savefig('{0}/pictures/{1}.png'.format(path, filename,), dpi=100)
    pl.show()


if __name__ == '__main__':
    # argv = ['no_budget-bid', 'avg_budget-bid', 'time_budget-bid', 'traffic_budget-bid', 'budget-bid']
    argv = ['result']

    for arg in argv:
        figure(arg)
