from os import getenv
from telegram import Bot
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from models import db, User, Event, Chat, Attendee 



#----------------------------------------------------------
# Загрузка переменных окружения
#----------------------------------------------------------
load_dotenv()

#---------- ------------------------------------------------
# Инициализация бота, приложения и базы данных
#----------------------------------------------------------
bot = Bot(token=getenv('TOKEN'))
app = Flask(__name__)


migrate = Migrate(app, db)


app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
