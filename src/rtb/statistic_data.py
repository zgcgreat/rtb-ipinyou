# -*- coding: <utf-8> -*-

"""
功能:统计每个广告主一天中每个时段的投标次数,这里统计的是1458广告主的
"""
import numpy as np
from csv import DictReader

in_path = '../data/'
out_path = '../output/'

fi = open(in_path + 'train12.csv', 'r')
T = 12   # timeSlot  将一天划分为T个时段
imps = []
clks = []
bidprices = []
payprices = []
ctrs = []
cpms = []
for i in range(6):
    imps.append([])
    clks.append([])
    bidprices.append([])
    payprices.append([])
    ctrs.append([])
    cpms.append([])
    for j in range(T):
        imps[i].append(0)
        clks[i].append(0)
        bidprices[i].append(0)
        payprices[i].append(0)
        ctrs[i].append(0)
        cpms[i].append(0)

for t, row in enumerate(DictReader(fi), start=1):
    clk = int(row['click'])
    day = int(row['timestamp'][6:8])
    hour = int(row['timestamp'][8:10])
    bidprice = int(row['bidprice'])
    payprice = int(row['payprice'])
    for i in range(0, 24, 2):
        if i <= int(hour) < i + 2:
            imps[day - 6][int(i / 2)] += 1
            clks[day - 6][int(i / 2)] += clk
            bidprices[day - 6][int(i / 2)] += bidprice
            payprices[day - 6][int(i / 2)] += payprice
fi.close()
# print('各时段的赢标(展示)次数:\n', imps)
# print('各时段的点击次数:\n', clks)


for i in range(np.array(imps).shape[0]):
    for k in range(T):
        ctrs[i][k] = float(clks[i][k] / imps[i][k])
        cpms[i][k] = payprices[i][k] / imps[i][k]


def writer(argv, list):
    fo = open(out_path + 'rtb-result/real/{}.xls'.format(argv), 'w')
    for i in range(np.array(list).shape[0]):
        for j in range(T):
            fo.write(str(list[i][j]) + '\t')
        fo.write('\n')
    fo.close()

args = ['imps', 'clks', 'bidprices', 'payprices', 'ctrs', 'cpms']
lts = [imps, clks, bidprices, payprices, ctrs, cpms]

for i in range(len(args)):
    writer(args[i], lts[i])
