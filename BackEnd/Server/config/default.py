'''
Default values, to be used for all environments or overridden by individual environments. An example might be setting
DEBUG = False in config/default.py and DEBUG = True in config/development.py.
'''

DEBUG = False

# MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'db_name'
MYSQL_CURSORCLASS = 'DictCursor'
