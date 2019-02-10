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

    def test_main_gui(self):
        '''
        Test triggering gui mode.
        '''

        with patch('sys.stdout'), patch('sys.argv', [__file__, 'gui']):
            with self.assertRaises(NotImplementedError):
                from frostmark.__main__ import main
                main('__main__')

    def test_main_console_export(self):
        '''
        Test exporting from console mode.
        '''

        args = [__file__, 'console', '-e', 'PATH']
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
            export_to.assert_called_once_with('PATH')
