from flask import Flask
from flask_cors import CORS
from db_connector.manager import Manager

# Init the flask app
app = Flask(__name__)
CORS(app)
app.debug = True

# Init a DB session
DBMS = Manager()