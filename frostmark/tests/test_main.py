'''
Test for command-line args parsing.
'''
import unittest
from unittest.mock import patch, MagicMock


class MainTestCase(unittest.TestCase):
    '''
    TestCase for various command-line arguments.
    '''

    def test_main_noargs(self):
        '''
        Test no input args.
        '''

        with patch('sys.stdout'), patch('sys.argv', []):
            with self.assertRaises(SystemExit):
                from frostmark.__main__ import main
                main('__main__')

    def test_main_emptystr(self):
        '''
        Test no input args as a list of empty string.
        '''

        with patch('sys.stdout'), patch('sys.argv', ['']):
            with self.assertRaises(SystemExit):
                from frostmark.__main__ import main
                main('__main__')

    def test_main_notimplemented(self):
        '''
        Test invalid input args.
        '''

        args = [__file__, 'notimplemented']
        with patch('sys.stderr'), patch('sys.argv', args):
            with self.assertRaises(SystemExit):
                from frostmark.__main__ import main
                main('__main__')

    @staticmethod
    def test_main_console():
        '''
        Test triggering console mode.
        '''

        with patch('sys.stdout'), patch('sys.argv', [__file__, 'console']):
            from frostmark.__main__ import main
            main('__main__')

    @staticmethod
    def test_main_gui():
        '''
        Test triggering gui mode.
        '''

        stdout = patch('sys.stdout')
        argv = patch('sys.argv', [__file__, 'gui'])
        with stdout, argv, patch('frostmark.core.gui.react_main') as react:
            from frostmark.__main__ import main
            main('__main__')
            react.assert_called_once_with()

    def test_main_console_export(self):
        '''
        Test exporting from console mode.
        '''

        args = [__file__, 'console', '-x', 'PATH']
        export_to = MagicMock()
        export_patch = patch(
            target='frostmark.exporter.Exporter.export_to',
            new=export_to
        )
        with patch('sys.stdout'), patch('sys.argv', args), export_patch:
            # not implemented yet, GUI is None
            from frostmark.__main__ import main
            with self.assertRaises(SystemExit):
                main('__main__')
            export_to.assert_called_once_with(path='PATH')

    def test_main_console_changeparentfolder(self):
        '''
        Test changing parent for folder from console.
        '''

        args = [
            __file__, 'console', '--change-parent-folder',
            '123', '456'
        ]
        cpf = MagicMock()
        cpf_patch = patch(
            target='frostmark.editor.Editor.change_parent_folder',
            new=cpf
        )
        with patch('sys.stdout'), patch('sys.argv', args), cpf_patch:
            # not implemented yet, GUI is None
            from frostmark.__main__ import main
            with self.assertRaises(SystemExit):
                main('__main__')
            cpf.assert_called_once_with(
                folder_id=123,
                parent_id=456
            )

    def test_main_console_changeparentbookmark(self):
        '''
        Test changing parent for bookmark from console.
        '''

        args = [
            __file__, 'console', '--change-parent-bookmark',
            '123', '456'
        ]
        cpb = MagicMock()
        cpb_patch = patch(
            target='frostmark.editor.Editor.change_parent_bookmark',
            new=cpb
        )
        with patch('sys.stdout'), patch('sys.argv', args), cpb_patch:
            # not implemented yet, GUI is None
            from frostmark.__main__ import main
            with self.assertRaises(SystemExit):
                main('__main__')
            cpb.assert_called_once_with(
                bookmark_id=123,
                parent_id=456
            )

    def test_main_console_renamefolder(self):
        '''
        Test changing folder_name for folder from console.
        '''

        args = [
            __file__, 'console', '--rename-folder',
            '123', '456'
        ]
        rename = MagicMock()
        rename_patch = patch(
            target='frostmark.editor.Editor.rename_folder',
            new=rename
        )
        with patch('sys.stdout'), patch('sys.argv', args), rename_patch:
            # not implemented yet, GUI is None
            from frostmark.__main__ import main
            with self.assertRaises(SystemExit):
                main('__main__')
            rename.assert_called_once_with(
                folder_id=123,
                name='456'
            )

    def test_main_console_renamebookmark(self):
        '''
        Test changing title for bookmark from console.
        '''

        args = [
            __file__, 'console', '--rename-bookmark',
            '123', '456'
        ]
        rename = MagicMock()
        rename_patch = patch(
            target='frostmark.editor.Editor.rename_bookmark',
            new=rename
        )
        with patch('sys.stdout'), patch('sys.argv', args), rename_patch:
            # not implemented yet, GUI is None
            from frostmark.__main__ import main
            with self.assertRaises(SystemExit):
                main('__main__')
            rename.assert_called_once_with(
                bookmark_id=123,
                name='456'
            )

    def test_main_console_changebookmarkurl(self):
        '''
        Test changing url for bookmark from console.
        '''

        args = [
            __file__, 'console', '--change-bookmark-url',
            '123', 'http://456'
        ]
        cbu = MagicMock()
        cbu_patch = patch(
            target='frostmark.editor.Editor.change_bookmark_url',
            new=cbu
        )
        with patch('sys.stdout'), patch('sys.argv', args), cbu_patch:
            # not implemented yet, GUI is None
            from frostmark.__main__ import main
            with self.assertRaises(SystemExit):
                main('__main__')
            cbu.assert_called_once_with(
                bookmark_id=123,
                url='http://456'
            )
