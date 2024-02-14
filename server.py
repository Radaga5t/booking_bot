from flask import jsonify, request
from models import db, User, Event , Attendee
from datetime import datetime
import logging

def register_routs(app):
    @app.after_request
    def apply_content_type(response):
        response.headers["Content-Type"] = "application/json"
        return response

    @app.route('/users/', methods=['GET'])
    def get_users():
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 
                      'admin': user.admin} for user in users]
        return jsonify({'users': user_list})
    
    @app.route('/events', methods=['GET'])
    def get_events():
        events = Event.query.all()
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'start_time': event.start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                'end_time': event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return jsonify(events_list), 200

    @app.route('/events/<int:user_id>', methods=['GET'])
    def get_events_by_user(user_id):
        
        event_ids = db.session.query(Attendee.event_id).filter_by(user_id=user_id).all()
        event_ids = [e[0] for e in event_ids]
        
        events = Event.query.filter(Event.id.in_(event_ids)).order_by(Event.id).all()
        
        events_data = []
        for event in events:
            event_data = {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat()
            }
            events_data.append(event_data)
        
        return jsonify(events_data)

    @app.route('/events', methods=['POST'])
    def create_event():
        data = request.get_json()
        
        try:
            user_id = data['user_id'] # он должен где то получить user_id
            title = data['title']
            description = data['description']
            start_time = datetime.fromisoformat(data['start_time']) if 'start_time' in data else datetime.utcnow()
            end_time = datetime.fromisoformat(data['end_time']) if 'end_time' in data else datetime.utcnow()
        
        except (KeyError, TypeError, ValueError) as e:
            return jsonify({'error': 'Invalid or missing data'}), 400

        new_event = Event(title=title, description=description, start_time=start_time, end_time=end_time)
        db.session.add(new_event)
        db.session.commit()

        attendee = Attendee(user_id=user_id, event_id=new_event.id)
        db.session.add(attendee)
        db.session.commit()
        return jsonify({'message': 'Event created successfully', 'event_id': new_event.id}), 201
    
    #------------------------------------------------


    '''
    @app.route('/event/<int:event_id>', methods=['PATCH'])
    def update_event(event_id):
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        data = request.get_json()

        title = data.get('title', event.title)
        description = data.get('description', event.description)
        start_time = data.get('start_time', event.start_time)
        end_time = data.get('end_time', event.end_time)

        event.title = title
        event.description = description
        event.start_time = start_time
        event.end_time = end_time
        
        db.session.commit()
        
        return jsonify({'success': 'Event updated'}), 200

    @app.route('/events/<int:event_id>', methods=['PATCH'])
    def update_event(event_id):
            event = Event.query.filter_by(id=event_id).first()
            data = request.get_json()

            if not event:
                return jsonify({'message': 'Event not found'}), 404

            title = data.get('title', event.title)
            description = data.get('description', event.description)
            start_time = data.get('start_time', event.start_time.isoformat())
            end_time = data.get('end_time', event.end_time.isoformat())

            event.title = title
            event.description = description

            if 'start_time' in data:
                event.start_time = datetime.fromisoformat(start_time)
            if 'end_time' in data:
                event.end_time = datetime.fromisoformat(end_time)

            db.session.commit()
            return jsonify({'message': 'Event updated successfully'}), 200
    '''



