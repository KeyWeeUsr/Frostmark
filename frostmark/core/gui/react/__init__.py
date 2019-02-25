"""
Module for running a web application wrapping the CLI.
"""

from os.path import join, dirname, abspath
from flask import Flask, Response

from frostmark.common import fetch_bookmark_tree, json_bookmark_tree

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


@APP.route('/list_bookmarks')
def list_bookmarks():
    response = Response(
        response=json_bookmark_tree(fetch_bookmark_tree()),
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        mimetype='application/json'
    )
    return response


def main():
    """
    Main function for running the backend server.
    """
    APP.run()


if __name__ == '__main__':
    main()
