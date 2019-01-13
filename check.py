"""
Style checker for Frostmark.
"""

from subprocess import Popen
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
PKG = join(ROOT, 'frostmark')
PKG_DOC = join(ROOT, 'doc', 'source')
PKG_DOC_MAKE = join(ROOT, 'doc', 'make.py')
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
    'check.py', 'setup.py', PKG, PKG_DOC, PKG_DOC_MAKE
], [
    'coverage', 'run', '--source', PKG,
    '-m', 'unittest', 'discover',
    '--failfast',
    '--catch',
    '--start-directory', join(PKG, 'tests'),
    '--top-level-directory', PKG
], [
    'coverage', 'report', '--show-missing'
]]


if __name__ == '__main__':
    for i, test in enumerate(CASES):
        proc = Popen(test)
        proc.communicate()
        print(f'[{i + 1}/{len(CASES)}] ', end='')
        if proc.returncode == 0:
            print('Success!')
        else:
            print('Fail!')
            break
