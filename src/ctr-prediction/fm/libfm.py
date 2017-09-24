# _*_ coding: utf-8 _*_

import math
import sys
import subprocess

data_path = '../output/fm/'
result_path = '../output/fm/'

cmd = 'ctr-prediction/fm/libFM -task r -train {train} -test {test} -out {out} -method mcmc -learn_rate 0.2 -dim \'1,1,8\' ' \
      '-iter 150 -validation {train}'.format(train=result_path + 'train.fm', test=result_path + 'test.fm', out=result_path + 'preds.txt')
subprocess.call(cmd, shell=True, stdout=sys.stdout)


with open(result_path + 'submission.csv', 'w') as outfile:
    outfile.write('id,prob\n')
    fi = open(result_path + 'preds.txt')
    for t, line in enumerate(fi, start=1):
        outfile.write('{0},{1}\n'.format(t, float(line.rstrip())))
    fi.close()

cmd = 'rm {0}train.fm {0}test.fm {0}preds.txt'.format(result_path)
subprocess.call(cmd, shell=True)

