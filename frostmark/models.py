'''
ORM SQLAlchemy models for Frostmark application storage.
'''

from ensure import ensure_annotations
from sqlalchemy import Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import relationship
from frostmark.db import BASE


class Folder(BASE):
    '''
    Folder item for grouping bookmarks.
    ID 0 is reserved for ROOT folder.
    '''
    # pylint: disable=too-few-public-methods

    __tablename__ = 'folder'

    __ROOT_ID__ = 0
    __ROOT_NAME__ = 'ROOT'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    folder_name = Column(String, nullable=False, default='')
    parent_folder_id = Column(
        Integer, ForeignKey('folder.id'),
        nullable=False, default=0
    )

    # not a column
    bookmarks = relationship('Bookmark', backref=__tablename__)
    parent_folder = relationship(
        'Folder', backref=__tablename__, remote_side='Folder.id'
    )

    @staticmethod
    @ensure_annotations
    def get_root() -> tuple:
        '''
        Return root folder constants to e.g. create root folder value in DB
        if it does not exist.
        '''
        return (Folder.__ROOT_ID__, Folder.__ROOT_NAME__)

    def __repr__(self):
        return (
            "<Folder("
            "id=%s, name='%s', parent_folder_id=%s"
            ")>" % (
                self.id, self.folder_name,
                self.parent_folder_id,
            )
        )


class Bookmark(BASE):
    '''
    Bookmark item containing URL, title, icon (favicon.ico) and folder_id.
    '''
    # pylint: disable=too-few-public-methods

    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    icon = Column(BLOB, nullable=False)
    folder_id = Column(
        Integer, ForeignKey('folder.id'),
        nullable=False, default=0
    )

    def __repr__(self):
        return (
            "<Bookmark("
            "id=%s, title='%s', url='%s', folder_id=%s"
            ")>" % (
                self.id, self.title,
                self.url, self.folder_id
            )
        )
