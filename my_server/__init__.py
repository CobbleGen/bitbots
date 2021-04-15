from flask import Flask
import flask_sqlalchemy

app = Flask(__name__)
from my_server.config import Config
app.config.from_object(Config)
db = flask_sqlalchemy.SQLAlchemy(app)
from my_server import routes
from my_server import chainhandler
