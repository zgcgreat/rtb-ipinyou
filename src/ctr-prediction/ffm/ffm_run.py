# -*- encoding:utf-8 -*-
import subprocess

cmd = 'python3 ctr-prediction/ffm/data2ffm.py {date}'.format(date=11)
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/ffm/ffm.py {date}'.format(date=11)
subprocess.call(cmd, shell=True)


cmd = 'python3 ctr-prediction/ffm/data2ffm.py {date}'.format(date=12)
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/ffm/ffm.py {date}'.format(date=12)
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/ffm/evaluate.py'
subprocess.call(cmd, shell=True)


path = '../data/'
cmd = 'rm {path}train11.csv {path}test11.csv'.format(path=path)
subprocess.call(cmd, shell=True)
