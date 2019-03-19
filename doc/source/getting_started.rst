Getting started
===============

Requirements
------------

* Python 3.7+ (however 3.6 should work too)

Installation
------------

Frostmark is distributed as a Python package on PyPI and on GitHub as a source
release with packages included. You can install multiple versions:

* CLI
* React GUI

The ``CLI`` version is the basic building stone and should work just fine for
quick listing or pulling and exporting the bookmarks from the browsers into
some common format. While you can use advanced options for editing bookmarks,
folders and their relationships, using the ``React GUI`` option is prettier.

You can install the ``CLI`` with::

    pip install frostmark

For the ``React GUI`` version you need to specify an additional flag for
``pip`` to install even the GUI dependencies::

    pip install frostmark[gui_react]

For installing from files (``.tar.gz`` or ``.whl``) you need to adjust the name
a little bit::

    # archive
    pip install frostmark.tar.gz
    pip install frostmark.tar.gz[gui_react]

    # wheel package
    pip install frostmark.whl
    pip install frostmark.whl[gui_react]

Commands
--------

After the successful installation you are provided with multiple options for
accessing the program:

* From Python as a module::

        # module help
        python -m frostmark
        python -m frostmark --help

        # CLI & CLI help
        python -m frostmark console
        python -m frostmark console --help

        # GUI & GUI help
        python -m frostmark gui
        python -m frostmark gui --help

* By specific commands provided by frostmark to the OS::

        # CLI & CLI help
        fmcli
        fmcli --help

        # GUI & GUI help
        fmgui
        fmgui --help
