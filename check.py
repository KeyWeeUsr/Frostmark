"""
Style checker for Frostmark.
"""

from subprocess import Popen
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
PKG = join(ROOT, 'frostmark')
CASES = [[
    'pycodestyle',
    '--ignore=none',
    '--show-source',
    '--count',
    '--max-line-length=79',
    f'{ROOT}'
], [
    'pylint',
    '--jobs=0',
    'check.py', 'setup.py', PKG
], [
    'python', '-m', 'unittest', 'discover',
    '--failfast',
    '--catch',
    '--start-directory', join(PKG, 'tests'),
    '--top-level-directory', PKG
]]


if __name__ == '__main__':
    for test in CASES:
        Popen(test).communicate()
