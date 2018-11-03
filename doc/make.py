'''
Simple pythonized Makefile to ensure compatibility between multiple platforms.
'''

import sys
from os import mkdir
from os.path import join, abspath, dirname
from subprocess import Popen
from shutil import rmtree

ROOT = dirname(abspath(__file__))
SPHINXOPTS = []
SPHINXBUILD = 'sphinx-build'
SOURCEDIR = join(ROOT, 'source')
BUILDDIR = join(ROOT, 'build')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'help':
        PROC = Popen([
            SPHINXBUILD, '-M', 'help',
            SOURCEDIR, BUILDDIR, ''.join(SPHINXOPTS)
        ])
        PROC.communicate()
        EXITCODE = PROC.returncode
    elif len(sys.argv) > 1 and sys.argv[1] == 'clean':
        rmtree(BUILDDIR)
        mkdir(BUILDDIR)
        EXITCODE = 0
    else:
        COMMAND = [
            SPHINXBUILD, '-M', ''.join(sys.argv[1:]),
            SOURCEDIR, BUILDDIR
        ]

        if SPHINXOPTS:
            COMMAND.extend(SPHINXOPTS)

        PROC = Popen(COMMAND)
        PROC.communicate()
        EXITCODE = PROC.returncode
    exit(EXITCODE)
