# models.py
from db import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="pending")  # pending, confirmed, canceled
    payment_status = db.Column(db.String(50), default="unpaid")  # unpaid, paid

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id
