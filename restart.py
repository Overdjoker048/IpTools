import subprocess
import sys
import time

time.sleep(0.2)
subprocess.run([sys.executable, "main.py"], check=True)