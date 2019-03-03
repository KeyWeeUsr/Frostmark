"""
Style checker and test + coverage runner for Frostmark.
"""

from subprocess import Popen
from os import environ
from os.path import join, dirname, abspath

ROOT = dirname(abspath(__file__))
PKG = join(ROOT, 'frostmark')
PKG_DOC = join(ROOT, 'doc', 'source')
PKG_DOC_BUILD = join(ROOT, 'doc', 'build')
PKG_DOC_MAKE = join(ROOT, 'doc', 'make.py')

DO_PROFILE = False

CASES = [[
    'pycodestyle',
    '--ignore=none',
    '--show-source',
    '--count',
    '--max-line-length=79',
    ROOT
], [
    'pylint',
    '--jobs=0',
    'release.py', 'check.py', 'setup.py', PKG, PKG_DOC, PKG_DOC_MAKE
], [
    'coverage', 'run', '--branch', '--source', PKG,
    '-m', 'unittest', 'discover',
    '--failfast',
    '--catch',
    '--start-directory', join(PKG, 'tests'),
    '--top-level-directory', PKG
], [
    'coverage', 'report', '--show-missing'
], [
    'sphinx-build', '-M', 'html', PKG_DOC,
    join(ROOT, 'doc', 'build'), '-j', 'auto', '-n', '-W'
]]


if __name__ == '__main__':
    CASES_LEN = len(CASES)
    for i, test in enumerate(CASES):
        if DO_PROFILE:
            environ['PYTHONOPTIMIZE'] = 1

        proc = Popen(test)
        proc.communicate()

        if DO_PROFILE:
            del environ['PYTHONOPTIMIZE']

        current = str(i + 1).zfill(len(str(CASES_LEN)))
        print(f'[{current}/{CASES_LEN}] ', end='')

        if proc.returncode == 0:
            print('Success!')
        else:
            print('Fail!')
            exit(proc.returncode)
