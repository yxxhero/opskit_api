from datetime import datetime
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


class Uploads(db.Model):
    __tablename__ = 'upload'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime)
    image_path = db.Column(db.String(256))
    user = db.relationship(
        'User', backref=db.backref('user_images', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    prase_count = db.Column(db.Integer, default=0)
    state = db.Column(db.Integer, default=0)
    content = db.Column(db.Text)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    noteId = db.Column(db.Integer, db.ForeignKey('note.id'))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    user = db.relationship(
        'User', backref=db.backref('user_comments', lazy='dynamic'))
    note = db.relationship(
        'Note', backref=db.backref('note_comments', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Note(db.Model):
    __tablename__ = 'note'

    NOTE_TYPES = [
        (1, 'database'),
        (2, 'web'),
        (3, 'docker'),
        (4, 'security'),
        (5, 'notice')
    ]

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    view_count = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    raw_content = db.Column(db.Text)
    note_type = db.Column(ChoiceType(NOTE_TYPES, impl=db.Integer()))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    user = db.relationship(
        'User', backref=db.backref('note_set', lazy='dynamic'))

    def __init__(self, title, content, raw_content, note_type, user, view_count=0, is_public=False):

        super().__init__()
        self.note_type = note_type
        self.title = title
        self.user = user
        self.content = content
        self.view_count = view_count
        self.is_public = is_public
        self.raw_content = raw_content
        self.create_time = datetime.utcnow()
        self.update_time = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = "user"

    USER_ROLES = [
        (1, 'Admin'),
        (2, 'Common'),
        (3, 'Vip')
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(100))
    user_email = db.Column(db.String(512))
    user_role = db.Column(ChoiceType(USER_ROLES, impl=db.Integer()), default=1)
    is_auditing = db.Column(db.Boolean, default=False)
    user_avatar = db.Column(db.String(512), default='https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png')
    user_description = db.Column(db.Text)
    create_time = db.Column(db.DateTime)

    def __init__(self, user_name, user_password, user_email, user_role=2, user_avatar='https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png', is_auditing=False, user_description=""):

        super().__init__()
        self.user_name = user_name
        self.user_password = user_password
        self.user_email = user_email
        self.user_role = user_role
        self.user_avatar = user_avatar
        self.create_time = datetime.utcnow()
        self.is_auditing = is_auditing
        self.user_description = user_description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
