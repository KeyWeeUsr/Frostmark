'''
Module for retrieving all 'profiles' from specified browser.
'''

import sys
from os import environ, listdir
from os.path import join, abspath, expanduser, exists

from ensure import ensure_annotations


@ensure_annotations
def get_location(browser: str) -> str:
    '''
    Get absolute path of the profiles location for browser.
    '''

    path = None
    if browser == 'firefox':
        if sys.platform == 'darwin':
            path = join(
                abspath(expanduser('~')),
                'Library', 'Application Support',
                'Firefox', 'Profiles'
            )
        elif sys.platform == 'win32':
            if 'APPDATA' in environ:
                path = join(
                    environ['APPDATA'],
                    'Mozilla', 'Firefox', 'Profiles'
                )
            else:
                path = join(
                    abspath(expanduser('~')), 'AppData', 'Roaming',
                    'Mozilla', 'Firefox', 'Profiles'
                )

    elif browser == 'opera':
        if sys.platform == 'win32':
            if 'APPDATA' in environ:
                path = join(
                    environ['APPDATA'],
                    'opera software', 'Opera stable'
                )
            else:
                path = join(
                    abspath(expanduser('~')), 'AppData', 'Roaming',
                    'opera software', 'Opera stable'
                )
    return path


@ensure_annotations
def get_profiles(browser: str) -> list:
    '''
    Get all profiles from browser profile location.
    '''

    profiles = []
    if browser == 'firefox':
        profiles = [
            join(get_location(browser), filename, 'places.sqlite')
            for filename in listdir(get_location(browser))
            if filename.endswith('.default') and exists(filename)
        ]
    elif browser == 'opera':
        # only one profile supported
        location = join(get_location(browser), 'Bookmarks')
        profiles = [location] if exists(location) else []

    return profiles


@ensure_annotations
def print_profiles(browser: str):
    '''
    Print all possible locations usable for importing for a specific
    browser such as .sqlite files or JSON files.
    '''

    for item in get_profiles(browser):
        print(item)
