import os

SECRET_KEY = 'SECRET_KEY'  # os.environ['SECRET_KEY']
DB_USERNAME = 'root'  # os.environ['DB_USERNAME']
DB_PASSWORD = 'garwal83'  # os.environ['DB_PASSWORD']
DB_HOST = 'localhost'  # os.environ['DB_HOST']
DATABASE_NAME = 'config'  # os.environ['DATABASE_NAME']
DB_URI = "mysql+pymysql://%s:%s@%s:3306/%s?charset=UTF8MB4"\
 % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)


SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
MYSQL_ROOT_PASSWORD = 'garwal83'  # os.environ['MYSQL_ROOT_PASSWORD']

BASE_INSTANCE_OWNER_EMAIL = 'root@example.com'


JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_SECURE = False  # True in production
JWT_COOKIE_CSRF_PROTECT = True
JWT_SECRET_KEY = 'super-secret'
