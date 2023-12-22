from flask import Flask
from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy
from telegram.ext import Updater, CommandHandler


from dotenv import load_dotenv
load_dotenv()


bot = Bot(token=getenv('bot_token'))

app = Flask(__name__)

#----------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('database_token')
db = SQLAlchemy(app)

# Модели SQLAlchemy (Пример пользователя)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=True)

    def repr(self):  # Исправлено здесь
        return '<User {}>'.format(self.telegram_id)
#----------------------------------------------------------------

@app.route('/')
def index():
    return 'Hello, world'

if __name__ == '__main__':
    app.run()