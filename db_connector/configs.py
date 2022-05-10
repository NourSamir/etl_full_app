import os

DB_HOST = os.environ.get('OP_DB_PROD_HOST', '')
DB_PORT = os.environ.get('OP_DB_PROD_PORT', 0)
DB_NAME = os.environ.get('OP_DB_NAME', '../db.sqlite')
DB_USERNAME = os.environ.get('OP_DB_USER_NAME', '')
DB_PASSWORD = os.environ.get('OP_DB_PASSWORD', '')
DB_DIALECT = 'sqlite'
DB_CHARSET = '?charset=utf8mb4'