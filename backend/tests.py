import unittest
import json
from app import app, db
from models import User

class BasicTests(unittest.TestCase):

    def setUp(self):
        # Establish an application context
        self.ctx = app.app_context()
        self.ctx.push()

        # Sets up a test client
        app.config['TESTING'] = True
        app.config['DEBUG'] = True  # Enable debug to see more detailed errors
        self.app = app.test_client()

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
        user = User(username="testuser", email="testuser@example.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "testuser@example.com")

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        # Simulate registration
        test_user = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass"
        }
        response = self.app.post('/api/register',
                                 data=json.dumps(test_user, ensure_ascii=False).encode('utf-8'),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration successful!', response.data.decode('utf-8'))

    def test_invalid_user_registration(self):
        # Simulate registration with invalid email
        test_user = {
            "username": "testuser",
            "email": "invalidemail",
            "password": "testpass"
        }
        response = self.app.post('/api/register',
                                 data=json.dumps(test_user, ensure_ascii=False).encode('utf-8'),
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

if __name__ == "__main__":
    unittest.main()
