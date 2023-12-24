from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate


#----------------------------------------------------------
# Загрузка переменных окружения
#----------------------------------------------------------
load_dotenv()

#---------- ------------------------------------------------
# Инициализация бота, приложения и базы данных
#----------------------------------------------------------
bot = Bot(token=getenv('TOKEN'))
app = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate(app, db)


app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#----------------------------------------------------------
# Модели Базы данных
#----------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50))
    
    events = db.relationship('Attendee', back_populates='user')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    attendees = db.relationship('Attendee', back_populates='event')


class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
   
    user = db.relationship('User', back_populates='events')
    event = db.relationship('Event', back_populates='attendees')


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    event = db.relationship('Event')

#----------------------------------------------------------
# Инициализация приложения и базы данных
#----------------------------------------------------------
db.init_app(app)

with app.app_context():
    db.create_all()

#----------------------------------------------------------
# Роут для корневого URL
#----------------------------------------------------------
@app.route('/')
def index():
    return 'pisa_popa_chelen'


#----------------------------------------------------------
# Запуск приложения
#----------------------------------------------------------
if __name__ == '__main__':
    app.run()
