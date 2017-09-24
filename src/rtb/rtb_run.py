import subprocess

cmd = 'python3 rtb/statistic_data.py'
subprocess.call(cmd, shell=True)

cmd = 'python3 rtb/rtb.py'
subprocess.call(cmd, shell=True)
