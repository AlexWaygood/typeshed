import itertools
import subprocess
import sys

for i in itertools.count():
    print(f"Iteration {i}")
    ret = subprocess.run([sys.executable, "tests/regr_test.py", "--all"], text=True)
    if ret.returncode != 0:
        break
