'''
Test for editing imported bookmarks.
'''
import unittest
from os import listdir, remove
from os.path import join, abspath, dirname


class EditTestCase(unittest.TestCase):
    '''
    TestCase for editing imported bookmarks.
    '''

    def test_edit_parent_folder(self):
        '''
        Test editing a parent folder of a Folder.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Folder
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        items = [
            {'id': 321, 'folder_name': 'old parent'},
            {'id': 666, 'folder_name': 'child', 'parent_folder_id': 321},
            {'id': 123, 'folder_name': 'new parent'}
        ]
        session = get_session()
        try:
            for item in items:
                session.add(Folder(**item))
            session.commit()

            for item in items:
                self.assertEqual(
                    session.query(Folder).filter(
                        Folder.folder_name == item['folder_name']
                    ).first().id,
                    item['id']
                )

            self.assertEqual(
                session.query(Folder).filter(
                    Folder.id == items[1]['id']
                ).first().parent_folder_id,
                items[0]['id']
            )

            Editor.change_parent_folder(
                folder_id=items[1]['id'],
                parent_id=items[2]['id']
            )

            self.assertEqual(
                session.query(Folder).filter(
                    Folder.id == items[1]['id']
                ).first().parent_folder_id,
                items[2]['id']
            )

        finally:
            session.close()

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_edit_parent_folder_circular(self):
        '''
        Test pointing parent folder to the folder's own id.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Folder
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {'id': 321, 'folder_name': 'child'}
        session = get_session()
        try:
            session.add(Folder(**item))
            session.commit()
        finally:
            session.close()

        with self.assertRaises(Exception):
            Editor.change_parent_folder(
                folder_id=item['id'],
                parent_id=item['id']
            )

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_edit_parent_folder_missingparent(self):
        '''
        Test editing parent to a non-existing Folder.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Folder
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {'id': 321, 'folder_name': 'child'}
        session = get_session()
        try:
            session.add(Folder(**item))
            session.commit()
        finally:
            session.close()

        with self.assertRaises(Exception):
            Editor.change_parent_folder(
                folder_id=item['id'],
                parent_id=2 ** 31
            )

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_edit_parent_folder_missingchild(self):
        '''
        Test editing parent of a non-existing Folder.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Folder
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {'id': 321, 'folder_name': 'new parent'}
        session = get_session()
        try:
            session.add(Folder(**item))
            session.commit()
        finally:
            session.close()

        with self.assertRaises(Exception):
            Editor.change_parent_folder(
                folder_id=2 ** 31,
                parent_id=item['id']
            )

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_edit_parent_bookmark(self):
        '''
        Test editing a parent folder of a bookmark.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Folder, Bookmark
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        items = [{
            'id': 321, 'folder_name': 'old parent', 'type': Folder
        }, {
            'id': 666, 'title': 'child', 'folder_id': 321, 'type': Bookmark,
            'url': '<url>', 'icon': b'<bytes>'
        }, {
            'id': 123, 'folder_name': 'new parent', 'type': Folder
        }]
        session = get_session()
        try:
            for item in items:
                item_type = item.pop('type')
                if item_type == Folder:
                    session.add(Folder(**item))
                elif item_type == Bookmark:
                    session.add(Bookmark(**item))
                item['type'] = item_type
            session.commit()

            for item in items:
                item_type = item.pop('type')
                if item_type == Folder:
                    self.assertEqual(
                        session.query(Folder).filter(
                            Folder.folder_name == item['folder_name']
                        ).first().id,
                        item['id']
                    )
                elif item_type == Bookmark:
                    self.assertEqual(
                        session.query(Bookmark).filter(
                            Bookmark.title == item['title']
                        ).first().id,
                        item['id']
                    )
                item['type'] = item_type

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.id == items[1]['id']
                ).first().folder_id,
                items[0]['id']
            )

            Editor.change_parent_bookmark(
                bookmark_id=items[1]['id'],
                parent_id=items[2]['id']
            )

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.id == items[1]['id']
                ).first().folder_id,
                items[2]['id']
            )
        finally:
            session.close()

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_edit_parent_bookmark_circular(self):
        '''
        Test pointing parent folder to the bookmark's own id.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Bookmark
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {
            'id': 321, 'title': 'child',
            'url': '<url>', 'icon': b'<bytes>'
        }
        session = get_session()
        try:
            session.add(Bookmark(**item))
            session.commit()
        finally:
            session.close()

        with self.assertRaises(Exception):
            Editor.change_parent_bookmark(
                bookmark_id=item['id'],
                parent_id=item['id']
            )

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_edit_parent_bookmark_missingparent(self):
        '''
        Test editing parent to a non-existing Folder.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Bookmark
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {
            'id': 321, 'title': 'child',
            'url': '<url>', 'icon': b'<bytes>'
        }
        session = get_session()
        try:
            session.add(Bookmark(**item))
            session.commit()
        finally:
            session.close()

        with self.assertRaises(Exception):
            Editor.change_parent_bookmark(
                bookmark_id=item['id'],
                parent_id=2 ** 31
            )

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_edit_parent_bookmark_missingchild(self):
        '''
        Test editing parent of a non-existing Bookmark.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Bookmark
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {
            'id': 321, 'title': 'child',
            'url': '<url>', 'icon': b'<bytes>'
        }
        session = get_session()
        try:
            session.add(Bookmark(**item))
            session.commit()
        finally:
            session.close()

        with self.assertRaises(Exception):
            Editor.change_parent_bookmark(
                bookmark_id=2 ** 31,
                parent_id=item['id']
            )

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_rename_folder(self):
        '''
        Test renaming a Folder item.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Folder
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {'id': 321, 'folder_name': 'old parent'}
        session = get_session()
        try:
            session.add(Folder(**item))
            session.commit()

            self.assertEqual(
                session.query(Folder).filter(
                    Folder.folder_name == item['folder_name']
                ).first().id,
                item['id']
            )

            self.assertEqual(
                session.query(Folder).filter(
                    Folder.id == item['id']
                ).first().folder_name,
                item['folder_name']
            )

            Editor.rename_folder(
                folder_id=item['id'],
                name=item['folder_name'][:3]
            )

            self.assertEqual(
                session.query(Folder).filter(
                    Folder.id == item['id']
                ).first().folder_name,
                item['folder_name'][:3]
            )
        finally:
            session.close()

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_rename_bookmark(self):
        '''
        Test renaming a Bookmark item.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Bookmark
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {
            'id': 321, 'title': 'child',
            'url': '<url>', 'icon': b'<bytes>'
        }
        session = get_session()
        try:
            session.add(Bookmark(**item))
            session.commit()

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.title == item['title']
                ).first().id,
                item['id']
            )

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.id == item['id']
                ).first().title,
                item['title']
            )

            Editor.rename_bookmark(
                bookmark_id=item['id'],
                name=item['title'][:3]
            )

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.id == item['id']
                ).first().title,
                item['title'][:3]
            )
        finally:
            session.close()

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))

    def test_change_bookmark_url(self):
        '''
        Test renaming a Bookmark item.
        '''
        from frostmark import db_base, user_data
        from frostmark.db import get_session
        from frostmark.models import Bookmark
        from frostmark.editor import Editor

        data = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(data))

        item = {
            'id': 321, 'title': 'child',
            'url': '<url>', 'icon': b'<bytes>'
        }
        session = get_session()
        try:
            session.add(Bookmark(**item))
            session.commit()

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.title == item['title']
                ).first().id,
                item['id']
            )

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.id == item['id']
                ).first().title,
                item['title']
            )

            Editor.change_bookmark_url(
                bookmark_id=item['id'],
                url=f"http://{item['url']}"
            )

            self.assertEqual(
                session.query(Bookmark).filter(
                    Bookmark.id == item['id']
                ).first().url,
                f"http://{item['url']}"
            )
        finally:
            session.close()

        self.assertIn(db_base.DB_NAME, listdir(data))
        remove(join(data, db_base.DB_NAME))
