from flask import request, jsonify
from flask_restful import Resource, Api
from db import app, db
from models import Event
from datetime import datetime
import pytz 

api = Api(app)  # Initialize Flask-RESTful API

# 📌 Create an Event (Fixed ✅)
class CreateEvent(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not all(k in data for k in ("name", "location", "date")):
                return {"error": "Missing required fields"}, 400

            # ✅ Parse timestamp properly
            date_obj = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)

            event = Event(
                name=data["name"],
                location=data["location"],
                date=date_obj
            )

            db.session.add(event)
            db.session.commit()

            return {"message": "Event created successfully"}, 201

        except ValueError:
            return {"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SSZ'"}, 400

        except Exception as e:
            return {"error": str(e)}, 500

# 📌 Get All Events
class GetEvents(Resource):
    def get(self):
        events = Event.query.all()
        return jsonify([event.to_json() for event in events])

# 📌 Get Single Event by ID
class GetEvent(Resource):
    def get(self, event_id):
        event = Event.query.get(event_id)
        if event:
            return jsonify(event.to_json())
        return {"message": "Event not found"}, 404

# 📌 Update Event (Fixed ✅)
class UpdateEvent(Resource):
    def put(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {"message": "Event not found"}, 404

        data = request.get_json()
        event.name = data.get("name", event.name)
        event.location = data.get("location", event.location)

        # ✅ Handle Date Parsing Properly
        if "date" in data:
            try:
                event.date = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
            except ValueError:
                return {"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SSZ'"}, 400

        db.session.commit()
        return {"message": "Event updated successfully", "event": event.to_json()}


# 📌 Delete Event
class DeleteEvent(Resource):
    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {"message": "Event not found"}, 404

        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted successfully"}

# ✅ Register API Endpoints Correctly
api.add_resource(CreateEvent, "/events")
api.add_resource(GetEvents, "/events")
api.add_resource(GetEvent, "/events/<int:event_id>")
api.add_resource(UpdateEvent, "/events/<int:event_id>")
api.add_resource(DeleteEvent, "/events/<int:event_id>")
