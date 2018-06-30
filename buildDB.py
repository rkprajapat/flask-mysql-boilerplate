from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import pyclbr
import sys

from settings import DB_URI
from settings import BASE_INSTANCE_OWNER_EMAIL
from utils.helpers import _import_submodules_from_package
import controllers
from controllers.instance.model import Instance
from controllers.user.model import User

engine = create_engine(DB_URI)
inspector = inspect(engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def setup_db():
    try:
        if not database_exists(DB_URI):
            print('Database not found. Creating database')
            create_database(DB_URI)
        print('Cheking database tables')
        create_tables()
        return True
    except Exception as e:
        print('Something went wrong with database setup')
        print('ERROR :', e)
        return False


def create_tables():
    tables = inspector.get_table_names()
    print('Found existing config tables :', tables)

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

    # first time instance and root user setup
    setup_root_admin()


def setup_root_admin():
    print('Checking if base instance is setup')
    instance = session.query(Instance).get(1)
    if instance:
        print('Base instance found')
        user = session.query(User).get(1)
    else:

        print('Base instance not found. Creating Base instance')
        instance = Instance()  # Create default instance
        instance.__setattr__('name', 'Base Instance')
        instance.__setattr__('owner_name', 'root')
        instance.__setattr__('owner_email', BASE_INSTANCE_OWNER_EMAIL)
        print(instance)
        session.add(instance)
        session.commit()
        setup_root_admin()



if __name__ == '__main__':
    setup_db()
