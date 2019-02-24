"""
Module for running a web application wrapping the CLI.
"""

from os.path import join, dirname, abspath
from flask import Flask

ROOT = dirname(abspath(__file__))
BUILD = join(ROOT, 'build')
APP = Flask(
    __name__,
    static_folder=join(BUILD, 'static'),
    static_url_path='/static'
)
APP.debug = True


@APP.route('/')
def index():
    """
    Index landing page using React build.
    """

    with open(join(BUILD, 'index.html'), 'rb') as html:
        return html.read()


def main():
    """
    Main function for running the backend server.
    """
    APP.run()


if __name__ == '__main__':
    main()
