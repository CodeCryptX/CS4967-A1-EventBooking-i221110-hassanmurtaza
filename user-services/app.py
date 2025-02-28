from flask import Flask, request, jsonify
from db import app, db
from models import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
import os

# Ensure the database tables are created inside the application context
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        if not data.get("name") or not data.get("email") or not data.get("password"):
            return jsonify({"error": "All fields are required"}), 400

        hashed_password = generate_password_hash(data['password'])
        user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecret")  # Change this in production!
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "token": access_token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)