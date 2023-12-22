from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask



load_dotenv()

bot = Bot(token=getenv('TOKEN'))
app = Flask(__name__)
db = SQLAlchemy()


app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Ваша модель User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50))

db.init_app(app)

# Создание всех таблиц
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'pisa_popa_chelen'

if __name__ == '__main__':
    app.run()