'''
Import bookmarks from various bookmarks database files into internal database.
'''
from ensure import ensure_annotations

from sqlalchemy import (
    create_engine, Column, Integer, String
)
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.ext.declarative.api import DeclarativeMeta as MetaBase

from frostmark.db import get_session
from frostmark.common import traverse
from frostmark.models import Folder, Bookmark
from frostmark.importer.firefox import FirefoxImporter


class Importer:
    '''
    Interface for retrieving and importing bookmarks into local storage
    for multiple backends.
    '''
    # pylint: disable=too-few-public-methods

    @ensure_annotations
    def __init__(self, backend: str):
        self.backend = None
        if backend == 'firefox':
            self.backend = FirefoxImporter()

    @staticmethod
    @ensure_annotations
    def _path_session(path: str, base: MetaBase) -> Session:
        '''
        Create a SQLAlchemy session over a SQLite database with custom
        MetaBase that connects the Python models to the engine and session.
        '''
        engine = create_engine(f'sqlite:///{path}')
        base.prepare(engine)
        maker = sessionmaker(bind=engine)
        session = maker()
        return session

    @ensure_annotations
    def import_from(self, path: str):
        '''
        Import bookmarks from particular path into internal storage.
        '''
        # pylint: disable=too-many-locals

        backend = self.backend

        # get the bookmarks tree from file
        source = self._path_session(path=path, base=backend.BASE)
        tree = backend.assemble_import_tree(source)

        # open internal DB
        nodes = traverse(tree)
        folders = {
            node.id: node
            for node in nodes
            if node.node_type == Folder
        }
        bookmarks = {
            node.id: node
            for node in nodes
            if node.node_type == Bookmark
        }

        # sqla objects
        frost = get_session()
        sqla_folders = {}

        # add folder structure to the database
        sorted_folders = sorted(
            folders.values(),
            # parent_folder_id is None for root folder
            key=lambda item: item.parent_folder_id or 0
        )
        for folder in sorted_folders:
            kwargs = {
                'folder_name': folder.folder_name
            }
            if folder.parent_folder_id:
                # in case there is a parent, get the Folder object
                # and pull its ID after flush() (otherwise it's None)
                real_id = sqla_folders[folder.parent_folder_id].id
                kwargs['parent_folder_id'] = real_id

            new_folder = Folder(**kwargs)
            frost.add(new_folder)

            # flush to obtain folder ID,
            # especially necessary for nested folders
            frost.flush()

            # preserve the original ID and point to a SQLA object
            sqla_folders[folder.id] = new_folder

        # add bookmarks
        for key in sorted(bookmarks.keys()):
            book = bookmarks[key]
            kwargs = {
                'title': book.title,
                'url': book.url,
                'icon': b'',
                'folder_id': sqla_folders[book.folder_id].id
            }

            # no need to flush, nothing required a bookmark
            # ID to be present before final commit()
            new_book = Bookmark(**kwargs)
            frost.add(new_book)

        # write data into internal DB
        frost.commit()
