import sys
from os import environ
from os.path import join, dirname, abspath, expanduser


def get_location(browser: str):
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


def get_profiles():
    return [
        filename
        for filename in listdir(get_location())
        if filename.endswith('.default')
    ]
