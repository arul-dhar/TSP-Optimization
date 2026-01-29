import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(REPO_ROOT, "data", "usa13509.tsp")
NN_OUT = os.path.join(REPO_ROOT, "results", "nearest_neighbor_tours.txt")

def run():
    # 1) Run nearest neighbor multi-start to generate tours file
    subprocess.check_call([sys.executable, os.path.join(REPO_ROOT, "src", "nearest_neighbor.py")])

    # 2) Run 2-opt improvement (reads nearest_neighbor_tours.txt)
    subprocess.check_call([sys.executable, os.path.join(REPO_ROOT, "src", "two_opt.py")])

if __name__ == "__main__":
    run()
