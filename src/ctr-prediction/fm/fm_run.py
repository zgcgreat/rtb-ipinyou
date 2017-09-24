# -*- encoding:utf-8 -*-
import subprocess

cmd = 'python3 ctr-prediction/fm/data2fm.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/fm/libfm.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/fm/evaluate.py'
subprocess.call(cmd, shell=True)
