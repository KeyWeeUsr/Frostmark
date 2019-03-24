# Frostmark

[![Coverage](https://coveralls.io/repos/KeyWeeUsr/frostmark/badge.svg?branch=master)
](https://coveralls.io/r/KeyWeeUsr/frostmark?branch=master)
[![Build](https://travis-ci.org/KeyWeeUsr/frostmark.svg?branch=master)
](https://travis-ci.org/KeyWeeUsr/frostmark)
[![Docs](https://readthedocs.org/projects/frostmark/badge/?version=latest)
](https://frostmark.readthedocs.io/en/latest/)
[![GitHub version](https://badge.fury.io/gh/keyweeusr%2Ffrostmark.svg)
](https://badge.fury.io/gh/keyweeusr%2Ffrostmark)
[![PyPI version](https://img.shields.io/pypi/v/frostmark.svg)
](https://pypi.org/project/frostmark/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/frostmark.svg)
](https://pypi.org/project/frostmark/)
[![Latest release deps](https://img.shields.io/librariesio/release/pypi/frostmark.svg)
](https://libraries.io/pypi/frostmark)
[![GitHub repo deps](https://img.shields.io/librariesio/github/keyweeusr/frostmark.svg)
](https://libraries.io/pypi/frostmark)

[![Downloads total](https://pepy.tech/badge/frostmark)
](https://pepy.tech/project/frostmark)
[![Downloads month](https://pepy.tech/badge/frostmark/month)
](https://pepy.tech/project/frostmark)
[![Downloads week](https://pepy.tech/badge/frostmark/week)
](https://pepy.tech/project/frostmark)
[![All Releases](https://img.shields.io/github/downloads/keyweeusr/frostmark/total.svg)
](https://github.com/KeyWeeUsr/frostmark/releases)
[![Code bytes](https://img.shields.io/github/languages/code-size/keyweeusr/frostmark.svg)
](https://github.com/KeyWeeUsr/frostmark)
[![Repo size](https://img.shields.io/github/repo-size/keyweeusr/frostmark.svg)
](https://github.com/KeyWeeUsr/frostmark)


Frostmark is a simple bookmarks manager. It can import all bookmarks from
multiple browsers, list the imported bookmarks and export them via HTML format.

The goal for the future is to be able to extensively manage the bookmarks both
via console and GUI interface, automatically search the system for the
available browsers, import the profiles without explicitly specifying paths
to the browser profiles and export all or only specific folders even directly
into the browser's bookmarks.

Feel free to open a pull request with your improvements for the project, open
an issue in case of bug or a feature request and come and talk about the
project in the
[Matrix community](https://riot.im/app/#/group/+frostmark:matrix.org)

## Installation

You can install the package with:

    pip install https://github.com/KeyWeeUsr/frostmark

## Documentation

The documentation is hosted via ReadTheDocs.org
[here](https://frostmark.readthedocs.io/en/latest/).

## Usage

After a successful Python package installation you can invoke frostmark like
this:

    frostmark

To access the help page just add `--help` after the command you want:

    frostmark -h
    frostmark --help

Currently the development is aiming for console version support first:

    frostmark console -h
    frostmark console --help

### Importing bookmarks

The browsers store your bookmarks in a place called "profile". Frostmark
will list each (in this case Firefox) profile on a new line for you with:

    frostmark console -p firefox
    frostmark console --list-profiles firefox

After you know what profile you want to import your bookmarks from, pass the
same profile location to the command that imports it:

    frostmark console -i firefox <PROFILE PATH>
    frostmark console --import-bookmarks firefox <PROFILE PATH>

Mostly you will only have one profile unless you ask the browser to create more
e.g. with signing with multiple Firefox accounts to Firefox or multiple Google
accounts to Chrome.

### Listing bookmarks

To check whether the import was successful you can list the bookmark tree with:

    frostmark console -l
    frostmark console --list-bookmarks

### Exporting bookmarks

Sometimes you just want to move the bookmarks between the browsers. For that
you can import the bookmarks from a browser profile into Frostmark and then
simply export it into a format another browser understands:

    frostmark console -x PATH
    frostmark console --export-bookmarks PATH

## Development

To add new features, fix existing stuff or propose other changes clone the repo
first to your machine:

    git clone https://github.com/KeyWeeUsr/frostmark

Then install it in an "editable" mode, so that the changes you do in the repo
are reflected right when you do them instead of re-installing the package to
Python again and again:

    pip install -e .[dev]
    pip install --editable .[dev]

After you do some changes in the repo, run the style checker and test runner
to prevent causing bugs:

    python check.py
