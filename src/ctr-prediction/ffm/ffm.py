import subprocess
import sys

date = sys.argv[1]

NR_THREAD = 8

path = '../output/ffm/'


# 训练
cmd = 'ctr-prediction/ffm/ffm-train -l 0.00002 -k 12 -t 50 -r 0.2 -s {nr_thread} -p {save}train.ffm  {save}train.ffm ' \
      '{save}model'.format(nr_thread=NR_THREAD, save=path)
subprocess.call(cmd, shell=True)
# 预测
cmd = 'ctr-prediction/ffm/ffm-predict {save}test.ffm {save}model {save}test.out'.format(save=path)
subprocess.call(cmd, shell=True)

with open(path + 'submission{}.csv'.format(date), 'w') as f:
    f.write('id,prob\n')
    for i, row in enumerate(open(path + 'test.out'), start=1):
        f.write('{0},{1}'.format(i, row))

cmd = 'rm {path}model {path}test.out {path}train.ffm {path}test.ffm'.format(path=path)
subprocess.call(cmd, shell=True)
