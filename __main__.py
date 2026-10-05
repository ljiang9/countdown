"""python -m countdown 入口。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from countdown import main

if __name__ == "__main__":
    main()
