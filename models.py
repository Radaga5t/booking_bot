from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    attendees = db.relationship('Attendee', back_populates='user', lazy='dynamic')
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    chat = db.relationship('Chat', back_populates='events')
    attendees = db.relationship('Attendee', back_populates='event', lazy='dynamic')

    def __init__(self, data):
        self.title = data.get('title')
        self.description = data.get('description')
        self.start_time = data.get('start_time')
        self.end_time = data.get('end_time')
        self.chat_id = data.get('chat_id')

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_identifier = db.Column(db.String(120), unique=True, nullable=False)
    events = db.relationship('Event', back_populates='chat', lazy='dynamic')

class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user = db.relationship('User', back_populates='attendees')
    event = db.relationship('Event', back_populates='attendees')
