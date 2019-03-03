'''
Test for creating folder and bookmark trees.
'''
import unittest
from unittest.mock import patch


class TreeTestCase(unittest.TestCase):
    '''
    TestCase for common tree assembling functionality.
    '''

    FOLDER_DATA = [{
        'id': 0,
        'parent_folder_id': None,
        'folder_name': 'ROOT'
    }, {
        'id': 1,
        'parent_folder_id': 0,
        'folder_name': 'one'
    }, {
        'id': 2,
        'parent_folder_id': 1,
        'folder_name': 'two'
    }, {
        'id': 3,
        'parent_folder_id': 1,
        'folder_name': 'three'
    }, {
        'id': 4,
        'parent_folder_id': 0,
        'folder_name': 'four'
    }, {
        'id': 5,
        'parent_folder_id': 0,
        'folder_name': 'five'
    }, {
        'id': 6,
        'parent_folder_id': 5,
        'folder_name': 'six'
    }, {
        'id': 7,
        'parent_folder_id': 6,
        'folder_name': 'seven'
    }]

    BOOKMARK_DATA = [{
        'id': 1,
        'title': 'a',
        'folder_id': 0,
        'url': '<url>'
    }, {
        'id': 2,
        'title': 'b',
        'folder_id': 0,
        'url': '<url>'
    }, {
        'id': 3,
        'title': 'c',
        'folder_id': 0,
        'url': '<url>'
    }, {
        'id': 4,
        'title': 'd',
        'folder_id': 1,
        'url': '<url>'
    }, {
        'id': 5,
        'title': 'e',
        'folder_id': 1,
        'url': '<url>'
    }, {
        'id': 6,
        'title': 'f',
        'folder_id': 1,
        'url': '<url>'
    }, {
        'id': 7,
        'title': 'g',
        'folder_id': 2,
        'url': '<url>'
    }, {
        'id': 8,
        'title': 'h',
        'folder_id': 3,
        'url': '<url>'
    }, {
        'id': 9,
        'title': 'i',
        'folder_id': 3,
        'url': '<url>'
    }, {
        'id': 10,
        'title': 'j',
        'folder_id': 3,
        'url': '<url>'
    }, {
        'id': 11,
        'title': 'k',
        'folder_id': 4,
        'url': '<url>'
    }, {
        'id': 12,
        'title': 'l',
        'folder_id': 5,
        'url': '<url>'
    }, {
        'id': 13,
        'title': 'm',
        'folder_id': 6,
        'url': '<url>'
    }, {
        'id': 14,
        'title': 'n',
        'folder_id': 7,
        'url': '<url>'
    }]

    def test_tree_folder(self):
        '''
        Test creating folder tree both nested and flat.
        '''

        from anytree import Node
        from frostmark.common import assemble_folder_tree, traverse
        from frostmark.models import Folder

        tree = assemble_folder_tree(
            items=self.FOLDER_DATA,
            key='parent_folder_id',
            node_type=Folder
        )
        flat_tree = traverse(tree)

        self.assertIsInstance(tree, Node)
        self.assertEqual(tree.id, 0)

        # unfold the same way each branch is build from the root
        # to the last child when assembling i.e. sorted and top-down
        #
        # 0
        # |-1
        # | |-2
        # | |-3
        # |
        # |-4
        # |
        # |-5
        #   |-6
        #     |-7
        self.assertEqual(
            [item.id for item in flat_tree],
            list(range(len(self.FOLDER_DATA)))
        )

        for item in flat_tree:
            self.assertEqual(item.node_type, Folder)

    def test_tree_folder_print(self):
        '''
        Test printing folder tree.
        '''

        from frostmark.common import assemble_folder_tree, print_bookmark_tree
        from frostmark.models import Folder

        expected_calls = [
            '[F] 0\tROOT',
            '|-- [F] 1\tone',
            '|   |-- [F] 2\ttwo',
            '|   +-- [F] 3\tthree',
            '|-- [F] 4\tfour',
            '+-- [F] 5\tfive',
            '    +-- [F] 6\tsix',
            '        +-- [F] 7\tseven',
        ]
        tree = assemble_folder_tree(
            items=self.FOLDER_DATA,
            key='parent_folder_id',
            node_type=Folder
        )
        with patch('builtins.print') as output:
            print_bookmark_tree(tree)

        self.assertEqual(len(output.call_args_list), len(expected_calls))
        for idx, item in enumerate(output.call_args_list):
            args, _ = item
            self.assertEqual(args[0], expected_calls[idx])

    def test_tree_bookmark(self):
        '''
        Test creating folder + bookmark tree both nested and flat.
        '''

        from anytree import Node
        from frostmark.common import (
            assemble_folder_tree,
            assemble_bookmark_tree,
            traverse
        )
        from frostmark.models import Folder, Bookmark

        folder_tree = assemble_folder_tree(
            items=self.FOLDER_DATA,
            key='parent_folder_id',
            node_type=Folder
        )
        tree = assemble_bookmark_tree(
            items=self.BOOKMARK_DATA,
            key='folder_id',
            folder_tree_root=folder_tree,
            node_type=Bookmark
        )

        flat_tree = traverse(tree)

        self.assertIsInstance(tree, Node)
        self.assertEqual(tree.id, 0)

        # unfold the same way each as with folders, but make sure bookmarks
        # are appended at the end of the Node children
        #
        # 0
        # |-1
        # | |-2
        # | | |-b7
        # | |
        # | |-3
        # | | |-b8
        # | | |-b9
        # | | |-b10
        # | |
        # | |-b4
        # | |-b5
        # | |-b6
        # |
        # |-4
        # | |-b11
        # |
        # |-5
        # | |-6
        # | | |-7
        # | | | |-b14
        # | | |
        # | | |-b13
        # | |
        # | |-b12
        # |
        # |-b1
        # |-b2
        # |-b3
        self.assertEqual([
            item.id
            for item in flat_tree
        ], [
            0, 1, 2, 7, 3, 8, 9, 10,
            4, 5, 6, 4, 11, 5, 6, 7,
            14, 13, 12, 1, 2, 3
        ])

        for item in flat_tree:
            if 'folder_name' in vars(item):
                self.assertEqual(item.node_type, Folder)
            else:
                self.assertEqual(item.node_type, Bookmark)

    def test_tree_bookmark_print(self):
        '''
        Test printing folder + bookmark tree.
        '''

        from frostmark.common import (
            assemble_folder_tree,
            assemble_bookmark_tree,
            print_bookmark_tree
        )
        from frostmark.models import Folder, Bookmark

        expected_calls = [
            '[F] 0\tROOT',
            '|-- [F] 1\tone',
            '|   |-- [F] 2\ttwo',
            '|   |   +-- [B] 7\tg <url>',
            '|   |-- [F] 3\tthree',
            '|   |   |-- [B] 8\th <url>',
            '|   |   |-- [B] 9\ti <url>',
            '|   |   +-- [B] 10\tj <url>',
            '|   |-- [B] 4\td <url>',
            '|   |-- [B] 5\te <url>',
            '|   +-- [B] 6\tf <url>',
            '|-- [F] 4\tfour',
            '|   +-- [B] 11\tk <url>',
            '|-- [F] 5\tfive',
            '|   |-- [F] 6\tsix',
            '|   |   |-- [F] 7\tseven',
            '|   |   |   +-- [B] 14\tn <url>',
            '|   |   +-- [B] 13\tm <url>',
            '|   +-- [B] 12\tl <url>',
            '|-- [B] 1\ta <url>',
            '|-- [B] 2\tb <url>',
            '+-- [B] 3\tc <url>',
        ]
        folder_tree = assemble_folder_tree(
            items=self.FOLDER_DATA,
            key='parent_folder_id',
            node_type=Folder
        )
        tree = assemble_bookmark_tree(
            items=self.BOOKMARK_DATA,
            key='folder_id',
            folder_tree_root=folder_tree,
            node_type=Bookmark
        )

        with patch('builtins.print') as output:
            print_bookmark_tree(tree)

        for idx, item in enumerate(output.call_args_list):
            args, _ = item
            self.assertEqual(args[0], expected_calls[idx])
        self.assertEqual(len(output.call_args_list), len(expected_calls))
