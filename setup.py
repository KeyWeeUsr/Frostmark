#!/usr/bin/env python
"""
Basic setup.py
"""

from glob import glob
from os.path import abspath, dirname, join, relpath
from setuptools import setup, find_packages
from frostmark import VERSION


ROOT = abspath(dirname(__file__))
REPO = 'https://github.com/KeyWeeUsr/Frostmark'
NAME = 'frostmark'
PKG = join(ROOT, NAME)


with open(join(ROOT, "README.md")) as fd:
    README = fd.read()


with open(join(ROOT, 'LICENSE.txt')) as fd:
    GPL = fd.read()


DATA = [relpath(path, ROOT) for path in [
    'LICENSE.txt',
    'README.md',
] + [
    *glob(join(PKG, 'tests', '*.html')),
    *glob(join(PKG, 'tests', '*.json')),
    *glob(join(PKG, 'tests', '*.sqlite')),
    *glob(join(
        PKG, 'core', 'gui', 'react', 'build', '*.*'
    )),
    *glob(join(
        PKG, 'core', 'gui', 'react', 'build', 'static', 'css', '*.*'
    )),
    *glob(join(
        PKG, 'core', 'gui', 'react', 'build', 'static', 'js', '*.*'
    ))
]]


setup(
    name=NAME,
    version=VERSION,
    license=GPL,

    description='TBD',
    long_description='TBD',
    packages=find_packages(),

    author='Peter Badida',
    author_email='keyweeusr@gmail.com',

    url=REPO,
    download_url=REPO + '/tarball/' + VERSION,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],

    entry_points={
        'console_scripts': [
            f'{NAME} = {NAME}.__main__:main',
            f'fmcli = {NAME}.__main__:main_console',
            f'fmgui = {NAME}.__main__:main_gui'
        ]
    },
    install_requires=['ensure', 'sqlalchemy', 'anytree'],
    extras_require={
        'dev': ['pycodestyle', 'pylint', 'coverage'],
        'ci': ['coveralls'],
        'doc': ['sphinx>=1.8.1'],
        'gui_react': ['flask'],
        'release': ['setuptools', 'wheel', 'twine', 'sphinx>=1.8.1']
    },
    include_package_data=True,
    data_files=[(NAME, DATA)]
)
