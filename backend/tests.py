### test.py

import json
import unittest
from models import User
from app import app, db
from http.cookies import SimpleCookie

def parse_cookies(response):
    cookies = {}
    cookie_headers = response.headers.getlist('Set-Cookie')
    for header in cookie_headers:
        parts = header.split(';')[0].split('=')
        if len(parts) == 2:
            cookies[parts[0]] = parts[1]
    return cookies

class BasicTests(unittest.TestCase):

    def setUp(self):
        # Establish an application context
        self.ctx = app.app_context()
        self.ctx.push()

        # Sets up a test client
        app.config['TESTING'] = True
        self.app = app.test_client(use_cookies=True)  # Make sure to handle cookies

        # Setup database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/test_database'
        db.create_all()  # Create tables for the test database

    def tearDown(self):
        # Drop all data after tests
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_database_connection(self):
        """ Test database connectivity and ability to add and retrieve data. """
        user = User(email="testuser@example.com", password_hash="hash", first_name="Test", last_name="User", company_name="TestCorp")
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(email="testuser@example.com").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "testuser@example.com")

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        # Simulate registration
        test_user = {
            "email": "test@example.com",
            "password": "testpass",
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Doe Inc"
        }
        response = self.app.post('/api/register',
                                 data=json.dumps(test_user).encode('utf-8'),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration successful!', response.data.decode('utf-8'))

        # Verify that the user was stored in the database with the correct details
        user = User.query.filter_by(email="test@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.company_name, "Doe Inc")

    def test_invalid_user_registration(self):
        # Simulate registration with invalid email
        test_user = {
            "email": "invalidemail",
            "password": "testpass"
        }
        response = self.app.post('/api/register',
                                 data=json.dumps(test_user).encode('utf-8'),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_non_existent_user_login(self):
        """ Test login with non-existent user. """
        login_data = {
            "email": "nonexistent@example.com",
            "password": "nopassword"
        }
        response = self.app.post('/api/login',
                                data=json.dumps(login_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('No such user exists', response.data.decode('utf-8'))

    def test_session_validation(self):
        # Register and login to create a session
        self.test_valid_user_registration()
        login_response = self.app.post('/api/login', json={
            "email": "test@example.com",
            "password": "testpass"
        }, follow_redirects=True)
        print("Login Response:", login_response.data.decode('utf-8'))
        print("Login Response Headers:", login_response.headers)
        print("Login Response Cookies:", login_response.headers.get('Set-Cookie'))

        # Extract cookies from login response
        cookies = parse_cookies(login_response)
        cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])
        print("Cookie Header Used in Request:", cookie_header)

        # Validate session before logout
        session_check_response = self.app.get('/api/validate_session', headers={"Cookie": cookie_header})
        print("Session Check Response Status:", session_check_response.status_code)
        print("Session Check Response Body:", session_check_response.data.decode('utf-8'))
        session_data = json.loads(session_check_response.data.decode('utf-8'))
        self.assertTrue(session_data.get('isAuthenticated', False))

        # Perform logout
        logout_response = self.app.post('/api/logout', headers={"Cookie": cookie_header})
        print("Logout Response:", logout_response.data.decode('utf-8'))

        # Check session after logout should not be authenticated
        session_check_response_after_logout = self.app.get('/api/validate_session', headers={"Cookie": cookie_header})
        print("Session Check After Logout:", session_check_response_after_logout.data.decode('utf-8'))
        session_data_after_logout = json.loads(session_check_response_after_logout.data.decode('utf-8'))
        self.assertFalse(session_data_after_logout.get('isAuthenticated', True), "Session should not be authenticated after logout.")

if __name__ == "__main__":
    unittest.main()
