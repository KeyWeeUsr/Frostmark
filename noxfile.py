"""
Style checker and test + coverage runner for Frostmark.

$ pip install --upgrade nox
$ nox
"""

from os import environ
from os.path import join, expanduser
import nox
from setup import ROOT, SETUP_KWARGS

PKG = join(ROOT, 'frostmark')
PKG_DOC = join(ROOT, 'doc', 'source')
PKG_DOC_MAKE = join(ROOT, 'doc', 'make.py')


@nox.session
def lint(session):
    """
    Install and run pycodestyle and pylint with special flags.
    """

    # install dev packages
    for dev in SETUP_KWARGS['extras_require']['dev']:
        session.install(dev)

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
def tests(session):
    """
    Install and run test runner + coverage report.
    """

    # install dependencies
    for pkg in SETUP_KWARGS['install_requires']:
        session.install(pkg)

    # install this package as editable
    session.install('--editable', '.')

    # run unittests with coverage package and create report
    session.run(
        'coverage', 'run', '--source', PKG,
        '-m', 'unittest', 'discover',
        '--failfast',
        '--catch',
        '--start-directory', join(PKG, 'tests'),
        '--top-level-directory', PKG
    )

    # show coverage report
    session.run('coverage', 'report', '--show-missing')
