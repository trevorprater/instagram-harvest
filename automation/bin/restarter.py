import os, time
while 1:
    time.sleep(60*54)
    os.system('python start-workers.py 50')
    os.system('python kill-workers.py 50')
