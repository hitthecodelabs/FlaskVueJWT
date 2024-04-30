### app.py

import os
from flask_cors import CORS
from flask_migrate import Migrate
from flask import Flask, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from extensions import db  # Import the SQLAlchemy instance
from models import User

import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Adjust as needed for security
CORS(app)  # This will allow all domains by default. For production, configure it to allow specific domains.

# Load configurations
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  # JWT Secret Key
app.config['DEBUG'] = True  # Enable debug for development

db.init_app(app)  # Initialize the db instance with the app

migrate = Migrate(app, db)  # Initialize Flask-Migrate
jwt = JWTManager(app)  # Initialize JWT Manager

with app.app_context():
    db.create_all()  # This will create all tables

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logging.debug(f'Received registration data: {data}')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            logging.error('Missing registration data')
            return jsonify({'error': 'Missing username, email, or password'}), 400

        if '@' not in email:
            logging.error('Invalid email format')
            return jsonify({'error': 'Invalid email format'}), 400

        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registration successful!'}), 200
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f'Registration Integrity Error: {e}')
        return jsonify({'error': 'Registration failed. The username or email may already be in use.'}), 409
    except Exception as e:
        db.session.rollback()
        logging.error(f'Registration Error: {e}')
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    logging.debug("Login request received with data: %s", request.json)
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'No such user exists'}), 404

        if check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful!', 'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        current_app.logger.error(f'Login error: {e}')
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500
    
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/userdata', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        user_id = get_jwt_identity()  # This gets the identity of the JWT in the current context
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Assuming you want to return some user-specific details
        user_data = {
            'username': user.username,
            'email': user.email,
            # Add other fields as necessary
        }
        return jsonify(user_data), 200
    except Exception as e:
        logging.error(f'Error fetching user data: {e}')
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

@app.route('/')
def hello():
    return jsonify({'message': 'Hello world!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True, threaded=True)

# '{"username": "newuser9", "email": "newuser9@example.com", "password": "strongpassword9"}'
# newuser8 newuser8@example.com strongpassword8
# newuser8 newuser8@example.com strongpassword8
# newuser9 newuser9@example.com strongpassword9
# newuser91 newuser91@example.com strongpassword91
# newuser92 newuser92@example.com strongpassword92
# newuser93 newuser93@example.com strongpassword93

# 16:27, Breaking Bad episode

### https://api.telegram.org/bot6947652517:AAH8HosWkhyUWaMXgTJ8Sxes2QUz5nCRKTw/getupdates
### https://one.google.com/u/1/explore-plan/gemini-advanced?pageId=none&g1_landing_page=65

# happyfox.com/help-desk-ticketing-system
# freshworks.com/freshservice
# knots.io
# pythia.cc
