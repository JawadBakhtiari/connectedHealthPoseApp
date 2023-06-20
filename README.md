# connectedhealth
Backend application for Connected Health VIP UNSW
# BlazePose Analysis App

This is a web-based application that aids physicians in analysing their patients' health remotely. It is built using Django for backend operations and uses Azure Blob Storage for persistent data storage. The application analyzes BlazePose keypoints sent by the frontend, which are then stored and can be visualized by the physicians.

## Components of the Application

### DataStore Class

This class is a wrapper around Azure Blob Storage operations. It provides methods to get and set session data, populate session data from local storage or Azure Blob Storage, write session data to local storage or Azure Blob Storage, and get the name of the session blob in Azure Blob Storage.

### Django Models

The application uses three Django models: `User`, `Session`, and `InvolvedIn`.

- `User` and `Session` models represent users and sessions respectively.
- The `InvolvedIn` model represents a many-to-many relationship between users and sessions, indicating which users participated in which sessions.

### Django Views

The application has two main view functions: `frames_upload` and `visualise_coordinates`.

- `frames_upload` receives POST requests from the frontend with user session data. This data includes BlazePose keypoints, which are then stored persistently in Azure Blob Storage.
- `visualise_coordinates` retrieves a user's session data from Azure Blob Storage. It generates an animation of the session data by creating a sequence of images with keypoints and connections drawn on them. This visualization can be used by physicians to analyze the patients' health status remotely.

## How to Use

1. Clone the repository:
    ```
    git clone https://github.com/nick-maiden/connectedhealth/tree/main/connectedhealth
    ```
2. Navigate to the project directory:
    ```
    cd connectedhealth
    ```
3. Install Django and other necessary libraries:
    ```
    pip install django
    pip install azure-storage-blob
    pip install orjson
    pip install opencv-python
    pip install plotly
    ```
4. Initialize the database:
    ```
    python3 manage.py migrate
    python3 manage.py makemigrations
    ```
5. Run the server:
    ```
    python3 manage.py runserver
    ```
6. Visit `localhost:8000` on your web browser to start using the application.

## Future Work

The current implementation has some error handling and edge cases that are not yet handled. For example, what should happen when a user or session doesn't exist, or when a user was not part of a session they're trying to access. Improvements could be made by adding appropriate error handling for these situations.

## Dependencies

- Django
- Azure Blob Storage
- OpenCV
- Numpy
- Plotly
- Orjson
