'''
Module for creating a connection to SQLite DB
and SQLAlchemy declarative base home.
'''
import unittest

from os import listdir, remove
from os.path import join, dirname, abspath


class DBBaseTestCase(unittest.TestCase):
    '''
    TestCase for SQLite database backend.
    '''

    def test_db_base(self):
        '''
        Test all variables, locations, files for creating DB base.
        '''

        from frostmark import db_base
        from frostmark import user_data

        folder = dirname(abspath(user_data.__file__))
        self.assertEqual(db_base.DB_PATH, join(folder, db_base.DB_NAME))
        self.assertEqual(
            str(db_base.ENGINE.url).replace('sqlite:///', ''),
            db_base.DB_PATH
        )
        self.assertNotIn(db_base.DB_NAME, listdir(folder))

    def test_db_create(self):
        '''
        Test creating SQLite3 DB only (without tables)
        in the user_data section.
        '''

        from frostmark import db_base
        from frostmark import user_data

        folder = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(folder))

        db_base.BASE.metadata.create_all(db_base.ENGINE)
        ses = db_base.SESSIONMAKER()
        ses.close()

        self.assertIn(db_base.DB_NAME, listdir(folder))
        remove(join(folder, db_base.DB_NAME))

    def test_db_session(self):
        '''
        Test getting session for SQLite DB which passively creates a new
        DB (new .sqlite file) if it isn't present yet.
        '''

        from frostmark import user_data
        from frostmark import db_base
        from frostmark.db import get_session
        from sqlalchemy.orm.session import Session

        folder = dirname(abspath(user_data.__file__))
        self.assertNotIn(db_base.DB_NAME, listdir(folder))

        # two sessions to check whether SQLA raises an Exception
        # e.g. if a table already exists and create_all() is called
        ses_one = get_session()
        self.assertIsInstance(ses_one, Session)

        ses_two = get_session()
        self.assertIsInstance(ses_two, Session)

        ses_one.close()
        ses_two.close()

        self.assertIn(db_base.DB_NAME, listdir(folder))
        remove(join(folder, db_base.DB_NAME))
