'''
Module for retrieving all 'profiles' from specified browser.
'''

import sys
from os import environ, listdir
from os.path import join, abspath, expanduser


def get_location(browser: str):
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
    return path


def get_profiles(browser: str):
    '''
    Get all profiles from browser profile location.
    '''

    return [
        filename
        for filename in listdir(get_location(browser))
        if filename.endswith('.default')
    ]
