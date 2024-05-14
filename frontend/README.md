
# Vue.js Frontend Application

This is the frontend application built with Vue.js for the full-stack project. It provides a user interface for interacting with the backend features such as user authentication, registration, and session management.

## Setup

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

1. **Start the Frontend**:
   ```
   cd frontend
   npm run serve
   ```

2. **Access the Application**:
   Open a browser and navigate to `http://localhost:8080` to access the frontend. The frontend will interact with the backend running at `http://localhost:5000`.

## License

This project is licensed under the MIT License.
