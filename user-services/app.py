from flask import Flask, request, jsonify
from db import app, db, logger
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

# ✅ Global Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f"404 Error: {request.url} not found")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"500 Error at {request.url}: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

# ✅ User Registration with Error Handling
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        if not data.get("name") or not data.get("email") or not data.get("password"):
            return jsonify({"error": "All fields are required"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 409

        hashed_password = generate_password_hash(data['password'])
        user = User(name=data["name"], email=data["email"], password=hashed_password)
        db.session.add(user)
        db.session.commit()

        logger.info(f"New user registered: {user.email}")
        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        logger.error("Database integrity error")
        return jsonify({"error": "Database integrity error"}), 500
    except Exception as e:
        logger.exception("Unexpected error during registration")
        return jsonify({"error": str(e)}), 500

# ✅ User Login with Logging
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
            logger.warning(f"Failed login attempt for email: {email}")
            return jsonify({"error": "Invalid email or password"}), 401

        login_user(user)
        logger.info(f"User logged in: {user.email}")
        return jsonify({"message": "Login successful"}), 200

    except Exception as e:
        logger.exception("Unexpected error during login")
        return jsonify({"error": str(e)}), 500

# ✅ Get User Profile with Logging
@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    try:
        logger.info(f"Fetching profile for user: {current_user.email}")
        return jsonify({
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        }), 200

    except Exception as e:
        logger.exception("Unexpected error while fetching profile")
        return jsonify({"error": str(e)}), 500

# ✅ Logout User with Logging
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logger.info(f"User logged out: {current_user.email}")
        logout_user()
        return jsonify({"message": "Logout successful"}), 200

    except Exception as e:
        logger.exception("Unexpected error during logout")
        return jsonify({"error": str(e)}), 500

# ✅ Update User Profile with Error Handling
@app.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    try:
        data = request.json
        if "name" in data:
            current_user.name = data["name"]
        if "email" in data:
            if User.query.filter_by(email=data["email"]).first():
                return jsonify({"error": "Email already in use"}), 409
            current_user.email = data["email"]

        db.session.commit()
        logger.info(f"User profile updated: {current_user.email}")
        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        logger.exception("Unexpected error during profile update")
        return jsonify({"error": str(e)}), 500

# ✅ Delete User Profile with Logging
@app.route('/profile', methods=['DELETE'])
@login_required
def delete_profile():
    try:
        db.session.delete(current_user)
        db.session.commit()
        logger.info(f"User deleted: {current_user.email}")
        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        logger.exception("Unexpected error during profile deletion")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
