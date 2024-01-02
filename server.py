from flask import jsonify, request
from app import app, db, User, Event, Chat, Attendee
#----------------------------------------------------------------User points
# GET /users/ - список пользователей
@app.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'is_admin': user.is_admin} for user in users]
    return jsonify({'users': user_list})

# POST /users/ - создать пользователя
@app.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()

    if 'username' not in data:
        return jsonify({'error': 'Требуется имя пользователя'}), 400

    new_user = User(username=data['username'], is_admin=data.get('is_admin', False))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Пользователь успешно создан', 'id': new_user.id})
#----------------------------------------------------------------Eventspoint
# GET /events/ - список ивентов
@app.route('/events/', methods=['GET'])
def get_events():
    events = Event.query.all()
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

    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'start_time' in data:
        event.start_time = data['start_time']
    if 'end_time' in data:
        event.end_time = data['end_time']

    db.session.commit()

    return jsonify({'message': 'Меропрриятие успешно обновлено'})
#----------------------------------------------------------------Chatpoints
# GET /chats/ - список чатов
@app.route('/chats/', methods=['GET'])
def get_chats():
    chats = Chat.query.all()
    chat_list = [{'id': chat.id, 'chat_identifier': chat.chat_identifier} for chat in chats]
    return jsonify({'chats': chat_list})

# POST /chats/ - создать чат
@app.route('/chats/', methods=['POST'])
def create_chat():
    data = request.get_json()

    if 'chat_identifier' not in data:
        return jsonify({'error': 'Требуется идентификатор чата'}), 400

    new_chat = Chat(chat_identifier=data['chat_identifier'])
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({'message': 'Чат успешно добавлен', 'id': new_chat.id})

# GET /chats/:id - детали конкретного чата по id
@app.route('/chats/<int:chat_id>/', methods=['GET'])
def get_chat(chat_id):
    chat = Chat.query.get(chat_id)

    if not chat:
        return jsonify({'error': 'Чат не существует'}), 404

    chat_details = {'id': chat.id, 'chat_identifier': chat.chat_identifier}
    return jsonify(chat_details)

# PATCH /chats/:id - обновить конкретный чат
@app.route('/chats/<int:chat_id>/', methods=['PATCH'])
def update_chat(chat_id):
    chat = Chat.query.get(chat_id)

    if not chat:
        return jsonify({'error': 'Чат не существует'}), 404

    data = request.get_json()

    if 'chat_identifier' in data:
        chat.chat_identifier = data['chat_identifier']

    db.session.commit()

    return jsonify({'message': 'Чат успешно обновлен'})
#-------------------------------------------------------------Attendee
# GET /attendees/ - список участников
@app.route('/attendees/', methods=['GET'])
def get_attendees():
    attendees = Attendee.query.all()
    attendee_list = [{'id': attendee.id, 'user_id': attendee.user_id, 'event_id': attendee.event_id} for attendee in attendees]
    return jsonify({'attendees': attendee_list})

# POST /attendees/ - добавить участника
@app.route('/attendees/', methods=['POST'])
def add_attendee():
    data = request.get_json()

    if 'user_id' not in data or 'event_id' not in data:
        return jsonify({'error': 'User ID and Event ID are required'}), 400

    user = User.query.get(data['user_id'])
    event = Event.query.get(data['event_id'])

    if not user or not event:
        return jsonify({'error': 'User or Event not found'}), 404

    new_attendee = Attendee(user_id=data['user_id'], event_id=data['event_id'])
    db.session.add(new_attendee)
    db.session.commit()

    return jsonify({'message': 'Attendee added successfully', 'id': new_attendee.id})

# GET /attendees/:id - детали конкретного участника по id
@app.route('/attendees/<int:attendee_id>/', methods=['GET'])
def get_attendee(attendee_id):
    attendee = Attendee.query.get(attendee_id)

    if not attendee:
        return jsonify({'error': 'Attendee not found'}), 404

    attendee_details = {'id': attendee.id, 'user_id': attendee.user_id, 'event_id': attendee.event_id}
    return jsonify(attendee_details)

# DELETE /attendees/:id - удалить участника
@app.route('/attendees/<int:attendee_id>/', methods=['DELETE'])
def delete_attendee(attendee_id):
    attendee = Attendee.query.get(attendee_id)

    if not attendee:
        return jsonify({'error': 'Attendee not found'}), 404

    db.session.delete(attendee)
    db.session.commit()

    return jsonify({'message': 'Attendee deleted successfully'})
#----------------------------------------------------------------
if __name__ == '__main__':
    app.run()