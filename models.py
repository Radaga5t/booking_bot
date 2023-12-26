from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_identifier = db.Column(db.String(120), unique=True, nullable=False)
    events = db.relationship('Event', backref='chat', lazy=True)

class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user = db.relationship('User', back_populates='events')
    event = db.relationship('Event', back_populates='attendees')
