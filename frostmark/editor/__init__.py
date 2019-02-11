'''
Edit imported bookmarks.
'''
from ensure import ensure_annotations

from frostmark.db import get_session
from frostmark.models import Folder


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
        child = session.query(Folder).filter(
            Folder.id == folder_id
        ).first()

        parent = session.query(Folder).filter(
            Folder.id == parent_id
        ).first()
        if not child or not parent:
            session.close()
            raise Exception(
                f'Child: {child} or parent: {parent} does not exist'
            )

        child.parent_folder_id = parent.id
        session.commit()
        session.close()
