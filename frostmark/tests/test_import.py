'''
Test for importing bookmarks from various browsers.
'''
import unittest
from unittest.mock import patch
from os import listdir, remove
from os.path import join, abspath, dirname


class ImportTestCase(unittest.TestCase):
    '''
    TestCase for importing bookmarks from various browsers.
    '''

    def test_pull_firefox(self):
        '''
        Test fetching Firefox profiles from places.sqlite.
        '''

        from anytree import Node
        from frostmark.common import traverse
        from frostmark.models import Folder, Bookmark
        from frostmark.importer import Importer
        from frostmark.importer.firefox import FirefoxImporter

        sample = join(
            dirname(abspath(__file__)),
            'sample_firefox.sqlite'
        )

        # pylint: disable=protected-access
        session = Importer._path_session(sample, FirefoxImporter.BASE)
        tree = FirefoxImporter.assemble_import_tree(session)
        flat_tree = traverse(tree)

        self.assertIsInstance(tree, Node)

        self.maxDiff = None  # pylint: disable=invalid-name
        self.assertEqual([
            (item.folder_name, item.node_type)

            if item.node_type == Folder
            else (item.title, item.node_type)

            for item in flat_tree
        ], [
            ('<no title>', Folder),
            ('Bookmarks Menu', Folder),
            ('Mozilla Firefox', Folder),
            ('Help and Tutorials', Bookmark),
            ('Customize Firefox', Bookmark),
            ('Get Involved', Bookmark),
            ('About Us', Bookmark),
            ('PortableApps.com', Bookmark),
            ('Recently Bookmarked', Bookmark),
            ('Recent Tags', Bookmark),
            ('Bookmarks Toolbar', Folder),
            ('Latest Headlines', Folder),
            ('Getting Started', Bookmark),
            ('Most Visited', Bookmark),
            ('Tags', Folder),
            ('Unsorted Bookmarks', Folder)
        ])

    def test_import_firefox(self):
        '''
        Test importing bookmark tree into internal DB.
        '''

        from frostmark import db_base
        from frostmark import user_data
        from frostmark.common import fetch_bookmark_tree, print_bookmark_tree
        from frostmark.importer import Importer

        urls = [
            'http://www.mozilla.com/en-US/firefox/help/',
            'http://www.mozilla.com/en-US/firefox/customize/',
            'http://www.mozilla.com/en-US/firefox/community/',
            'http://www.mozilla.com/en-US/about/',
            'http://portableapps.com/', (
                'place:folder=BOOKMARKS_MENU&folder=UNFILED_BOOKMARKS'
                '&folder=TOOLBAR&queryType=1&sort=12&maxResults=10'
                '&excludeQueries=1'
            ),
            'place:type=6&sort=14&maxResults=10',
            'http://www.mozilla.com/en-US/firefox/central/',
            'place:sort=8&maxResults=10'
        ]
        expected_calls = [
            f'[F] ROOT',
            f'+-- [F] <no title>',
            f'    |-- [F] Bookmarks Menu',
            f'    |   |-- [F] Mozilla Firefox',
            f'    |   |   |-- [B] Help and Tutorials {urls[0]}',
            f'    |   |   |-- [B] Customize Firefox {urls[1]}',
            f'    |   |   |-- [B] Get Involved {urls[2]}',
            f'    |   |   +-- [B] About Us {urls[3]}',
            f'    |   |-- [B] PortableApps.com {urls[4]}',
            f'    |   |-- [B] Recently Bookmarked {urls[5]}',
            f'    |   +-- [B] Recent Tags {urls[6]}',
            f'    |-- [F] Bookmarks Toolbar',
            f'    |   |-- [F] Latest Headlines',
            f'    |   |-- [B] Getting Started {urls[7]}',
            f'    |   +-- [B] Most Visited {urls[8]}',
            f'    |-- [F] Tags',
            f'    +-- [F] Unsorted Bookmarks'
        ]

        folder = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(folder))

        # import bookmarks from sample firefox database
        Importer('firefox').import_from(join(
            dirname(abspath(__file__)),
            'sample_firefox.sqlite'
        ))
        self.assertIn(db_base.DB_NAME, listdir(folder))

        # fetch bookmarks from internal db and test the console output
        with patch('builtins.print') as output:
            print_bookmark_tree(fetch_bookmark_tree())

        for idx, item in enumerate(output.call_args_list):
            args, _ = item
            self.assertEqual(args[0], expected_calls[idx])
        self.assertEqual(len(output.call_args_list), len(expected_calls))

        # remove internal DB
        remove(join(folder, db_base.DB_NAME))
