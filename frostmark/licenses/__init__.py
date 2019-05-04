"""
Module for handling all license files related to the project.
"""

from os import listdir
from os.path import abspath, dirname, join

from ensure import ensure_annotations


class Licenses:
    """
    Collector for all license files related to the project.
    """

    @staticmethod
    @ensure_annotations
    def fetch_licenses():
        """
        Read all *.txt files from this module's folder which contains
        all license files related to the project.
        """

        all_licenses = {}
        licenses_root = dirname(abspath(__file__))
        for file in listdir(licenses_root):
            if not file.endswith('.txt'):
                continue

            name_parts = file.split('-')
            if len(name_parts) > 1:
                filename = name_parts[-1]
                commit = name_parts[-2]
                package = ''.join(name_parts[0:-2])
            else:
                filename = package = ''.join(name_parts)
                commit = ''

            with open(join(licenses_root, file)) as license_file:
                all_licenses[package] = {
                    'commit': commit,
                    'filename': filename,
                    'license': license_file.read()
                }
        return all_licenses

    @staticmethod
    @ensure_annotations
    def print_all_licenses():
        """
        Pretty-print all collected licenses.
        """

        for name, item in Licenses.fetch_licenses().items():
            print('~' * 79)
            print(f'{name} - {item["filename"]} ({item["commit"]})')
            print('~' * 79)
            print(item['license'])
            print('\n\n')
