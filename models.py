from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    events = db.relationship('Event', secondary='attendee',
                             back_populates='users')

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    users = db.relationship('User', secondary='attendee',
                            back_populates='events')
    chats = db.relationship('Chat', secondary='event_chat',
                            back_populates='events')

class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True, nullable=False)
    events = db.relationship('Event', secondary='event_chat',
                             back_populates='chats')

class Attendee(db.Model):
    __tablename__ = 'attendee'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

class EventChat(db.Model):
    __tablename__ = 'event_chat'

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True)




