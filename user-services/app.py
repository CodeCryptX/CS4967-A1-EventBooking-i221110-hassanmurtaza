from flask import Flask, request, jsonify
from db import app, db
from models import User
from werkzeug.security import generate_password_hash

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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5001)
