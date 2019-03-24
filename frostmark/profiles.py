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

    path = ''
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
        elif sys.platform == 'linux':
            path = join(abspath(expanduser('~')), '.mozilla', 'firefox')

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
    loc = get_location(browser)

    # missing profile folder or the browser is not installed
    if loc == '':
        return profiles

    if browser == 'firefox':
        profiles = [
            join(loc, fname, 'places.sqlite')
            for fname in listdir(loc)
            if fname.endswith('.default') and join(loc, fname, 'places.sqlite')
        ]

    elif browser == 'opera':
        # only one profile supported
        bm_location = join(loc, 'Bookmarks')
        profiles = [bm_location] if exists(bm_location) else []

    return profiles


@ensure_annotations
def get_all_profiles() -> dict:
    '''
    Get all profiles for all supported browsers.
    '''

    browsers = ['firefox', 'opera']
    profiles = {}

    for browser in browsers:
        profiles[browser] = get_profiles(browser)

    return profiles


@ensure_annotations
def print_profiles(browser: str):
    '''
    Print all possible locations usable for importing for a specific
    browser such as .sqlite files or JSON files.
    '''

    for item in get_profiles(browser):
        print(item)


@ensure_annotations
def print_all_profiles():
    '''
    Print all possible locations usable for importing for a specific
    browser such as .sqlite files or JSON files.
    '''

    for browser, profiles in get_all_profiles().items():
        # ignore empty profiles - probably no profiles
        # or this browser is not installed
        if not profiles:
            continue

        print(browser)
        for item in profiles:
            print(f'\t{item}')
