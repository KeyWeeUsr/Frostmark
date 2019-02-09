'''
Test for exporting bookmarks to various browsers' formats.
'''
import unittest
from unittest.mock import patch, MagicMock
from os import listdir, remove
from os.path import join, abspath, dirname
from io import BytesIO


class ExportTestCase(unittest.TestCase):
    '''
    TestCase for exporting bookmarks to various formats.
    '''

    def test_export_firefox(self):
        '''
        Test exporting HTML file from internal DB.
        '''

        from frostmark import db_base
        from frostmark import user_data
        from frostmark.importer import Importer
        from frostmark.exporter import Exporter

        expected = (
            '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n'
            '<!-- This is an automatically generated file.\n'
            '    It will be read and overwritten.\n'
            '    DO NOT EDIT!\n'
            '-->\n'
            '<META\n'
            '    HTTP-EQUIV="Content-Type"\n'
            '    CONTENT="text/html; charset=UTF-8"\n'
            '/>\n'
            '<TITLE>Bookmarks</TITLE>\n'
            '<H1>Bookmarks</H1>\n'
            '<DL><p>\n'
            '    <DT><H3><no title></H3>\n'
            '    <DL><p>\n'
            '        <DT><H3>Bookmarks Menu</H3>\n'
            '        <DL><p>\n'
            '            <DT><H3>Mozilla Firefox</H3>\n'
            '            <DL><p>\n'
            '                <DT><A HREF="http://www.mozilla.com/en-US/firefox'
            '/help/" ICON="">Help and Tutorials</A>\n'
            '                <DT><A HREF="http://www.mozilla.com/en-US/firefox'
            '/customize/" ICON="">Customize Firefox</A>\n'
            '                <DT><A HREF="http://www.mozilla.com/en-US/firefox'
            '/community/" ICON="">Get Involved</A>\n'
            '                <DT><A HREF="http://www.mozilla.com/en-US/about/"'
            ' ICON="">About Us</A>\n'
            '            </DL><p>\n'
            '            <HR>\n'
            '            <DT><A HREF="http://portableapps.com/" ICON="">'
            'PortableApps.com</A>\n'
            '            <DT><A HREF="place:folder=BOOKMARKS_MENU&folder='
            'UNFILED_BOOKMARKS&folder=TOOLBAR&queryType=1&sort=12&maxResults='
            '10&excludeQueries=1" ICON="">Recently Bookmarked</A>\n'
            '            <DT><A HREF="place:type=6&sort=14&maxResults=10" '
            'ICON="">Recent Tags</A>\n'
            '        </DL><p>\n'
            '        <DT><H3>Bookmarks Toolbar</H3>\n'
            '        <DL><p>\n'
            '            <DT><H3>Latest Headlines</H3>\n'
            '            <DL><p>\n'
            '            </DL><p>\n'
            '            <DT><A HREF="http://www.mozilla.com/en-US/firefox/'
            'central/" ICON="">Getting Started</A>\n'
            '            <DT><A HREF="place:sort=8&maxResults=10" ICON="">'
            'Most Visited</A>\n'
            '        </DL><p>\n'
            '        <DT><H3>Tags</H3>\n'
            '        <DL><p>\n'
            '        </DL><p>\n'
            '        <DT><H3>Unsorted Bookmarks</H3>\n'
            '        <DL><p>\n'
            '        </DL><p>\n'
            '    </DL><p>\n'
            '</DL><p>\n'
        )
        folder = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(folder))

        # import bookmarks from sample firefox database
        Importer('firefox').import_from(join(
            dirname(abspath(__file__)),
            'sample_firefox.sqlite'
        ))
        self.assertIn(db_base.DB_NAME, listdir(folder))

        # file-like object to catch HTML output
        bytesout = BytesIO()

        # mock context manager to return BytesIO
        mocked_file = MagicMock(__enter__=MagicMock(return_value=bytesout))

        # mock builtins.open() to return mocked_file
        mocked_open = MagicMock(return_value=mocked_file)
        with patch('builtins.open', new=mocked_open) as output:
            # export HTML to "out.html" file
            Exporter.export_to(join(folder, 'out.html'))

            # "file" was created and written to
            output.assert_called_once_with(join(folder, 'out.html'), 'rb')

            # rewind and compare
            bytesout.seek(0)
            self.assertEqual(bytesout.read().decode('utf-8'), expected)

        # remove internal DB
        remove(join(folder, db_base.DB_NAME))
