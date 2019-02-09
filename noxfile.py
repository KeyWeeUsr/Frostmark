"""
Style checker and test + coverage runner for Frostmark.

$ pip install --upgrade nox
$ nox
"""

from os import mkdir
from os.path import join, exists
from shutil import rmtree

import nox
from setup import ROOT

PKG = join(ROOT, 'frostmark')
PKG_DOC = join(ROOT, 'doc', 'source')
PKG_DOC_BUILD = join(ROOT, 'doc', 'build')
PKG_DOC_MAKE = join(ROOT, 'doc', 'make.py')


@nox.session
def lint(session):
    """
    Install and run pycodestyle and pylint with special flags.
    """

    # install dev packages
    session.install('--editable', '.[dev]')

    # run pycodestyle with custom flags
    session.run(
        'pycodestyle', '--ignore=none', '--show-source', '--count',
        '--max-line-length=79', '--exclude=.nox', ROOT
    )

    # run pylint with multiple processes
    session.run(
        'pylint', '--jobs=0', '--ignore=.nox',
        'noxfile.py', 'setup.py', PKG, PKG_DOC, PKG_DOC_MAKE
    )


@nox.session
def test(session):
    """
    Install and run test runner + coverage report as dev.
    """

    # install this package as editable
    session.install('--editable', '.[dev]')

    # run unittests with coverage package and create report
    session.run(
        'coverage', 'run', '--branch', '--source', PKG,
        '-m', 'unittest', 'discover',
        '--failfast',
        '--catch',
        '--start-directory', join(PKG, 'tests'),
        '--top-level-directory', PKG
    )

    # show coverage report
    session.run('coverage', 'report', '--show-missing')


@nox.session
def doc(session):
    """
    Install and run Sphinx to build documentation.
    """

    # install this package as editable
    session.install('--editable', '.[doc]')

    # clean first in case there is previous build
    if exists(PKG_DOC_BUILD):
        rmtree(PKG_DOC_BUILD)
        mkdir(PKG_DOC_BUILD)

    # run unittests with coverage package and create report
    session.run(
        'sphinx-build', '-M', 'html', PKG_DOC,
        join(ROOT, 'doc', 'build'), '-j', 'auto', '-n', '-W'
    )
