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


def setup_db(app):
    try:
        if not database_exists(DB_URI):
            app.logger.warning('Database not found. Creating database')
            create_database(DB_URI)
        app.logger.info('Checking database tables')
        create_tables(app)
        return True
    except Exception as e:
        app.logger.error('Something went wrong with database setup')
        app.logger.error(e)
        return False


def create_tables(app):
    tables = inspector.get_table_names()
    app.logger.debug('Found existing config tables')
    app.logger.debug(tables)

    for module in _import_submodules_from_package(controllers):
        for submodule in _import_submodules_from_package(module):
            module_name = submodule.__name__.split('.')[-1]
            if module_name == 'model':
                for _class in pyclbr.readmodule(submodule.__name__).keys():
                    tbl = getattr(submodule, _class)
                    tbl_name = getattr(tbl, '__tablename__')
                    if tbl_name not in tables:
                        app.logger.info('Creating table: ', tbl_name)
                        tbl.__table__.create(session.bind)

    # first time instance and root user setup
    setup_root_admin(app)


def setup_root_admin(app):
    app.logger.info('Checking if base instance is setup')
    instance = session.query(Instance).get(1)
    if instance:
        app.logger.info('Base instance found')
        app.logger.info('Checking if root user exists')
        user = session.query(User).get(1)
        if user:
            app.logger.info('root user found')
        else:
            app.logger.warning('root user not found. Creating root user')
            user = User()
            pw = input('Enter root user password:')
            if not pw:
                app.logger.error('root user password can not be empty.')
                sys.exit()
            user.set_password(str(pw).encode('utf-8'))
            user.__setattr__('user_name', 'root')
            user.__setattr__('name', 'root')
            user.__setattr__('instance_id', 1)
            user.__setattr__('admin', True)
            user.__setattr__('email', BASE_INSTANCE_OWNER_EMAIL)
            session.add(user)
            session.commit()
            app.logger.info('Completed creating root user')
    else:
        app.logger.warning('Base instance not found. Creating Base instance')
        instance = Instance()
        instance.__setattr__('name', 'Base Instance')
        instance.__setattr__('owner_name', 'root')
        instance.__setattr__('owner_email', BASE_INSTANCE_OWNER_EMAIL)
        session.add(instance)
        session.commit()
        setup_root_admin(app)


if __name__ == '__main__':
    pass
