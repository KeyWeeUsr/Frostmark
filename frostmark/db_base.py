'''
Module for creating a connection to SQLite DB
and SQLAlchemy declarative base home.
'''

from os.path import join, dirname, abspath

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from frostmark import user_data

DB_NAME = 'user_db.sqlite'
DB_PATH = join(dirname(abspath(user_data.__file__)), DB_NAME)
ENGINE = create_engine(f'sqlite:///{DB_PATH}')
BASE = declarative_base()
SESSIONMAKER = sessionmaker()
SESSIONMAKER.configure(bind=ENGINE)
