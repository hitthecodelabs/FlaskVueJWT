
# Landing Page

This is a full-stack application with a Flask backend and a Vue.js frontend. The backend handles user authentication, registration, and session management using JSON Web Tokens (JWT), while the frontend provides a user interface for interacting with these features.

## Backend

The backend is built with Flask and includes user authentication, registration, and session management using JWT.

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

## Frontend

The frontend is built with Vue.js and provides a user interface for interacting with the backend features.

### Setup

1. **Environment Variables**: 
   Create the following `.env` files in the `frontend` directory with the appropriate variables:
   - `.env`
   - `.env.local`
   - `.env.production`

   Example content for `.env`:
   ```
   VUE_APP_API_URL=http://localhost:5000
   ```

2. **Install Dependencies**: 
   Run the following command to install the necessary dependencies:
   ```
   npm install
   ```

3. **Start the Application**:
   Run the application using the following command:
   ```
   npm run serve
   ```

### Application Structure

- **src/**
  - **api.js**: Handles API requests.
  - **App.vue**: Root Vue component.
  - **assets/**: Static assets like images and styles.
  - **authStore.js**: Vuex store module for authentication.
  - **components/**: Contains Vue components.
    - **AboutUs.vue, ContactUs.vue, DashboardPage.vue, etc.**: Individual components for different parts of the app.
  - **dashboardApi.js**: API requests specific to the dashboard.
  - **main.js**: Entry point for the Vue application.
  - **router.js**: Vue Router configuration.
  - **store/**: Vuex store modules.
    - **auth.js**: Vuex store module for authentication.
  - **tests/**: Contains test files.
    - **unit/**: Unit tests for the frontend components.
      - **example.spec.js, SignupForm.spec.js**: Example test files.
  - **vue.config.js**: Configuration file for Vue CLI.

### Components

- **LoginForm.vue**: Component for user login.
- **SignupForm.vue**: Component for user registration.
- **DashboardPage.vue**: Component for displaying user-specific information after login.
- **NavBar.vue**: Navigation bar that dynamically updates based on user authentication status.

### Notes

- **Router Configuration**:
  - Uses navigation guards to protect routes that require authentication and to prevent authenticated users from accessing guest-only routes.

- **State Management**:
  - Uses Vuex to manage authentication state and user data.

## Running the Application

1. **Start the Backend**:
   ```
   cd backend
   flask run
   ```

2. **Start the Frontend**:
   ```
   cd frontend
   npm run serve
   ```

3. **Access the Application**:
   Open a browser and navigate to `http://localhost:8080` to access the frontend. The frontend will interact with the backend running at `http://localhost:5000`.

## License

This project is licensed under the MIT License.
