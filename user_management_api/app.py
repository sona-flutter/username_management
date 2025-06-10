from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from models import db, User
from schemas import ma, UserSchema
from datetime import datetime
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database configuration - Using SQLite for easier setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and marshmallow
db.init_app(app)
ma.init_app(app)

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Root route
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to User Management API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "emails": "/users/emails",
            "clear_all": "/users/clear",
            "swagger_ui": "/swagger",
            "api_docs": "/static/swagger.json"
        },
        "available_methods": {
            "GET /users": "Get all users",
            "POST /users": "Create a new user",
            "GET /users/<id>": "Get user by ID",
            "PUT /users/<id>": "Update user by ID",
            "DELETE /users/<id>": "Delete user by ID",
            "GET /users/emails": "Get all existing emails",
            "DELETE /users/clear": "Clear all users (for testing)"
        }
    })

# CRUD APIs
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not data.get('user_email'):
            return jsonify({"error": "user_email is required"}), 400
        
        if not data.get('user_name'):
            return jsonify({"error": "user_name is required"}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(user_email=data['user_email']).first()
        if existing_user:
            return jsonify({"error": f"User with email '{data['user_email']}' already exists"}), 400
        
        # Handle date conversion if provided
        if 'user_date_of_birth' in data and data['user_date_of_birth']:
            try:
                # Convert string date to datetime.date object
                date_str = data['user_date_of_birth']
                if isinstance(date_str, str):
                    data['user_date_of_birth'] = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        
        # Return the created user data
        user_schema = UserSchema()
        return jsonify({
            "message": "User created successfully!", 
            "user_id": user.user_id,
            "user": user_schema.dump(user)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        
        # Handle specific database errors
        if "UNIQUE constraint failed: users.user_email" in error_msg:
            return jsonify({"error": "Email address already exists. Please use a different email."}), 400
        elif "NOT NULL constraint failed" in error_msg:
            return jsonify({"error": "Required field is missing. Please check user_name and user_email."}), 400
        else:
            return jsonify({"error": f"Database error: {error_msg}"}), 400

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        # Handle date conversion if provided
        if 'user_date_of_birth' in data and data['user_date_of_birth']:
            try:
                # Convert string date to datetime.date object
                date_str = data['user_date_of_birth']
                if isinstance(date_str, str):
                    data['user_date_of_birth'] = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({"message": "User updated!"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted!"})

# Helper routes
@app.route('/users/emails', methods=['GET'])
def get_existing_emails():
    """Get all existing email addresses"""
    users = User.query.with_entities(User.user_email, User.user_name, User.user_id).all()
    emails = [{"user_id": user.user_id, "user_name": user.user_name, "user_email": user.user_email} for user in users]
    return jsonify({
        "existing_emails": emails,
        "count": len(emails)
    })

@app.route('/users/clear', methods=['DELETE'])
def clear_all_users():
    """Clear all users from database (for testing)"""
    try:
        count = User.query.count()
        User.query.delete()
        db.session.commit()
        return jsonify({
            "message": f"All {count} users have been deleted from the database",
            "deleted_count": count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    # Make accessible from other machines by setting host='0.0.0.0'
    app.run(debug=True, host='0.0.0.0', port=5000)
