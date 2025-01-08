# Quiz Application

This is a simple quiz application built with Flask. The application allows users to register, log in, take quizzes, and view their results.

## Project Structure

app.py

db.sqlite3

README.md

requirements.txt

static/ 
    
    css/

       style.css 
    js/

       script.js 

templates/ 
   
    base.html 
    home.html 
    leaderboard.html 
    login.html 
    profile.html 
    quiz.html 
    register.html 
    results.html 
venv/ 

    bin/ 
    include/ 
    lib/ 
    lib64/ 
    pyvenv.cfg 
    share/

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/dagm24/Webstack---Portfolio-Project-.git
    cd Webstack---Portfolio-Project-
    ```

2. **Create a virtual environment:**

    ```sh
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application:**

    ```sh
    python app.py
    ```

6. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000
    ```

    ```

## Features

- **User Registration:** Users can create an account.
- **User Login:** Users can log in to their account.
- **Take Quiz:** Users can take quizzes.
- **View Results:** Users can view their quiz results.
- **Leaderboard:** Users can view the leaderboard.
- **Profile Management:** Users can update their profile information.

## File Descriptions

- **app.py:** The main application file.
- **db.sqlite3:** The SQLite database file.
- **requirements.txt:** The file containing the list of dependencies.
- **Procfile:** The file that tells Heroku how to run the application.
- **static/css/style.css:** The main stylesheet.
- **static/js/profile.js:** JavaScript file for profile page functionality.
- **templates/:** The directory containing HTML templates.


## Contributors

- [Dagmawit Tibebu](tibebudag07@gmail.com)