'''
Module for retrieving bookmark data from Chrome `Bookmarks` file
and providing a clean tree structure for further use.
'''

import json
from ensure import ensure_annotations
from anytree import Node

from frostmark.common import (
    assemble_folder_tree, assemble_bookmark_tree, traverse
)
from frostmark.models import Folder, Bookmark


class ChromeImporter:
    '''
    Assembler for Chrome bookmark node tree.
    '''
    # pylint: disable=too-few-public-methods

    @staticmethod
    @ensure_annotations
    def walk_folders(item: dict, parent_id: int) -> list:
        '''
        Chrome Bookmarks JSON walker for folders.
        '''

        items = []
        if item['type'] != 'folder':
            return items

        items.append({
            'id': int(item['id']),
            'folder_name': item['name'],
            'parent_folder_id': parent_id or None,
            'item': item
        })
        for child in item['children']:
            items += ChromeImporter.walk_folders(child, int(item['id']))
        return items

    @staticmethod
    @ensure_annotations
    def walk_bookmarks(item: dict, folder_id: int) -> list:
        '''
        Chrome Bookmarks JSON walker for bookmarks in folders.
        '''

        items = []

        for child in item.get('children', []):
            if 'type' not in child:
                # some kind of broken structure
                continue

            if child['type'] == 'folder':
                # folder, therefore will be handled in the next
                # walk from another item of flat list
                continue

            elif child['type'] == 'url':
                # yay, bookmark
                items.append({
                    'id': int(child['id']),
                    'title': (
                        child['url']
                        if not child['name']
                        else child['name']
                    ),
                    'folder_id': folder_id,
                    'url': child['url']
                })
        return items

    @staticmethod
    @ensure_annotations
    def assemble_import_tree(path: str) -> Node:
        '''
        Assemble a bookmark tree structure from `Bookmarks` file to be able
        to either display or correctly import/merge the structure into
        internal bookmarks database.
        '''
        with open(path, 'rb') as fbookmark:
            raw = json.loads(fbookmark.read().decode('utf-8'))

        trees = []
        if 'bookmark_bar' in raw['roots']:
            folder_items = ChromeImporter.walk_folders(
                raw['roots']['bookmark_bar'], 0
            )
            trees.append(
                assemble_folder_tree(
                    items=folder_items,
                    key='parent_folder_id',
                    node_type=Folder
                )
            )
        if 'custom_root' in raw['roots']:
            raw_custom_sorted = sorted(
                raw['roots']['custom_root'].items(),
                key=lambda item: item[0]
            )
            for _, value in raw_custom_sorted:
                folder_items = ChromeImporter.walk_folders(value, 0)
                trees.append(
                    assemble_folder_tree(
                        items=folder_items,
                        key='parent_folder_id',
                        node_type=Folder
                    )
                )
        if 'other' in raw['roots']:
            folder_items = ChromeImporter.walk_folders(
                raw['roots']['other'], 0
            )
            trees.append(
                assemble_folder_tree(
                    items=folder_items,
                    key='parent_folder_id',
                    node_type=Folder
                )
            )
        if 'synced' in raw['roots']:
            folder_items = ChromeImporter.walk_folders(
                raw['roots']['synced'], 0
            )
            trees.append(
                assemble_folder_tree(
                    items=folder_items,
                    key='parent_folder_id',
                    node_type=Folder
                )
            )

        # printable folder tree
        folder_tree = Node(
            name=0,
            node_type=Folder,
            id=0,
            folder_name='<no title>',
            parent_folder_id=None,
            item={}
        )
        for tree in trees:
            tree.parent = folder_tree
            tree.parent_folder_id = folder_tree.id  # pylint: disable=no-member

        bookmarks = []
        for folder in traverse(folder_tree):
            bookmarks += ChromeImporter.walk_bookmarks(folder.item, folder.id)
            delattr(folder, 'item')

        # printable folder+bookmark tree
        bookmark_tree = assemble_bookmark_tree(
            items=bookmarks,
            key='folder_id',
            folder_tree_root=folder_tree,
            node_type=Bookmark
        )
        return bookmark_tree
