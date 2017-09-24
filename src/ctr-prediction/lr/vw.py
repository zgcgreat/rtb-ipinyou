# _*_ coding: utf-8 _*_

import subprocess
import math

path = '../output/lr/'
submission = path + 'submission.csv'

# 训练
cmd = 'vw {path}train.vw -f {path}model --sgd -c -k --passes 100 -b 20 ' \
      '--loss_function logistic --early_terminate 5'.format(path=path)
subprocess.call(cmd, shell=True)

# 测试
cmd = 'vw {path}test.vw -t -i {path}model -p {path}preds.txt --loss_function logistic '.format(path=path)
subprocess.call(cmd, shell=True)


def sigmod(x):
    return 1 / (1 + math.exp(-x))


with open(submission, 'w') as outfile:
    outfile.write('id,prob\n')
    for t, line in enumerate(open(path+'preds.txt', 'r'), start=1):
        row = line.strip().split(' ')
        pro = sigmod(float(line))
        outfile.write('%s,%f\n' % (t, pro))


# 删除中间数据文件
cmd = 'rm {path}train.vw.cache {path}train.vw {path}test.vw {path}preds.txt {path}model'.format(path=path)
subprocess.call(cmd, shell=True)


