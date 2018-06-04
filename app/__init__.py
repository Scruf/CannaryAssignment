from flask import Flask
from flask_mongoengine import MongoEngine
from app.apis import api
from mongoengine import connect
from .extensions import db
from .config import * 

#create_app will initialize all of the application settings such mongodb connection and flask_restplus
def create_app():
	app = Flask(__name__)
	connect(**MONGODB_SETTINGS)
	app.debug = True
	api.init_app(app)
	db.init_app(app)	
	return app
