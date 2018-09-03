"""
Style checker for Frostmark.
"""

from subprocess import Popen


CASES = [
    'pycodestyle .',
    'pylint setup.py'
]


if __name__ == '__main__':
    for test in CASES:
        Popen(test).communicate()
