# _*_ coding: utf-8 _*_

import subprocess

cmd = 'python3 ctr-prediction/lr/data2vw.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/lr/vw.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/lr/evaluate.py'
subprocess.call(cmd, shell=True)