import subprocess
import sys
import time

time.sleep(0.2)
try:
    subprocess.run([sys.executable, "main.py"], check=True)
except:
    pass