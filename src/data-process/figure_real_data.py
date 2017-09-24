# coding=utf-8

import numpy as np
import pylab as pl

'''
功能:画session2每天的各种走势图
'''

path = '../../output/rtb-result/real/'


def get_list(arg):  # 读出文件的每一行添加到一个列表
    file = open(path + '{0}.xls'.format(arg), 'r')
    list = []
    for line in file:
        feats = []
        s = line.split('\t')
        for i in range(len(s)):
            if s[i] != '\n':
                feats.append(s[i])
        list.append(feats)
    file.close()
    return list


def figure(list, filename):
    x = np.arange(1, 13)
    for i in range(len(list)):
        if i < 4:
            date = '0{0}'.format(i + 6)
        else:
            date = '{0}'.format(i + 6)
        pl.plot(x, list[i], label='{0}'.format(date))
        pl.plot(x, list[i], 'o')

    pl.legend(loc='best')
    pl.xticks(x)  # 设置x轴刻度
    pl.title('{0} of advertiser 1458'.format(filename))
    pl.xlabel('timeSlot')
    pl.ylabel('{0}'.format(filename))
    pl.grid(True)  # 添加网格
    pl.savefig('{0}images/{1}.png'.format(path, filename, ), dpi=100)
    pl.show()


if __name__ == '__main__':
    argv = ['imps', 'clks', 'ctrs', 'cpms', 'payprices']
    for arg in argv:
        list = get_list(arg)
        figure(list, arg)
