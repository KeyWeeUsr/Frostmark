"""
Style checker for Frostmark.
"""

from subprocess import Popen
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
CASES = [
    ['pycodestyle', f'{ROOT}'],
    ['pylint', 'check.py', 'setup.py', f'{join(ROOT, "frostmark")}']
]


if __name__ == '__main__':
    for test in CASES:
        Popen(test).communicate()
