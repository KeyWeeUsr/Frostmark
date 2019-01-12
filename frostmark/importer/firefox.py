'''
Module for retrieving bookmark data from Firefox `places.sqlite`
and providing a clean tree structure for further use.
'''

from ensure import ensure_annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import (
    declarative_base,
    DeferredReflection
)
from anytree import Node

from frostmark.common import assemble_folder_tree, assemble_bookmark_tree
from frostmark.models import Folder, Bookmark


class FirefoxImporter:
    '''
    Assembler for Firefox bookmark node tree.
    '''
    # pylint: disable=too-few-public-methods

    # toolkit/components/places/nsNavBookmarks.h
    ITEMTYPE_BOOKMARK = 1
    ITEMTYPE_FOLDER = 2
    ITEMTYPE_SEPARATOR = 3
    BASE = declarative_base(cls=DeferredReflection)

    @staticmethod
    @ensure_annotations
    def assemble_import_tree(session: Session) -> Node:
        '''
        Assemble a bookmark tree structure from places.sqlite to be able
        to either display or correctly import/merge the structure into
        internal bookmarks database.

        sample:
        {
            '_sa_instance_state': <InstanceState object>,
            'fk': None,
            'keyword_id': None,
            'lastModified': 1530777327687000,
            'parent': 5380,
            'folder_type': None,
            'position': 0,
            'id': 5538,
            'dateAdded': 1530777262406000,
            'type': 2,
            'title': 'title'
        }
        '''
        ff_folders = session.query(moz_bookmarks).filter(
            moz_bookmarks.type == FirefoxImporter.ITEMTYPE_FOLDER
        ).order_by(moz_bookmarks.id).all()

        folders = []
        for folder in ff_folders:
            folders.append({
                'id': folder.id,
                'folder_name': (
                    '<no title>' if not folder.title else folder.title
                ),
                'parent_folder_id': (
                    folder.parent if folder.parent != 0 else None
                )
            })

        # printable folder tree
        folder_tree = assemble_folder_tree(
            items=folders,
            key='parent_folder_id',
            node_type=Folder
        )

        ff_bookmarks = session.query(
            moz_bookmarks,
            moz_places
        ).filter(
            moz_bookmarks.type == FirefoxImporter.ITEMTYPE_BOOKMARK
        ).filter(
            moz_bookmarks.fk == moz_places.id
        ).order_by(moz_places.id).all()

        bookmarks = []
        for book, place in ff_bookmarks:
            bookmarks.append({
                'id': book.id,
                'title': place.url if not book.title else book.title,
                'folder_id': book.parent,
                'url': place.url
            })

        # printable folder+bookmark tree
        bookmark_tree = assemble_bookmark_tree(
            items=bookmarks,
            key='folder_id',
            folder_tree_root=folder_tree,
            node_type=Bookmark
        )
        return bookmark_tree


class moz_anno_attributes(FirefoxImporter.BASE):
    # pylint: disable=too-few-public-methods,missing-docstring,invalid-name

    __tablename__ = 'moz_anno_attributes'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String)


class moz_annos(FirefoxImporter.BASE):
    # pylint: disable=too-few-public-methods,missing-docstring,invalid-name

    __tablename__ = 'moz_annos'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    place_id = Column(Integer)
    anno_attribute_id = Column(Integer)
    mime_type = Column(String)
    content = Column(String)
    flags = Column(Integer)
    expiration = Column(Integer)
    type = Column(Integer)
    dateAdded = Column(Integer)
    lastModified = Column(Integer)


class moz_bookmarks(FirefoxImporter.BASE):
    '''
    Item info - folders, bookmarks, separators, etc.
    '''
    # pylint: disable=too-few-public-methods,invalid-name

    __tablename__ = 'moz_bookmarks'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    type = Column(Integer)
    fk = Column(Integer)
    parent = Column(Integer)
    position = Column(Integer)
    title = Column(String)
    keyword_id = Column(Integer)
    folder_type = Column(String)
    dateAdded = Column(Integer)
    lastModified = Column(Integer)


class moz_historyvisits(FirefoxImporter.BASE):
    # pylint: disable=too-few-public-methods,missing-docstring,invalid-name

    __tablename__ = 'moz_historyvisits'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    from_visit = Column(Integer)
    place_id = Column(Integer)
    visit_date = Column(Integer)
    visit_type = Column(Integer)
    session = Column(Integer)


class moz_inputhistory(FirefoxImporter.BASE):
    # pylint: disable=too-few-public-methods,missing-docstring,invalid-name

    __tablename__ = 'moz_inputhistory'
    place_id = Column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    input = Column(String)
    use_count = Column(Integer)


class moz_items_annos(FirefoxImporter.BASE):
    # pylint: disable=too-few-public-methods,missing-docstring,invalid-name

    __tablename__ = 'moz_items_annos'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    item_id = Column(Integer)
    anno_attribute_id = Column(Integer)
    mime_type = Column(String)
    content = Column(String)
    flags = Column(Integer)
    expiration = Column(Integer)
    type = Column(Integer)
    dateAdded = Column(Integer)
    lastModified = Column(Integer)


class moz_keywords(FirefoxImporter.BASE):
    '''
    Tag info.
    '''
    # pylint: disable=too-few-public-methods,invalid-name

    __tablename__ = 'moz_keywords'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    keyword = Column(String)
    place_id = Column(Integer)
    post_data = Column(String)


class moz_places(FirefoxImporter.BASE):
    '''
    Bookmark info.
    '''
    # pylint: disable=too-few-public-methods,invalid-name

    __tablename__ = 'moz_places'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    url = Column(String)
    title = Column(String)
    rev_host = Column(String)
    visit_count = Column(Integer)
    hidden = Column(Integer)
    typed = Column(Integer)
    favicon_id = Column(Integer)
    frecency = Column(Integer)
