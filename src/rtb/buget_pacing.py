# -*- encoding:utf-8 -*-


import math
from compute_c import get_c, get_preds

'''
预算步进
'''

pred_reqs, pred_clks, pred_cpms, pred_ctrs = get_preds()
avg_ctr = sum(pred_ctrs) / len(pred_ctrs)
avg_cpm = sum(pred_cpms) / len(pred_cpms)


# 求平均alfa
def avgalfa(ctr):
    T = 12  # 将一天分成T个时段
    sum_alfasquare = 0
    for i in range(0, T):
        kpi_t = ctr  # 当前时段平均展示质量
        avgkpi = avg_ctr  # 一天的平均展示质量
        alfa_t = (kpi_t - avgkpi) / avgkpi  # 时段t的alfa
        sum_alfasquare = sum_alfasquare + pow(alfa_t, 2)
    avg_alfa = pow(sum_alfasquare / T, 0.5)
    return alfa_t, avg_alfa


# 求平均beta
def avgbeta(cpm):  # cpm: 当前时段平均成交价 avgcpm：一天的平均成交价
    T = 12  # 将一天分成T个时段
    sum_betasquare = 0
    for i in range(0, T):
        beta_t = (cpm - avg_cpm) / avg_cpm
        sum_betasquare = sum_betasquare + pow(beta_t, 2)

    avg_beta = pow(sum_betasquare / T, 0.5)
    return beta_t, avg_beta


# 映射函数
def f(x, fai):
    return 2 / (1 + math.pow(math.e, - x * fai))


# 广告展示质量系数函数
def qf(alfa):
    return f(alfa, 1)  # fai = 1


# 市场竞争程度系数
def cf(beta_t, alfa_t, avg_alfa, avg_beta):
    return f(-1 * avg_alfa / avg_beta * beta_t + alfa_t, 1)  # fai = 1


def p_t(ctr, cpm, BGT):
    c = get_c(BGT)
    alfa_t, avg_alfa = avgalfa(ctr)
    beta_t, avg_beta = avgbeta(cpm)
    cf_t = cf(beta_t, alfa_t, avg_alfa, avg_beta)
    qf_t = qf(alfa_t)
    p = c * cf_t * qf_t
    return p


# 各时段的步进p预测值
def get_p(BGT):
    p = []
    for i in range(0, 12):
        pt = p_t(pred_ctrs[i], pred_cpms[i], BGT)
        p.append(pt)
    return p


# 该时段p占当天的比例
def get_pp(BGT):
    sum = 0
    for i in range(0, 12):
        sum += get_p(BGT)[i]
    pp = []
    for j in range(0, 12):
        temp = get_p(BGT)[j] / sum
        pp.append(temp)
    return pp
