'''
Test for importing bookmarks from various browsers.
'''
import unittest
from os.path import join, abspath, dirname


class ImportTestCase(unittest.TestCase):
    '''
    TestCase for importing bookmarks from various browsers.
    '''

    def test_import_firefox(self):
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
