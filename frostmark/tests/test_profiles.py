'''
Test for retrieving various browser profile locations.
'''
import unittest
from unittest.mock import patch
from os.path import basename


class ProfileTestCase(unittest.TestCase):
    '''
    TestCase for various browser profile locations.
    '''

    def test_profile_firefox_win(self):
        '''
        Test fetching Firefox profiles on Windows.
        '''

        from frostmark.profiles import get_profiles
        expected_profiles = ['1.default', '2.default']
        platform = patch('sys.platform', 'win32')
        listdir = patch(
            'frostmark.profiles.listdir',
            return_value=expected_profiles
        )

        # with APPDATA
        with platform, listdir:
            self.assertEqual(
                [basename(path) for path in get_profiles('firefox')],
                expected_profiles
            )

        # without APPDATA
        env = patch('frostmark.profiles.environ', {})
        with platform, listdir, env:
            self.assertEqual(
                [basename(path) for path in get_profiles('firefox')],
                expected_profiles
            )

    def test_profile_firefox_macos(self):
        '''
        Test fetching Firefox profiles on macOS.
        '''

        from frostmark.profiles import get_profiles
        expected_profiles = ['1.default', '2.default']
        platform = patch('sys.platform', 'darwin')
        listdir = patch(
            'frostmark.profiles.listdir',
            return_value=expected_profiles
        )

        with platform, listdir:
            self.assertEqual(
                [basename(path) for path in get_profiles('firefox')],
                expected_profiles
            )

    def test_profile_opera_win(self):
        '''
        Test fetching Opera profiles on Windows.
        '''

        from frostmark.profiles import get_profiles
        expected_profiles = ['Opera stable']
        platform = patch('sys.platform', 'win32')
        listdir = patch(
            'frostmark.profiles.listdir',
            return_value=expected_profiles
        )

        # with APPDATA
        with platform, listdir:
            self.assertEqual(
                [basename(path) for path in get_profiles('opera')],
                expected_profiles
            )

        # without APPDATA
        env = patch('frostmark.profiles.environ', {})
        with platform, listdir, env:
            self.assertEqual(
                [basename(path) for path in get_profiles('opera')],
                expected_profiles
            )
