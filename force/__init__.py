from flask import Flask
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

app = Flask("4ce")
app.config.from_object("config")
app.debug = True

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

flask_bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

from force import login
from force import notes
from force import auth