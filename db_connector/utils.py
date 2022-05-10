from db_connector.configs import *
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


# construct connection string, formatted string
# self.connection_string = cf.dialect + "://" + cf.db_username + ":" + cf.db_password + \
#                          "@" + cf.host + ":" + cf.port + "/" + cf.db_name + cf.charset

# Constrict a connection string, formatted URL
connection_string = engine.URL.create(
    DB_DIALECT,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    query={
        'charset': 'utf8mb4',
        'check_same_thread': 'False'
    },
)

# Initiate an engine
_engine = create_engine(
    connection_string,
    encoding='utf-8',
    pool_pre_ping=True,
    echo=False
)


# initiate a session that holds DB objs to manipulate it, it's the DB handle
Session = scoped_session(sessionmaker(bind=_engine))
session = Session()

Base = declarative_base()
