from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

load_dotenv()
TELEGRAM_BOT_TOKEN = getenv('bot_token')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://booking_bot:252752@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Ваша модель User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50))

# Создание всех таблиц
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "pisa_popa_chelen"

if __name__ == '__main__':
    app.run()