'''
Module for creating SQLite DB schema and session retrieving.
'''

from frostmark.db_base import BASE, SESSIONMAKER, ENGINE


def folder_check_root(session):
    '''
    Check whether default rows for Folder model exist and create them if not.
    '''
    from frostmark.models import Folder

    folders = session.query(Folder).all()
    root_folder = Folder.get_root()

    if not any([fold.id == root_folder[0] for fold in folders]):
        session.add(Folder(
            id=root_folder[0],
            folder_name=root_folder[1],
            parent_folder_id=root_folder[0]
        ))
    session.commit()


def get_session():
    '''
    Create DB schema and return a new session.
    '''

    BASE.metadata.create_all(ENGINE)
    session = SESSIONMAKER()
    folder_check_root(session)
    return session
