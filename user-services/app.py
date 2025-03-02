from flask import Flask, request, jsonify, render_template
from db import app, db
from models import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login if user is not authenticated

# Ensure the database tables are created inside the application context
with app.app_context():
    db.create_all()

# Load user for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

### ✅ 1️⃣ User Registration ###
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        if not data.get("name") or not data.get("email") or not data.get("password"):
            return jsonify({"error": "All fields are required"}), 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 409

        hashed_password = generate_password_hash(data['password'])
        user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

### ✅ 2️⃣ User Login (Session-Based) ###
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

        login_user(user)  # Create session for user
        return jsonify({"message": "Login successful"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

### ✅ 3️⃣ User Logout ###
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # End session
    return jsonify({"message": "Logout successful"}), 200

### ✅ 4️⃣ Get User Profile (Protected) ###
@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }), 200

### ✅ 5️⃣ Update User Profile ###
@app.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.json
    if "name" in data:
        current_user.name = data["name"]
    if "email" in data:
        current_user.email = data["email"]  # Ensure uniqueness in the database

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

### ✅ 6️⃣ Delete User Profile ###
@app.route('/profile', methods=['DELETE'])
@login_required
def delete_profile():
    db.session.delete(current_user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
