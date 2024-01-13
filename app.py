from flask import Flask, jsonify , request , abort
from telegram import Bot
from flask_migrate import Migrate
from models import db, User, Event, Chat, Attendee
from dotenv import load_dotenv
from os import getenv
#---------------------------------------------------------------Variables
load_dotenv()
#bot = Bot(token=getenv('TOKEN'))

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
#----------------------------------------------------------------Server settings
@app.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'is_admin': user.is_admin} for user in users]
    return jsonify({'users': user_list})

# GET /events/ - список ивентов
@app.route('/events/', methods=['GET'])
def get_events():
    events = Event.query.all() #фильтрация по юзеру
    event_list = [{'id': event.id, 'title': event.title, 'description': event.description,
                   'start_time': event.start_time.isoformat(), 'end_time': event.end_time.isoformat()} for event in events]
    return jsonify({'events': event_list})

# POST /events/ - создать ивент 
@app.route('/events/', methods=['POST'])
def create_event():
    data = request.get_json()

    if 'title' not in data:
        return jsonify({'error': 'Требуется название'}), 400

    new_event = Event(title=data['title'], description=data.get('description'),
                      start_time=data.get('start_time'), end_time=data.get('end_time'))
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Мероприятие успешно создано', 'id': new_event.id})

# GET /events/:id - детали конкретного ивента по id
@app.route('/events/<int:event_id>/', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({'error': 'Мероприятие не нашлось'}), 404

    event_details = {'id': event.id, 'title': event.title, 'description': event.description,
                     'start_time': event.start_time.isoformat(), 'end_time': event.end_time.isoformat()}
    return jsonify(event_details)

# PATCH /events/:id - обновить конкретный эвент
@app.route('/events/<int:event_id>/', methods=['PATCH'])
def update_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({'error': 'Мероприятие не нашлось'}), 404

    data = request.get_json()

    if 'title' in data: # переделать 
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'start_time' in data:
        event.start_time = data['start_time']
    if 'end_time' in data:
        event.end_time = data['end_time']

    db.session.commit()

    return jsonify({'message': 'Меропрриятие успешно обновлено'})
# GET /chats/ - список чатов
@app.route('/chats/', methods=['GET'])
def get_chats():
    chats = Chat.query.all()
    chat_list = [{'id': chat.id, 'chat_identifier': chat.chat_identifier} for chat in chats]
    return jsonify({'chats': chat_list})
#----------------------------------------------------------------Launcher
if __name__ == '__main__':
    app.run()
