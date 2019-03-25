"""
Module for running a web application wrapping the CLI.
"""

import json
from os import environ
from os.path import join, dirname, abspath
from tempfile import NamedTemporaryFile
from flask import Flask, Response, request

from frostmark.common import (
    fetch_bookmark_tree,
    fetch_folder_tree,
    json_bookmark_tree
)
from frostmark.editor import Editor
from frostmark.exporter import Exporter
from frostmark.profiles import get_all_profiles
from frostmark.importer import Importer

ROOT = dirname(abspath(__file__))
BUILD = join(ROOT, 'build')
APP = Flask(
    __name__,
    static_folder=join(BUILD, 'static'),
    static_url_path='/static'
)
APP.debug = False


@APP.route('/')
def index():
    """
    Index landing page using React build.
    """

    with open(join(BUILD, 'index.html'), 'rb') as html:
        return html.read()


@APP.route('/api/list_tree')
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


@APP.route('/api/list_folders')
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


@APP.route('/api/edit_bookmark', methods=['POST'])
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


@APP.route('/api/export_bookmarks')
def export_bookmarks():
    """
    Export all bookmarks as HTML.
    """
    export = Exporter.prepare_export()
    response = Response(
        response=export.encode('utf-8'),
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*',
            'Content-Disposition': 'attachment; filename="export.html"'
        },
        mimetype='application/octet-stream'
    )
    return response


@APP.route('/api/list_profiles')
def list_profiles():
    """
    Return all profiles found in all available browsers.
    """
    response = Response(
        response=json.dumps(get_all_profiles()),
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        mimetype='application/json'
    )
    return response


@APP.route('/api/import_bookmarks', methods=['POST'])
def import_bookmarks():
    """
    Import bookmarks from file.
    """
    browser = request.form.get('browser')
    bookmarks = request.files.get('file')
    status = 302

    # only edit if all the fields are ok
    if all([item is not None for item in (browser, bookmarks)]):
        with NamedTemporaryFile() as temp:
            temp.write(bookmarks.read())
            Importer(browser).import_from(temp.name)
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
