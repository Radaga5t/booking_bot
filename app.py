from flask import Flask, jsonify , request , abort
from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv
from flask_migrate import Migrate
from models import db, User, Event, Chat, Attendee
from server import *
#---------------------------------------------------------------Variables
load_dotenv()
bot = Bot(token=getenv('TOKEN'))

app = Flask(__name__)
migrate = Migrate(app, db)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#----------------------------------------------------------------Models
db.init_app(app)

with app.app_context():
    db.create_all()
#----------------------------------------------------------------Mistakes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Внутренняя ошибка сервера"), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify(error="Непредвиденная ошибка"), 500
#----------------------------------------------------------------
if __name__ == '__main__':
    app.run()
