from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import pyclbr

from settings import DB_URI
from utils.helpers import _import_submodules_from_package
import controllers

engine = create_engine(DB_URI)
inspector = inspect(engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def setup_db():
    try:
        if not database_exists(DB_URI):
            create_db()
        return True
    except Exception as e:
        print('Database not found', e)
        return False


def create_db():
    create_database(DB_URI)
    create_tables()


def create_tables():
    tables = inspector.get_table_names()

    for module in _import_submodules_from_package(controllers):
        for submodule in _import_submodules_from_package(module):
            module_name = submodule.__name__.split('.')[-1]
            if module_name == 'model':
                for _class in pyclbr.readmodule(submodule.__name__).keys():
                    tbl = getattr(submodule, _class)
                    tbl_name = getattr(tbl, '__tablename__')
                    if tbl_name not in tables:
                        print('Creating table: ', tbl_name)
                        tbl.__table__.create(session.bind)


if __name__ == '__main__':
    setup_db()
