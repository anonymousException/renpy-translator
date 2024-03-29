
import sys
import threading
import time
from datetime import datetime

timestamp = str(int(time.time()))
log_path = 'log'+'.txt'
f=open(log_path,'a+',encoding='utf-8')
sys.stdout = f
sys.stderr = f
log_lock = threading.Lock()
def log_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=True):
    log_lock.acquire()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),end ='\t')
    print(*objects, sep=' ', end='\n', file=sys.stdout, flush=True)
    log_lock.release()