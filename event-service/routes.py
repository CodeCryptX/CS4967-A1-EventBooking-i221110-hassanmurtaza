import logging
from flask import request, jsonify
from flask_restful import Resource, Api
from db import app, db
from models import Event
from datetime import datetime
import pytz

# ✅ Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("event_service.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

api = Api(app)  # Initialize Flask-RESTful API

# 📌 Create an Event (Enhanced with Logging ✅)
class CreateEvent(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not all(k in data for k in ("name", "location", "date")):
                logging.warning("CreateEvent: Missing required fields")
                return {"error": "Missing required fields"}, 400

            # ✅ Parse timestamp properly
            try:
                date_obj = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
            except ValueError:
                logging.error("CreateEvent: Invalid date format")
                return {"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SSZ'"}, 400

            event = Event(name=data["name"], location=data["location"], date=date_obj)
            db.session.add(event)
            db.session.commit()

            logging.info(f"Event Created: {event.id} - {event.name}")
            return {"message": "Event created successfully", "event_id": event.id}, 201

        except Exception as e:
            logging.exception("CreateEvent: Unexpected error")
            return {"error": "Internal server error"}, 500

# 📌 Get All Events
class GetEvents(Resource):
    def get(self):
        try:
            events = Event.query.all()
            logging.info(f"GetEvents: {len(events)} events fetched")
            return jsonify([event.to_json() for event in events])
        except Exception as e:
            logging.exception("GetEvents: Unexpected error")
            return {"error": "Internal server error"}, 500

# 📌 Get Single Event by ID
class GetEvent(Resource):
    def get(self, event_id):
        try:
            event = Event.query.get(event_id)
            if event:
                logging.info(f"GetEvent: Event {event_id} fetched")
                return jsonify(event.to_json())
            logging.warning(f"GetEvent: Event {event_id} not found")
            return {"message": "Event not found"}, 404
        except Exception as e:
            logging.exception(f"GetEvent: Error fetching event {event_id}")
            return {"error": "Internal server error"}, 500

# 📌 Update Event
class UpdateEvent(Resource):
    def put(self, event_id):
        try:
            event = Event.query.get(event_id)
            if not event:
                logging.warning(f"UpdateEvent: Event {event_id} not found")
                return {"message": "Event not found"}, 404

            data = request.get_json()
            event.name = data.get("name", event.name)
            event.location = data.get("location", event.location)

            # ✅ Handle Date Parsing Properly
            if "date" in data:
                try:
                    event.date = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
                except ValueError:
                    logging.error(f"UpdateEvent: Invalid date format for event {event_id}")
                    return {"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SSZ'"}, 400

            db.session.commit()
            logging.info(f"UpdateEvent: Event {event_id} updated")
            return {"message": "Event updated successfully", "event": event.to_json()}

        except Exception as e:
            logging.exception(f"UpdateEvent: Unexpected error while updating event {event_id}")
            return {"error": "Internal server error"}, 500

# 📌 Delete Event
class DeleteEvent(Resource):
    def delete(self, event_id):
        try:
            event = Event.query.get(event_id)
            if not event:
                logging.warning(f"DeleteEvent: Event {event_id} not found")
                return {"message": "Event not found"}, 404

            db.session.delete(event)
            db.session.commit()
            logging.info(f"DeleteEvent: Event {event_id} deleted")
            return {"message": "Event deleted successfully"}

        except Exception as e:
            logging.exception(f"DeleteEvent: Unexpected error while deleting event {event_id}")
            return {"error": "Internal server error"}, 500

# ✅ Register API Endpoints Correctly
api.add_resource(CreateEvent, "/events")
api.add_resource(GetEvents, "/events")
api.add_resource(GetEvent, "/events/<int:event_id>")
api.add_resource(UpdateEvent, "/events/<int:event_id>")
api.add_resource(DeleteEvent, "/events/<int:event_id>")
