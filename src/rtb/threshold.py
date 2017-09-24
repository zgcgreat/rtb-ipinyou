# -*- encoding:utf-8 -*-
from compute_c import get_preds

'''
功能: 找到每个时段广告请求ctr过滤阈值，利用了前一天的数据，从原始数据中用前5天的数据对第6天做一个ctr预测
'''

# 预测得到的20130612各时段的广告请求数
reqs, clks, cpms, pred_ctrs = get_preds()


# 先从submission11中取出所以ctr值放入一个列表
lt1 = []
b = 0
fi = open('../output/ffm/submission11.csv', 'r')
next(fi)
for line in fi:
    s = line.split(',')
    ctr = s[1]
    lt1.append(ctr)
fi.close()


def get_threshold(i, c):
    sum = 0
    for j in range(0, i):
        sum += reqs[j]
    lt = lt1[sum:(sum + reqs[i])]
    lt.sort(reverse=True)
    if len(lt) <= c:
        t = lt[-1]
    else:
        t = lt[c]
    return t


