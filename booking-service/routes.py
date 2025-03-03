from flask import request, jsonify
from models import Booking
from db import db

def init_routes(app):
    @app.route("/book", methods=["POST"])
    def book_ticket():
        data = request.json
        if not data or "user_id" not in data or "event_id" not in data:
            return jsonify({"error": "Invalid request data"}), 400

        new_booking = Booking(user_id=data["user_id"], event_id=data["event_id"])
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"message": "Booking created", "booking_id": new_booking.id}), 201

    @app.route("/pay/<int:booking_id>", methods=["POST"])
    def make_payment(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        booking.payment_status = "paid"
        booking.status = "confirmed"
        db.session.commit()
        return jsonify({"message": "Payment successful", "booking_status": booking.status}), 200

    @app.route("/status/<int:booking_id>", methods=["GET"])
    def get_booking_status(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        return jsonify({
            "booking_id": booking.id,
            "status": booking.status,
            "payment_status": booking.payment_status
        }), 200
