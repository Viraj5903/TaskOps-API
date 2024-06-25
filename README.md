# TaskOps API

## Overview
TaskOps (Task Operations) API is a RESTful backend API built with Flask and MongoDB, using Python programming language. It is designed to streamline task management operations for various web and mobile applications. The API provides endpoints for user registration and authentication, as well as creating, retrieving, updating, and deleting tasks. The API ensures secure authentication and authorization using JWT tokens, serving as an efficient and easy task management solution.

## Description
TaskOps API offers a comprehensive solution for efficient and easy task management, focusing on user account management and secure operations. Utilizing Flask for its lightweight and flexible framework and MongoDB for its scalable NoSQL database capabilities, the API, developed with Python, ensures seamless user registration and authentication, as well as CRUD (Create, Read, Update, Delete) operations for tasks. Authentication and authorization are handled securely using JWT tokens, ensuring that only authorized users can access and manipulate task data.

The API adheres to RESTful principles, employing HTTP methods for predictable and intuitive endpoint design. It supports functionalities such as:
- User registration and authentication: Enables users to create accounts and securely authenticate using their credentials to access the task management features.
- Creating tasks: Allows authenticated users to create new personal or work-related tasks with specified descriptions and assignments.
- Retrieving tasks: Provides endpoints for authenticated users to fetch tasks they have created or tasks assigned to them.
- Updating tasks: Enables authenticated users to update task statuses (e.g., marking tasks as completed).
- Deleting tasks: Allows authenticated users to delete tasks they have created.

## Technology Used
TaskOps API utilizes the following technologies:
- Python: Backend programming language.
- Flask: Lightweight and extensible framework for building RESTful APIs.
- MongoDB: Scalable NoSQL database for storing task data efficiently.
- JWT (JSON Web Tokens): Secure method for transmitting authentication credentials between client and server.

## Setup Instructions
1. Clone the repository:
    ```
    git clone https://github.com/Viraj5903/TaskOps-API
    ```
2. Navigate to project root directory.
   ```
   cd TaskOps-API
   ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. MongoDB Setup
   - Create the project on [MongoDB Cloud](https://www.mongodb.com/products/platform/cloud).
   - Create a cluster within MongoDB Cloud.
5. Obtain MongoDB Connection String
   - Click on "Connect" in your MongoDB Cloud dashboard.
   - Select "Python" as the driver and copy the connection string provided.
6. Configure MongoDB Connection
   - Create or edit the `app_config.py` file in your project directory.
   - Add the MongoDB connection string as a constant:
        ```
        CONST_MONGO_URL = "<your_mongodb_connection_string>"
        ```

7. Run the Flask application:
   ```
   flask --app app run
   ```
   - Ensure you are in the project root directory where app.py (or your main Flask application file) resides.
  
#### NOTES:
- Replace <your_mongodb_connection_string> in CONST_MONGO_URL with the actual MongoDB connection string you obtained from MongoDB Cloud.
- Make sure MongoDB is running and accessible with the provided connection string.
- Adjust the flask run command if necessary based on your Flask application structure or additional configurations.

## API Endpoints Documentation
<b><i>Note: All request bodies must be in JSON format, and responses will be returned as JSON objects.</i></b>

### Users API Endpoints:
1. Create User Endpoint:
   - URL: `/users/`
   - Method: POST
   - Description: Creates a new user.
     - Requires email, password, and name in the request body.
     - Checks for required keys (email, password, name).
     - Ensures no duplicate email exists.
     - Hashes the password securely.
     - Saves the user details to MongoDB.
     - Returns the MongoDB-generated user ID upon success.
   
2. Login User Endpoint:
   - URL: `/users/login`
   - Method: POST
   - Description: Logs in a user.
     - Requires email and password in the request body.
     - Validates email existence.
     - Validates password correctness.
     - Generates a JWT token upon successful login.
     - Returns the JWT token with expiration, and basic user details.

### Tasks API Endpoints:
  <b><i>Note: For all Tasks API endpoints, a JWT authentication token is required in the header of the request. The JWT token can be obtained by logging in using the Login User Endpoint above. Make sure to include the JWT token in the header with the key "x-access-token" and the value as the obtained JWT Token.</i></b>

1. Create Task:
   - URL: `/tasks/`
   - Method: POST
   - Description: Creates a new task.
     - Requires authentication token, task description, and assignedToUid.
     - Validates token using validateJWT function.
     - Checks for required keys (description and assignedToUid) in request data.
     - Retrieves createdBy user from token.
     - Saves the task details to MongoDB.
     - Returns the MongoDB-generated task ID.

2. Get Tasks Created by the User
   - URL: `/tasks/createdby/`
   - Method: GET
   - Description: Retrieves tasks created by the authenticated user
     - Validates token using validateJWT function.
     - Returns a list of tasks created by the user.

3. Get Tasks Assigned to the User
   - URL: `/tasks/assignedto/`
   - Method: GET
   - Description: Retrieves tasks assigned to the authenticated user
     - Validates token using validateJWT function.
     - Returns a list of tasks assigned to the user.

4. Update Task
   - URL: `/tasks/<taskUid>`
   - Method: PATCH
   - Description: Updates the status (done attribute) of a task.
     - Requires authentication token.
     - Validates token using validateJWT function.
     - Checks for done status in request body.
     - Verifies if the authenticated user is authorized to update the task.
     - Updates the task status in MongoDB.
     - Returns the updated task ID upon success.

5. Delete Task
   - URL: `/tasks/<taskUid>`
   - Method: DELETE
   - Description: Deletes a task.
     - Requires authentication token.
     - Validates token using validateJWT function.
     - Verifies if the user created the task.
     - Deletes the task from MongoDB.
     - Returns the number of tasks affected.

## Author
- [Viraj Patel\(@Viraj5903\)](https://github.com/Viraj5903): 
  - Creator and maintainer of TaskOps API, responsible for designing and implementing the RESTful backend API for efficient task management.
  - Managed the MongoDB database for storing user and task data.
  - Developed the User API endpoints (Create User and Login User) to handle user registration and authentication.
  - Developed the Delete Task endpoint.
  - Managed the GitHub repository for effective version control, issue tracking, and collaboration among team members.

### Contributors
- [Manpreet Kaur\(@Kaur-Manpreet12\)](https://github.com/Kaur-Manpreet12): 
  - Developed the `Create Task` endpoint, responsible for adding new tasks to the system.
  
- [Dil Raval\(@DilRaval\)](https://github.com/DilRaval): 
  - Developed the `Get Tasks Created by the User` endpoint, enabling users to retrieve tasks they have created.

- [Aryan Handa\(@aryanhanda19\)](https://github.com/aryanhanda19):
  - Developed the `Get Tasks Assigned to the User` endpoint, allowing users to fetch tasks assigned to them.

- [Payal Rangra\(payalRangra04\)](https://github.com/payalRangra04):
  - Developed the `Update Task` endpoint, responsible for updating task statuses.