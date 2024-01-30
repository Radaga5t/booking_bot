from flask import jsonify, request
from sqlalchemy.exc import IntegrityError



def register_routes(app, db, User, Event, Chat):
    @app.after_request
    def apply_content_type(response):
        response.headers["Content-Type"] = "application/json"
        return response
    
    @app.route('/users/', methods=['GET'])
    def get_users():
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 'is_admin': user.is_admin} for user in users]
        return jsonify({'users': user_list})

    @app.route('/events/', methods=['GET'])
    def get_events():
        user_id = request.args.get('user_id') 
        if user_id:
            try:
                user_id = int(user_id)
            except ValueError:
                return jsonify({'error': 'Неверный формат user_id'}), 400

            events = Event.query.filter_by(user_id=user_id).all()  
        else:
            events = Event.query.all() 

        event_list = [{'id': event.id, 'title': event.title, 'description': event.description,
                    'start_time': event.start_time.isoformat(), 'end_time': event.end_time.isoformat()} for event in events]
        return jsonify({'events': event_list})
 
    @app.route('/events/', methods=['POST'])
    def create_event():
        data = request.get_json()

        try:
            new_event = Event(data)
            db.session.add(new_event)
            db.session.commit()
            return jsonify({'message': 'Мероприятие успешно создано', 'id': new_event.id}), 201
        except IntegrityError as e:
            db.session.rollback()  # Откат изменений, если возникла ошибка
            return jsonify({'error': 'Отсутствует обязательное поле или нарушение уникальности данных.'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Произошла ошибка при создании мероприятия', 'details': str(e)}), 500

        
    @app.route('/events/<int:event_id>/', methods=['GET'])
    def get_event(event_id):
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'error': 'Мероприятие не нашлось'}), 404

        event_details = {'id': event.id, 'title': event.title, 'description': event.description,
                        'start_time': event.start_time.isoformat(), 'end_time': event.end_time.isoformat()}
        return jsonify(event_details)

    @app.route('/events/<int:event_id>/', methods=['PATCH'])
    def update_event(event_id):
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'error': 'Мероприятие не нашлось'}), 404

        data = request.get_json()

        allowed_fields = ['title', 'description', 'start_time', 'end_time']

        for field in allowed_fields:
            if field in data:
                setattr(event, field, data[field])

        db.session.commit()

        return jsonify({'message': 'Мероприятие успешно обновлено'})
