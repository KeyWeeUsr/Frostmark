"""
Module for running a web application wrapping the CLI.
"""

from os import environ
from os.path import join, dirname, abspath
from flask import Flask, Response, request

from frostmark.common import (
    fetch_bookmark_tree,
    fetch_folder_tree,
    json_bookmark_tree
)
from frostmark.editor import Editor

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


@APP.route('/list_tree')
def list_tree():
    """
    Return a flat list of a bookmark tree.
    """
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


@APP.route('/list_folders')
def list_folders():
    """
    Return a flat list of a folder tree.
    """
    response = Response(
        response=json_bookmark_tree(fetch_folder_tree()),
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        mimetype='application/json'
    )
    return response


@APP.route('/edit_bookmark', methods=['POST'])
def edit_bookmark():
    """
    Edit a single bookmark via HTML form.
    """
    # collect parameters
    bookmark_id = request.form.get('id', type=int)
    folder_id = request.form.get('folder', type=int)
    name = request.form.get('title')
    url = request.form.get('url')
    status = 302

    # only edit if all the fields are ok
    if all([item is not None for item in (bookmark_id, folder_id, name, url)]):
        Editor.rename_bookmark(
            bookmark_id=bookmark_id,
            name=name
        )
        Editor.change_bookmark_url(
            bookmark_id=bookmark_id,
            url=url
        )
        Editor.change_parent_bookmark(
            bookmark_id=bookmark_id,
            parent_id=folder_id
        )
        status = 301

    response = Response(
        status=status,
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*',
            'Location': '/'
        },
        mimetype='application/json'
    )
    return response


def main():
    """
    Run Flask app on a specific host.
    """
    APP.run(host=environ.get('FROSTMARK_HOST', '127.0.0.1'))


if __name__ == '__main__':
    main()
