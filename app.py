from flask import Flask
from flask_restful import  Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from opskit_api.resources.helloworld import HelloWorld 

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

api.add_resource(HelloWorld, '/')


