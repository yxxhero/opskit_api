import datetime
from sqlalchemy_utils.types.choice import ChoiceType
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
db = SQLAlchemy(app)
redis_store = FlaskRedis(app)
migrate = Migrate(app, db)

# model


class Note(db.Model):
    __tablename__ = 'note'

    NOTE_TYPES = [
        (1, 'database'),
        (2, 'web'),
        (3, 'docker'),
        (4, 'security')
    ]

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    note_type = db.Column(ChoiceType(NOTE_TYPES, impl=db.Integer()))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime)

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.create_time = datetime.utcnow()


class User(db.Model):
    __tablename__ = "user"

    USER_ROLES = [
        (0, 'vip'),
        (1, 'Common'),
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(100))
    user_email = db.Column(db.String(512))
    user_role = db.Column(ChoiceType(USER_ROLES, impl=db.Integer()), default=1)
    note = db.relationship('Note', backref='user', lazy=True)
