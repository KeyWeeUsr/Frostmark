'''
Module for retrieving all 'profiles' from specified browser.
'''

import sys
from os import environ, listdir
from os.path import join, abspath, expanduser

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
            filename
            for filename in listdir(get_location(browser))
            if filename.endswith('.default')
        ]
    elif browser == 'opera':
        # only one profile supported
        profiles = [get_location(browser)]

    return profiles
