from db import db

class Event(db.Model):
    __tablename__ = "events"  #   Ensure table name is explicitly set

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "date": self.date.isoformat()
        }
