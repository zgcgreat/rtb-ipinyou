# coding=utf-8
from __future__ import division
import math
from threshold import get_threshold
from buget_pacing import get_p, get_pp
from compute_c import get_preds
from datetime import datetime
import random

in_path = '../data/'
out_path = '../output/'


def bidding_price(CPM, floorprice, pctr):  # 出价策略函数
    avgCTR = get_avgCTR(pred_ctrs)
    return abs((CPM - floorprice)) * math.pow(math.e, pctr / avgCTR / 2) + floorprice


def bidding_const(bid):
    return bid


def bidding_random():
    return random.randint(0, 300)


def bidding_linear1(ctr, time_slot):
    if ctr / pred_ctrs[time_slot] >= 1.2:
        bid = 2 * cpms[time_slot]
    elif 0.8 < float(ctr / pred_ctrs[time_slot]) < 1.2:
        bid = cpms[time_slot]
    else:
        bid = 0
    return bid


def bidding_linear2(ctr, time_slot):
    bid = ctr / pred_ctrs[time_slot] * cpms[time_slot]
    return bid


def win(ccfm, bid):
    return bid >= ccfm[2] and bid > ccfm[3]  # 竞标价高于保留价，且高于市场成交价，即赢标


pctrs = []  # 存放预测ctr数据
fi = open(out_path + 'ffm/submission.csv', 'r')
next(fi)
for line in fi:
    pctr = float(line.replace('\n', '').split(',')[1])
    pctrs.append(pctr)
fi.close()


def get_avgCTR(pred_ctrs):
    sumCTR = 0
    for i in range(0, len(pred_ctrs)):
        sumCTR += pred_ctrs[i]
    avgCTR = sumCTR / len(pred_ctrs)
    return avgCTR


def get_timeSlot_data(day, t, length):
    pctr = []
    ccfm = []  # clk cnv floor marketprice
    total_cost = 0

    file = open(in_path + 'test12.csv', 'r')
    next(file)  # 文件第一行是头部信息，从文件第二行开始读取
    for line in file:
        s = line.split(',')
        daystamp = s[4][6:8]
        timestamp = s[4][8:10]  # 截取天数+小时

        if int(daystamp) == day:
            if t <= int(timestamp) < t + 2:
                clk = int(s[0])
                cnv = 0
                floorprice = int(s[20])
                marketprice = float(s[23])
                ccfm.append((clk, cnv, floorprice, marketprice))
                total_cost += marketprice
    file.close()
    # 获得每个时段的pctr
    for i in range(length, length + len(ccfm)):
        pctr.append(pctrs[i])
    return ccfm, total_cost, pctr


def simulateBidding(cases, budget, pctr, threshold, cpms, time_slot):  # cases : ccfm列表,(clk,cnv,floo,market)

    clk_true = 0  # 测试数据中实际的点击次数
    cost = 0
    clks = 0
    cnvs = 0
    bids = 0  # 投标次数
    imps = 0

    for j in range(0, len(cases)):
        case1 = cases[j]
        clk_true += case1[0]
    for i in range(0, len(cases)):
        case = cases[i]  # ccfm[i]
        theta = threshold
        if pctr[i] >= theta:  # 预测CTR 高于阈值的广告才进行投标
            if cost <= budget:
                bid = bidding_price(cpms, case[2], pctr[i])  # 出价策略，优化的主要目标之一
                # bid = random.randint(0, 300)
                # bid = 300
                bids += 1  # 每投一次标，投标次数加1
                if win(case, bid):
                    imps += 1
                    clks += case[0]
                    cnvs += case[1]
                    cost += case[3]
                '''
                    print('赢标 ！！！\n')
                else:
                    print('失败 ！！！\n')
                '''
            if cost > budget:
                break
    wr = float(imps / bids)  # 赢标率

    cpm = cost / imps
    if clks == 0:
        ecpc = 0
    else:
        ecpc = cost / clks
    return str(int(budget)) + '\t\t' + str(int(cost)) + '\t\t' + str(bids) + '\t\t' + str(imps) + '\t\t' + str(
        clks) + '\t\t' + str(clk_true) + '\t\t' + str(cnvs) + '\t\t' + str(ecpc) + '\t\t' + str(wr), cost, wr, cpm


def p_next(t, BGT):
    # 根据均值预测
    p = get_pp(BGT)  # 分发概率
    temp = 0
    for i in range(t, 12):
        temp += reqs[i] * p[i] * 1.0 * cpms[i]
    pt_next = p[t] / temp
    return pt_next


def start_bidding(fo, reqs, cpms, pred_ctr):
    day = 12  # 20130612这一天
    BGT = 10000000  # 一天的总预算30297100
    print('今天的总预算:', BGT)

    total_cost = 0  # 模拟过程中的实际总花费
    total_cost_true = 0  # 数据集中的实际总花费
    n = 12  # 将一天划分为12个时段

    nums = []
    for j in range(0, 12):
        nums.append(0)
    p = get_p(BGT)  # 分发概率 budgetpacing.py

    length = 0
    for i in range(0, 24, int(24 / n)):  # 划分时段

        # 2、无预算分配策略
        # budget = BGT - total_cost
        # pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)

        # 2、平均分配
        # budget = BGT / n
        # pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)

        # 3、基于点击率分配
        # sum_tmp = 0
        # ii = int(i / 2)
        # for k in range(ii, 12):
        #     sum_tmp += pred_ctrs[k]
        # budget = (BGT - total_cost) * pred_ctrs[int(i / 2)] / sum_tmp
        # pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)

        # 4、基于流量分配
        # sum_tmp = 0
        # ii = int(i / 2)
        # for k in range(ii, 12):
        #     sum_tmp += reqs[k]
        # budget = (BGT - total_cost) * reqs[int(i / 2)] / sum_tmp
        # pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)

        # 5、按时段长度占剩余时段总长度的比例分配
        # budget = (BGT - total_cost) * (1 / (12 - (i / 2)))
        # pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)

        # 6、我们的
        if i == 0:
            budget = reqs[int(i / 2)] * 1 * cpms[int(i / 2)] * p[int(i / 2)]
            # budget = BGT
            pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)
        if i != 22 and i != 0:
            pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)
            # budget = (BGT - tocost) * pt_next / wr
            budget = reqs[int(i / 2)] * 1 * cpms[int(i / 2)] * pt_next  # 因为用了赢标日志模拟广告请求，所以将预测的赢标率都设为了1
        if i == 22:
            pt_next = p_next(int(i / 2), BGT) * (BGT - total_cost)
            budget = min(reqs[int(i / 2)] * 1 * cpms[int(i / 2)] * pt_next, BGT - total_cost)

        num = reqs[int(i / 2)] * pt_next
        nums[int(i / 2)] += int(num)
        threshold = float(get_threshold(int(i / 2), int(num)))
        # threshold = 0

        ccfm, cost_t, pctr = get_timeSlot_data(day, i, length)
        length += len(ccfm)
        total_cost_true += cost_t

        if total_cost <= BGT:
            print('\n{0}-{1}时段log中的实际花费:'.format(i, i + 2), cost_t)
            print('本时段预算:', budget)
            result, cost, winrate, cpm = simulateBidding(ccfm, budget, pctr, threshold,
                                                                               cpms[int(i / 2)], int(i / 2))
            fo.write(result + '\n')

            total_cost += cost
            print('预算剩余:', BGT - total_cost)

            header = 'budget\t\tspend\t\tbid\t\tipm\t\tclk\t\tclk_true\t\tcnv\t\tecpc\t\twr'
            print(header + '\n')
            print(result)
        else:
            print('今天的预算已用完！！！')
            break

    fo.close()
    print('\nlog中统计得到的一天的实际总花费:', total_cost_true)


if __name__ == '__main__':
    start = datetime.now()
    fo = open(out_path + 'rtb-result/result.xls', 'w')
    header = 'budget\t\tspend\t\tbid\t\tipm\t\tclk\t\tclk_true\t\tcnv\t\tecpc\t\twr'
    fo.write(header + "\n")
    reqs, clks, cpms, pred_ctrs = get_preds()
    start_bidding(fo, reqs, cpms, pred_ctrs)
    fo.close()
    end = datetime.now()
    t = end - start
    print('全部完成，耗时:', t)
