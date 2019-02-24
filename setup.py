#!/usr/bin/env python
"""
Basic setup.py
"""

from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from frostmark import VERSION


ROOT = abspath(dirname(__file__))
REPO = 'https://github.com/KeyWeeUsr/Frostmark'


with open(join(ROOT, "README.md")) as fd:
    README = fd.read()


with open(join(ROOT, 'LICENSE.txt')) as fd:
    GPL = fd.read()


setup(
    name='frostmark',
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
            'frostmark = frostmark.__main__:main'
        ]
    },
    install_requires=['ensure', 'sqlalchemy', 'anytree'],
    extras_require={
        'dev': ['pycodestyle', 'pylint', 'coverage'],
        'ci': ['coveralls'],
        'doc': ['sphinx>=1.8.1'],
        'gui_react': ['flask']
    }
)
