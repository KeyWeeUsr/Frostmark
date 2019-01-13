'''
Test for retrieving various browser profile locations.
'''
import unittest
from unittest.mock import patch
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
        with exi, platform, listdir:
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
        with exi, platform, listdir:
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
