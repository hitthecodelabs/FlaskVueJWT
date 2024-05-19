### app.py

import os
import requests
from flask_cors import CORS
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import decode_token

from models import User
from extensions import db
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
from flask import Flask, jsonify, request, current_app, make_response
from werkzeug.security import generate_password_hash, check_password_hash

import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Adjust as needed for security
# CORS(app)  # This will allow all domains by default. For production, configure it to allow specific domains.
CORS(app, resources={r"/api/*": {"origins": "*"}}, 
     supports_credentials=True, 
     allow_headers=[
         "Content-Type", "Authorization", "X-Requested-With"
         ]
    )
# CORS(app, resources={r"/api/*": {"origins": ["https://yourtrusteddomain.com", "https://anothertrusteddomain.com"]}})

# Load configurations
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True  # Enable debug for development
# app.config['DEBUG'] = os.getenv('FLASK_DEBUG').lower() == 'true'  # Controlled by environment variable

app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  # JWT Secret Key
# Set up configuration for JWT to use cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to `True` in production if using HTTPS
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Consider enabling CSRF protection
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # Ensure the cookie is accessible across the entire app
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'  # Strict or Lax or None depending on your requirements
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'  # Ensure this is set to 'access_token'

db.init_app(app)  # Initialize the db instance with the app

migrate = Migrate(app, db)  # Initialize Flask-Migrate
jwt = JWTManager(app)  # Initialize JWT Manager

with app.app_context():
    db.create_all()  # This will create all tables

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        company_name = data.get('company_name')

        if not email or not password:
            logging.error('Missing registration data')
            return jsonify({'error': 'Missing email or password'}), 400

        if '@' not in email:
            logging.error('Invalid email format')
            return jsonify({'error': 'Invalid email format'}), 400

        password_hash = generate_password_hash(password)
        new_user = User( email=email, password_hash=password_hash, first_name=first_name, 
                        last_name=last_name, company_name=company_name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registration successful!'}), 200
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f'Registration Integrity Error: {e}')
        return jsonify({'error': 'Registration failed. The email may already be in use.'}), 409
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

        # Validate input presence
        if not email or not password:
            logging.error("Login attempt missing email or password")
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()

        # Check if user exists
        if not user:
            logging.error(f"Login attempt for non-existent user: {email}")
            return jsonify({'error': 'No such user exists'}), 404

        # Validate password and create access token
        if check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            response = make_response(jsonify({'message': 'Login successful!'}), 200)
            response.set_cookie('access_token', access_token, httponly=False, secure=False, samesite='Lax')
            logging.info(f"Login successful. Access Token set: {access_token}")
            decoded_token = decode_token(access_token)
            logging.info(f"Decoded token: {decoded_token}")
            return response
        else:
            logging.warning(f"Invalid password attempt for user: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500

@app.route('/set_test_cookie')
def set_test_cookie():
    resp = make_response("Cookie set")
    resp.set_cookie('test_cookie', 'test_value', httponly=True, secure=False, samesite='Lax')
    return resp

@app.route('/get_test_cookie')
def get_test_cookie():
    test_cookie = request.cookies.get('test_cookie', 'Not set')
    return f"Test cookie: {test_cookie}"

# Flask endpoint to validate session
@app.route('/api/validate_session', methods=['GET'])
@jwt_required(optional=True)
def validate_session():
    current_user = get_jwt_identity()
    logging.info(f"Current user from JWT: {current_user}")
    cookies = request.cookies
    logging.info(f"Received cookies: {cookies}")
    return jsonify({'isAuthenticated': bool(current_user)}), 200

@app.route('/api/check_session', methods=['GET'])
@jwt_required()
def check_session():
    user_id = get_jwt_identity()
    if user_id:
        logging.info(f"User ID from JWT: {user_id}")
        return jsonify({'message': 'User is logged in', 'user_id': user_id}), 200
    else:
        cookies = request.cookies
        logging.error(f"Failed to retrieve JWT: Current cookies: {cookies}")
        return jsonify({'message': 'Authentication failed'}), 401

@app.route('/api/debug/decode_jwt')
def debug_decode_jwt():
    access_token_cookie = request.cookies.get('access_token')
    if access_token_cookie:
        try:
            decoded_token = decode_token(access_token_cookie)
            user_identity = decoded_token['sub']
            return jsonify({
                "decoded": True,
                "user_identity": user_identity,
                "decoded_token": decoded_token
            }), 200
        except Exception as e:
            return jsonify({
                "decoded": False,
                "error": str(e)
            }), 400
    return jsonify({"error": "No access token found"}), 400

@app.route('/api/userdata', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        user_id = get_jwt_identity()  # This gets the identity of the JWT in the current context
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Return user-specific details including first_name, last_name, and company_name
        user_data = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'company_name': user.company_name
        }
        return jsonify(user_data), 200
    except Exception as e:
        logging.error(f'Error fetching user data: {e}')
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logged out successfully'}), 200)
    response.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax', secure=False)
    # response.set_cookie('access_token', '', expires=0)  # Clear the access token cookie
    return response

@app.route('/api/save_api_key', methods=['POST'])
@jwt_required()
def save_api_key():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        api_key = data.get('api_key')
        jira_domain = data.get('jira_domain')
        jira_email = data.get('jira_email')

        logging.info(f"Received API Key: {api_key}")
        logging.info(f"Received Jira Domain: {jira_domain}")
        logging.info(f"Received Jira Email: {jira_email}")

        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        user = db.session.get(User, user_id)
        if user:
            user.api_key = api_key
            user.jira_domain = jira_domain
            user.jira_email = jira_email
            db.session.commit()
            logging.info(f"Saved API key and Jira information for user ID: {user_id}")
            return jsonify({'message': 'API key and Jira information saved successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        logging.error(f'Error saving API key: {e}')
        return jsonify({'error': 'Failed to save API key', 'message': str(e)}), 500


@app.route('/api/get_api_key', methods=['GET'])
@jwt_required()
def get_api_key():
    try:
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user and user.api_key:
            return jsonify({
                'api_key': user.api_key,
                'jira_domain': user.jira_domain,
                'jira_email': user.jira_email
            }), 200
        return jsonify({'message': 'API key not found'}), 404
    except Exception as e:
        logging.error(f'Error fetching API key: {e}')
        return jsonify({'error': 'Failed to fetch API key', 'message': str(e)}), 500

@app.route('/api/jira_user_info', methods=['GET'])
@jwt_required()
def jira_user_info():
    logging.info("Accessing /api/jira_user_info")
    try:
        user_id = get_jwt_identity()
        logging.info(f"User ID: {user_id}")
        user = db.session.get(User, user_id)
        if user:
            logging.info(f"Retrieved user: {user.email}")
            logging.info(f"API Key: {user.api_key}")
            logging.info(f"Jira Domain: {user.jira_domain}")
            logging.info(f"Jira Email: {user.jira_email}")
        if user and user.api_key and user.jira_domain and user.jira_email:
            response = jira_api_request(user.jira_domain, user.jira_email, user.api_key, 'myself')
            logging.info("Jira API request successful")
            return jsonify(response), 200
        logging.warning("Jira information not found")
        return jsonify({'message': 'Jira information not found'}), 404
    except Exception as e:
        logging.error(f'Error fetching Jira user info: {e}')
        return jsonify({'error': 'Failed to fetch Jira user info', 'message': str(e)}), 500

def jira_api_request(jira_domain, jira_email, jira_api_token, endpoint):
    url = f"https://{jira_domain}.atlassian.net/rest/api/3/{endpoint}"
    auth = HTTPBasicAuth(jira_email, jira_api_token)
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, auth=auth, 
                            verify=True
                            )
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}", "details": response.text}

@app.route('/')
def hello():
    return jsonify({'message': 'Hello world!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True, threaded=True) ### debug
    # app.run(host='0.0.0.0', port=5000, use_reloader=True, threaded=True) ### prod
