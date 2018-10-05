import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# model

class Note(db.Model):
    __tablename__ = 'note'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime)

    def __init__(self, title, content):
        self.title = title
        self.content = content 
        self.create_time = datetime.utcnow()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(100))
    user_email = db.Column(db.String(512))
    note = db.relationship('Note', backref='user', lazy=True)


