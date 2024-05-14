
## Flask Backend Application

This is a Flask backend application with user authentication, registration, and session management using JSON Web Tokens (JWT).

### Setup

1. **Environment Variables**: 
   Create a `.env` file in the `backend` directory with the following environment variables:
   ```
   DB_USER=<your_database_username>
   DB_PASSWORD=<your_database_password>
   DB_HOST=<your_database_host>
   DB_PORT=<your_database_port>
   DB_NAME=<your_database_name>
   SECRET_KEY=<your_jwt_secret_key>
   ```

2. **Install Dependencies**: 
   Run the following command to install the necessary dependencies:
   ```
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   Initialize the database and run migrations:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Start the Application**:
   Run the application using the following command:
   ```
   flask run
   ```

### Application Structure

- **app.py**: Main application file where the Flask app is initialized and routes are defined.
- **config.py**: Configuration file for setting up different environments (development, production, etc.).
- **extensions.py**: File to initialize and configure Flask extensions like SQLAlchemy, Migrate, etc.
- **migrations/**: Directory for database migration files managed by Alembic.
- **models.py**: Defines database models.
- **requirements.txt**: Lists all the dependencies needed for the backend.
- **utils.py**: Utility functions and helpers for the backend.

### Endpoints

- **User Registration**: 
  - `POST /api/register`: Register a new user with email, password, and optional details.

- **User Login**:
  - `POST /api/login`: Authenticate user and set a JWT in a cookie.

- **Session Validation**:
  - `GET /api/validate_session`: Check if the user is authenticated based on the JWT.
  - `GET /api/check_session`: Ensure the user is logged in and retrieves their ID from the JWT.

- **User Data**:
  - `GET /api/userdata`: Returns user-specific information based on their JWT identity.

- **User Logout**:
  - `POST /api/logout`: Clear the JWT cookie to log out the user.

- **Miscellaneous**:
  - `GET /set_test_cookie`: Sets a test cookie.
  - `GET /get_test_cookie`: Retrieves the value of the test cookie.
  - `GET /api/debug/decode_jwt`: Decodes and returns information about the JWT from the cookie.
  - `GET /`: Returns a simple "Hello world!" message.

### Notes

- **CORS Configuration**:
  - Configured to allow all origins for development purposes. For production, configure it to allow specific trusted domains.

- **JWT Configuration**:
  - JWT is set up to use cookies for secure storage. Adjust settings for secure cookies and CSRF protection as needed for production.

- **Logging**:
  - Logging is configured to output debug information for development purposes. Adjust logging levels as needed for production.
