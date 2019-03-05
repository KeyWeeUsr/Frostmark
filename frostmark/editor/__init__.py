'''
Edit imported bookmarks.
'''
from ensure import ensure_annotations

from frostmark.db import get_session
from frostmark.models import Folder, Bookmark


class Editor:
    '''
    Class encapsuling methods for editing imported Bookmarks and Folders.
    '''
    # pylint: disable=too-few-public-methods

    @staticmethod
    @ensure_annotations
    def change_parent_folder(folder_id: int, parent_id: int):
        '''
        Change folder's parent if both the parent and the child exist
        and if the new parent isn't the child itself.
        '''

        if folder_id == parent_id:
            raise Exception('Folder can not be its own parent')

        session = get_session()
        try:
            child = session.query(Folder).filter(
                Folder.id == folder_id
            ).first()

            parent = session.query(Folder).filter(
                Folder.id == parent_id
            ).first()
            if not child or not parent:
                raise Exception(
                    f'Child: {child} or parent: {parent} does not exist'
                )

            child.parent_folder_id = parent.id
            session.commit()

        finally:
            session.close()

    @staticmethod
    @ensure_annotations
    def change_parent_bookmark(bookmark_id: int, parent_id: int):
        '''
        Change bookmark's parent if both the parent and the child exist
        and if the new parent isn't the child itself.
        '''

        if bookmark_id == parent_id:
            raise Exception('Bookmark can not be its own parent')

        session = get_session()
        try:
            child = session.query(Bookmark).filter(
                Bookmark.id == bookmark_id
            ).first()

            parent = session.query(Folder).filter(
                Folder.id == parent_id
            ).first()
            if not child or not parent:
                raise Exception(
                    f'Child: {child} or parent: {parent} does not exist'
                )

            child.folder_id = parent.id
            session.commit()

        finally:
            session.close()

    @staticmethod
    @ensure_annotations
    def rename_folder(folder_id: int, name: str):
        '''
        Change folder's name.
        '''

        session = get_session()
        try:
            child = session.query(Folder).filter(
                Folder.id == folder_id
            ).first()

            child.folder_name = name
            session.commit()

        finally:
            session.close()

    @staticmethod
    @ensure_annotations
    def rename_bookmark(bookmark_id: int, name: str):
        '''
        Change bookmark's title.
        '''

        session = get_session()
        try:
            child = session.query(Bookmark).filter(
                Bookmark.id == bookmark_id
            ).first()

            child.title = name
            session.commit()

        finally:
            session.close()

    @staticmethod
    @ensure_annotations
    def change_bookmark_url(bookmark_id: int, url: str):
        '''
        Change bookmark's title.
        '''

        session = get_session()
        try:
            child = session.query(Bookmark).filter(
                Bookmark.id == bookmark_id
            ).first()

            child.url = url
            session.commit()

        finally:
            session.close()
