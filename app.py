from flask import Flask, jsonify
from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv
load_dotenv()
bot = Bot(token=getenv('TOKEN'))

#----------------------------------------------------------------SQLALchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#----------------------------------------------------------------Models

attendees = db.Table('attendees', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    events_attending = db.relationship('Event',secondary=attendees, back_populates="attendees")

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    attendees = db.relationship('User', secondary=attendees, back_populates='events_attending')

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_identifier = db.Column(db.String(120), unique=True, nullable=False)
    events = db.relationship('Event', backref='chat', lazy=True)

#----------------------------------------------------------------Table
    
db.init_app(app)
with app.app_context():
    db.create_all()

#----------------------------------------------------------------Error handling
    
# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404


# Обработчик ошибки 500
@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Внутренняя ошибка сервера"), 500


# Обработчик для неопределенных ошибок
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify(error="Непредвиденная ошибка"), 500

#----------------------------------------------------------------Flask
@app.route('/')
def index():
    return 'Hello, world'

if __name__ == '__main__':
    app.run()