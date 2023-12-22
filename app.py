from flask import Flask, jsonify
from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv
load_dotenv()

bot = Bot(token=getenv('TOKEN'))
#----------------------------------------------------------------
app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#----------------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

#----------------------------------------------------------------


db.init_app(app)
with app.app_context():
    db.create_all()

#----------------------------------------------------------------
    
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



@app.route('/')
def index():
    return 'Hello, world'

if __name__ == '__main__':
    app.run()