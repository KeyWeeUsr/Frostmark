'''
Test for retrieving various browser profile locations.
'''
import unittest
from unittest.mock import patch, call
from os.path import basename, dirname, join


class ProfileTestCase(unittest.TestCase):
    '''
    TestCase for various browser profile locations.
    '''

    def test_profile_firefox_win(self):
        '''
        Test fetching Firefox profiles on Windows.
        '''

        from frostmark.profiles import get_profiles
        found_profiles = ['profile1.default', 'profile2.default']
        expected_files = [
            join('profile1.default', 'places.sqlite'),
            join('profile2.default', 'places.sqlite')
        ]
        exi = patch('frostmark.profiles.exists')
        platform = patch('sys.platform', 'win32')
        listdir = patch(
            'frostmark.profiles.listdir',
            return_value=found_profiles
        )

        # with APPDATA
        env = patch('frostmark.profiles.environ', {
            'APPDATA': 'dummy'
        })
        with exi, platform, listdir, env:
            self.assertEqual([
                join(basename(dirname(item)), basename(item))
                for item in get_profiles('firefox')
            ], expected_files)

        # without APPDATA
        env = patch('frostmark.profiles.environ', {})
        with exi, platform, listdir, env:
            self.assertEqual([
                join(basename(dirname(item)), basename(item))
                for item in get_profiles('firefox')
            ], expected_files)

    def test_profile_firefox_macos(self):
        '''
        Test fetching Firefox profiles on macOS.
        '''

        from frostmark.profiles import get_profiles
        found_profiles = ['profile1.default', 'profile2.default']
        expected_files = [
            join('profile1.default', 'places.sqlite'),
            join('profile2.default', 'places.sqlite')
        ]
        exi = patch('frostmark.profiles.exists')
        platform = patch('sys.platform', 'darwin')
        listdir = patch(
            'frostmark.profiles.listdir',
            return_value=found_profiles
        )

        with exi, platform, listdir:
            self.assertEqual([
                join(basename(dirname(item)), basename(item))
                for item in get_profiles('firefox')
            ], expected_files)

    def test_profile_firefox_linux(self):
        '''
        Test fetching Firefox profiles on GNU/Linux distros.
        '''

        from frostmark.profiles import get_profiles
        found_profiles = ['profile1.default', 'profile2.default']
        expected_files = [
            join('profile1.default', 'places.sqlite'),
            join('profile2.default', 'places.sqlite')
        ]
        exi = patch('frostmark.profiles.exists')
        platform = patch('sys.platform', 'linux')
        listdir = patch(
            'frostmark.profiles.listdir',
            return_value=found_profiles
        )

        with exi, platform, listdir:
            self.assertEqual([
                join(basename(dirname(item)), basename(item))
                for item in get_profiles('firefox')
            ], expected_files)

    def test_profile_opera_win(self):
        '''
        Test fetching Opera profiles on Windows.
        '''

        from frostmark.profiles import get_profiles
        found_profiles = ['Opera stable']
        expected_files = [
            join('Opera stable', 'Bookmarks')
        ]
        exi = patch('frostmark.profiles.exists')
        platform = patch('sys.platform', 'win32')
        listdir = patch(
            'frostmark.profiles.listdir',
            return_value=found_profiles
        )

        # with APPDATA
        env = patch('frostmark.profiles.environ', {
            'APPDATA': 'dummy'
        })
        with exi, platform, listdir, env:
            self.assertEqual([
                join(basename(dirname(item)), basename(item))
                for item in get_profiles('opera')
            ], expected_files)

        # without APPDATA
        env = patch('frostmark.profiles.environ', {})
        with exi, platform, listdir, env:
            self.assertEqual([
                join(basename(dirname(item)), basename(item))
                for item in get_profiles('opera')
            ], expected_files)

    def test_profile_unsupported_browser(self):
        '''
        Test fetching profiles for an unsupported browser.
        '''

        from frostmark.profiles import get_profiles
        self.assertEqual(get_profiles('not_supported'), [])

    def test_profile_all_browsers(self):
        '''
        Test fetching all profiles.
        '''

        from frostmark.profiles import get_all_profiles, SUPPORTED_BROWSERS
        with patch('frostmark.profiles.get_profiles') as gprof:
            get_all_profiles()
            self.assertEqual(
                gprof.call_args_list,
                [call(b) for b in SUPPORTED_BROWSERS]
            )

    @staticmethod
    def test_profile_print():
        '''
        Test printing profiles for a browser.
        '''

        from frostmark.profiles import print_profiles
        expected = 'dummy'
        profiles = patch(
            'frostmark.profiles.get_profiles',
            return_value=[expected]
        )
        with profiles, patch('builtins.print') as output:
            print_profiles('')
            output.assert_called_once_with(expected)

    def test_profile_print_all(self):
        '''
        Test printing profiles for all browsers.
        '''

        from frostmark.profiles import print_all_profiles
        expected = {'a': ['1', '2'], 'b': ['3', '4']}
        profiles = patch(
            'frostmark.profiles.get_all_profiles',
            return_value=expected
        )
        with profiles, patch('builtins.print') as output:
            print_all_profiles()

            # access call argument
            # call('a') -> ('a', ) -> 'a'
            self.assertIn(output.call_args_list[0][0][0], expected.keys())
            self.assertIn(output.call_args_list[3][0][0], expected.keys())

            # append \t prefix
            expected = {
                key: [
                    f'\t{item}'
                    for item in value
                ]
                for key, value in expected.items()
            }
            # [call('\t1'), ...] -> [('\t1', ), ...] -> ['\t1', ...]
            self.assertIn(
                [cll[0][0] for cll in output.call_args_list[1:3]],
                expected.values()
            )
            self.assertIn(
                [cll[0][0] for cll in output.call_args_list[4:6]],
                expected.values()
            )

    @staticmethod
    def test_profile_print_all_empty():
        '''
        Test printing empty profiles.
        '''

        from frostmark.profiles import print_all_profiles
        profiles = patch(
            'frostmark.profiles.get_all_profiles',
            return_value={'empty_profiles': []}
        )
        with profiles, patch('builtins.print') as output:
            print_all_profiles()
            output.assert_not_called()
