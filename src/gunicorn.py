import multiprocessing as mp
from wifichameleon.config import PROJ_ROOT, RELAY_CACHE, STRIP_MODE
import os
try:
  os.remove(PROJ_ROOT+RELAY_CACHE)
except:
  pass
if STRIP_MODE:
  bind = "0.0.0.0:5000"
else:
  bind = "0.0.0.0:5005"
timeout = 60
graceful_timeout = 60
workers = mp.cpu_count()