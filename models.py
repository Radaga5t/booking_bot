from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Добавили связывание с моделью Attendee для получения всех участников с данным пользователем
    attendees = db.relationship('Attendee', back_populates='user', lazy='dynamic')
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    # Связь модели события с моделью чата
    chat = db.relationship('Chat', back_populates='events')
    # Добавили связывание с моделью Attendee для получения всех участников события
    attendees = db.relationship('Attendee', back_populates='event', lazy='dynamic')

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_identifier = db.Column(db.String(120), unique=True, nullable=False)
    # back_populates здесь более точное, оно позволяет связать две модели в обе стороны
    events = db.relationship('Event', back_populates='chat', lazy='dynamic')

class Attendee(db.Model):  # Исправленное название класса
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    # Устанавливаем двусторонне связывание между User и Attendee, Event и Attendee
    user = db.relationship('User', back_populates='attendees')
    event = db.relationship('Event', back_populates='attendees')
