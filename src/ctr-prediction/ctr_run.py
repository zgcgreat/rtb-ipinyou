# -*- encoding:utf-8 -*-
import subprocess
from datetime import datetime

start = datetime.now()

cmd = 'python3 ctr-prediction/ffm/ffm_run.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/fm/fm_run.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/lr/lr_run.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 plot_roc.py'
subprocess.call(cmd, shell=True)

print('time:', datetime.now() - start)
