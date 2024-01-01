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
#----------------------------------------------------------------


if __name__ == '__main__':
    app.run()