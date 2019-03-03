# -*- coding: utf-8 -*-
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
            f'[F] 0\tROOT',
            f'+-- [F] 1\t<no title>',
            f'    |-- [F] 2\tBookmarks Menu',
            f'    |   |-- [F] 6\tMozilla Firefox',
            f'    |   |   |-- [B] 2\tHelp and Tutorials {urls[0]}',
            f'    |   |   |-- [B] 3\tCustomize Firefox {urls[1]}',
            f'    |   |   |-- [B] 4\tGet Involved {urls[2]}',
            f'    |   |   +-- [B] 5\tAbout Us {urls[3]}',
            f'    |   |-- [B] 6\tPortableApps.com {urls[4]}',
            f'    |   |-- [B] 8\tRecently Bookmarked {urls[5]}',
            f'    |   +-- [B] 9\tRecent Tags {urls[6]}',
            f'    |-- [F] 3\tBookmarks Toolbar',
            f'    |   |-- [F] 7\tLatest Headlines',
            f'    |   |-- [B] 1\tGetting Started {urls[7]}',
            f'    |   +-- [B] 7\tMost Visited {urls[8]}',
            f'    |-- [F] 4\tTags',
            f'    +-- [F] 5\tUnsorted Bookmarks'
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

    def test_pull_opera(self):
        '''
        Test fetching Opera profile.
        '''

        from anytree import Node
        from frostmark.common import traverse
        from frostmark.models import Folder, Bookmark
        from frostmark.importer.opera import OperaImporter

        sample = join(
            dirname(abspath(__file__)),
            'sample_opera.json'
        )

        # pylint: disable=protected-access
        tree = OperaImporter.assemble_import_tree(sample)
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
            ('Bookmarks bar', Folder),
            ('PortableApps.com', Bookmark),
            ('Shared Bookmarks', Folder),
            ('Speed Dial', Folder),
            ('V7', Folder),
            ('', Folder),
            ('Let\'s connect', Bookmark),
            ('Booking.com: Cheap Hotels', Bookmark),
            ('Wikipedia', Bookmark),
            ('', Folder),
            ('Spojte sa s nami', Bookmark),
            ('Zoznam', Bookmark),
            ('Facebook', Bookmark),
            ('Amazon.com', Bookmark),
            ('eBay', Bookmark),
            ('Yahoo!', Bookmark),
            ('Twitter', Bookmark),
            ('YouTube', Bookmark),
            ('Mall', Bookmark),
            ('Heureka', Bookmark),
            ('Topky', Bookmark),
            ('Amazon.de', Bookmark),
            ('Azet', Bookmark),
            ('Trash', Folder),
            ('Unsorted Bookmarks', Folder),
            ('My Folders', Folder),
            ('Other bookmarks', Folder),
            ('Mobile bookmarks', Folder)
        ])

    def test_import_opera(self):
        '''
        Test importing bookmark tree into internal DB.
        '''

        from frostmark import db_base
        from frostmark import user_data
        from frostmark.common import fetch_bookmark_tree, print_bookmark_tree
        from frostmark.importer import Importer

        urls = [
            'http://portableapps.com/',
            'http://www.opera.com/follow',
            'http://www.booking.com/',
            'http://en.wikipedia.org/',
            'http://www.opera.com/sk/follow',
            'http://www.zoznam.sk/',
            'http://www.facebook.com/',
            'http://www.amazon.com/',
            'http://www.ebay.com/',
            'http://www.yahoo.com/',
            'http://www.twitter.com/',
            'http://www.youtube.com/',
            'http://www.mall.sk/',
            'http://www.heureka.sk/',
            'http://www.topky.sk/',
            'http://www.amazon.de/',
            'http://www.azet.sk/'
        ]
        expected_calls = [
            f'[F] 0\tROOT',
            f'|-- [F] 1\t<no title>',
            f'|-- [F] 2\tBookmarks bar',
            f'|   +-- [B] 1\tPortableApps.com {urls[0]}',
            f'|-- [F] 3\tShared Bookmarks',
            f'|-- [F] 4\tSpeed Dial',
            f'|   +-- [F] 10\tV7',
            f'|       |-- [F] 11\t',
            f'|       |   |-- [B] 8\tLet\'s connect {urls[1]}',
            f'|       |   |-- [B] 9\tBooking.com: Cheap Hotels {urls[2]}',
            f'|       |   +-- [B] 10\tWikipedia {urls[3]}',
            f'|       |-- [F] 12\t',
            f'|       |   |-- [B] 16\tSpojte sa s nami {urls[4]}',
            f'|       |   +-- [B] 17\tZoznam {urls[5]}',
            f'|       |-- [B] 2\tFacebook {urls[6]}',
            f'|       |-- [B] 3\tAmazon.com {urls[7]}',
            f'|       |-- [B] 4\teBay {urls[8]}',
            f'|       |-- [B] 5\tYahoo! {urls[9]}',
            f'|       |-- [B] 6\tTwitter {urls[10]}',
            f'|       |-- [B] 7\tYouTube {urls[11]}',
            f'|       |-- [B] 11\tMall {urls[12]}',
            f'|       |-- [B] 12\tHeureka {urls[13]}',
            f'|       |-- [B] 13\tTopky {urls[14]}',
            f'|       |-- [B] 14\tAmazon.de {urls[15]}',
            f'|       +-- [B] 15\tAzet {urls[16]}',
            f'|-- [F] 5\tTrash',
            f'|-- [F] 6\tUnsorted Bookmarks',
            f'|-- [F] 7\tMy Folders',
            f'|-- [F] 8\tOther bookmarks',
            f'+-- [F] 9\tMobile bookmarks'
        ]

        folder = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(folder))

        # import bookmarks from sample firefox database
        Importer('opera').import_from(join(
            dirname(abspath(__file__)),
            'sample_opera.json'
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

    def test_pull_chrome(self):
        '''
        Test fetching Chrome profile.
        '''

        from anytree import Node
        from frostmark.common import traverse
        from frostmark.models import Folder, Bookmark
        from frostmark.importer.chrome import ChromeImporter

        sample = join(
            dirname(abspath(__file__)),
            'sample_chrome.json'
        )

        # pylint: disable=protected-access
        tree = ChromeImporter.assemble_import_tree(sample)
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
            ('Panel so záložkami', Folder),
            ('folder', Folder),
            ('nestedfolder', Folder),
            ('YouTube', Bookmark),
            ('emptyfolder', Folder),
            ('Google', Bookmark),
            ('PortableApps.com', Bookmark),
            ('Ostatné', Folder),
            ('Mapy Google', Bookmark),
            ('Záložky v mobile', Folder)
        ])

    def test_import_chrome(self):
        '''
        Test importing bookmark tree into internal DB.
        '''

        from frostmark import db_base
        from frostmark import user_data
        from frostmark.common import fetch_bookmark_tree, print_bookmark_tree
        from frostmark.importer import Importer

        urls = [
            'https://www.youtube.com/',
            'https://www.google.com/',
            'http://portableapps.com/',
            'https://www.google.com/maps'
        ]
        expected_calls = [
            f'[F] 0\tROOT',
            f'|-- [F] 1\t<no title>',
            f'|-- [F] 2\tPanel so záložkami',
            f'|   |-- [F] 5\tfolder',
            f'|   |   |-- [F] 6\tnestedfolder',
            f'|   |   |   +-- [B] 3\tYouTube {urls[0]}',
            f'|   |   |-- [F] 7\temptyfolder',
            f'|   |   +-- [B] 2\tGoogle {urls[1]}',
            f'|   +-- [B] 1\tPortableApps.com {urls[2]}',
            f'|-- [F] 3\tOstatné',
            f'|   +-- [B] 4\tMapy Google {urls[3]}',
            f'+-- [F] 4\tZáložky v mobile'
        ]

        folder = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(folder))

        # import bookmarks from sample firefox database
        Importer('chrome').import_from(join(
            dirname(abspath(__file__)),
            'sample_chrome.json'
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
