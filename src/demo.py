# -*- encoding:utf-8 -*-
import subprocess
from datetime import datetime

start = datetime.now()

cmd = 'python3 data-process/split_data.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 ctr-prediction/ctr_run.py'
subprocess.call(cmd, shell=True)

# cmd = 'python3 ctr-prediction/plot_roc.py'
# subprocess.call(cmd, shell=True)

cmd = 'python3 rtb/rtb_run.py'
subprocess.call(cmd, shell=True)

print('time:', datetime.now() - start)
