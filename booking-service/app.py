from flask import Flask
from db import init_db, db
from routes import init_routes

app = Flask(__name__)

# Initialize Database
init_db(app)

# Register Routes
init_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True,port=5003)
