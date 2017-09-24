# -*- encoding:utf-8 -*-
import math

'''
计算分发概率基准值c
'''

path = '../output/rtb-result'


# 时间衰减影响力系数
def f(x):
    return pow(math.e, -24 * (x - 1)) - pow(math.e, -24 * x)


s = []  # 存放从20130312到20130606各天的影响力系数
for i in range(0, 6):
    s.append(f(i + 1))

S = 1 - pow(math.e, -24 * 7)


def getReqs(t, argv):
    req = []
    reqs = 0
    fi = open('{0}/real/{1}.xls'.format(path, argv), 'r')
    for e, line in enumerate(fi, start=1):
        s = line.split('\t')
        req.append(s[t])
        if e == 6:
            break
    fi.close()

    for i in range(0, 6):
        # reqs += ((float(s[5 - i]) / S) * float(req[i]))  # 通过衰减预测第7天的广告请求数
        reqs += float(req[i])
    reqs = reqs / 6  # 通过平均预测第7天的广告请求数
    return reqs


def get_preds():
    imps = []
    clks = []
    cpms = []
    ctrs = []
    for t in range(0, 12):
        imp = int(getReqs(t, 'imps'))
        imps.append(imp)
        clk = getReqs(t, 'clks')
        clks.append(clk)
        cpm = getReqs(t, 'cpms')
        cpms.append(cpm)
        ctr = getReqs(t, 'ctrs')
        ctrs.append(ctr)
    return imps, clks, cpms, ctrs


def get_c(BGT):
    imps, clks, cpms, ctrs = get_preds()
    pBGT = 0  # 预测的总预算
    for i in range(0, len(imps)):
        pBGT += imps[i] * cpms[i]
    c = BGT / pBGT
    return c
