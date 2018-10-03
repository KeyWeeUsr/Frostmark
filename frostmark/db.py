'''
Module for creating SQLite DB schema and session retrieving.
'''

from frostmark.db_base import BASE, SESSIONMAKER, ENGINE


def get_session():
    '''
    Create DB schema and return a new session.
    '''

    BASE.metadata.create_all(ENGINE)
    return SESSIONMAKER()
