from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the SQLite database


def init_db():
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        # Create tables if they don't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY, 
            username TEXT, 
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            username TEXT UNIQUE, 
            password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY, 
            question_text TEXT, 
            option_a TEXT, 
            option_b TEXT, 
            option_c TEXT, 
            correct_option TEXT)''')

        # Insert some quiz questions if they don't exist
        cursor.execute('SELECT COUNT(*) FROM questions')
        if cursor.fetchone()[0] == 0:
            # Add sample quiz questions
            questions = [
                ('What is the capital of France?', 'Berlin', 'Paris', 'Rome', 'b'),
                ('Which of these is the largest planet?',
                 'Earth', 'Mars', 'Jupiter', 'c'),
                ('What is 2 + 2?', '3', '4', '5', 'b')
            ]
            cursor.executemany(
                'INSERT INTO questions (question_text, option_a, option_b, option_c, correct_option) VALUES (?, ?, ?, ?, ?)', questions)
            conn.commit()

        conn.commit()


@app.route('/api/questions', methods=['GET'])
def get_questions():
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, question_text, option_a, option_b, option_c FROM questions')
        questions = cursor.fetchall()

    # Format the data as JSON
    quiz_questions = [
        {
            'id': question[0],
            'question_text': question[1],
            'options': {
                'a': question[2],
                'b': question[3],
                'c': question[4]
            }
        }
        for question in questions
    ]

    return jsonify(quiz_questions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                conn.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already exists. Please choose another.', 'danger')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


@app.route('/')
def home():
    if 'username' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        flash('Please log in first to take the quiz.', 'warning')
        return redirect(url_for('login'))

    # Fetch the user's previous scores from the database
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT score, timestamp FROM results WHERE username = ? ORDER BY timestamp DESC', (session['username'],))
        previous_scores = cursor.fetchall()  # This will give a list of tuples

    if request.method == 'POST':
        # Fetch user answers
        answers = {
            'q1': request.form.get('q1'),
            'q2': request.form.get('q2'),
            'q3': request.form.get('q3'),
        }
        correct_answers = {'q1': 'b', 'q2': 'a', 'q3': 'c'}
        score = sum(1 for q, a in answers.items() if a == correct_answers[q])

        # Save results in the database
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO results (username, score) VALUES (?, ?)', (session['username'], score))
            conn.commit()

        # Include the current score and previous scores in the template
        return render_template('results.html', username=session['username'], score=score, previous_scores=previous_scores)

    return render_template('quiz.html', username=session['username'], previous_scores=previous_scores)


@app.route('/results')
def view_results():
    if 'username' not in session:
        flash('Please log in to view results.', 'warning')
        return redirect(url_for('login'))

    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, score FROM results')
        results = cursor.fetchall()

    return render_template('results.html', results=results)

# Add this new route to your Flask app
@app.route('/leaderboard')
def leaderboard():
    print("Leaderboard route accessed")  # Debugging line
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        # Fetch the latest score for each user
        cursor.execute('''
            SELECT username, score 
            FROM results 
            WHERE id IN (
                SELECT MAX(id) 
                FROM results 
                GROUP BY username
            )
            ORDER BY score DESC
            LIMIT 10
        ''')
        leaderboard_data = cursor.fetchall()

    # Add index to each entry in leaderboard_data
    leaderboard_with_index = [(index + 1, name, score) for index, (name, score) in enumerate(leaderboard_data)]

    return render_template('leaderboard.html', leaderboard=leaderboard_with_index)
@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    
    # Fetch the user's previous scores from the database
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT score, timestamp FROM results WHERE username = ? ORDER BY timestamp DESC', (username,))
        previous_scores = cursor.fetchall()  # This will give a list of tuples

    # Calculate total quizzes taken and achievements
    quizzes_taken = len(previous_scores)  # Example calculation
    achievements = 5  # This could be fetched from another table or calculated

    

    return render_template('profile.html', previous_scores=previous_scores, quizzes_taken=quizzes_taken, achievements=achievements)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        flash('Please log in to update your profile.', 'warning')
        return redirect(url_for('login'))

    new_username = request.form['username']
    new_password = request.form['password']
    hashed_password = generate_password_hash(new_password)

    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET username = ?, password = ? WHERE username = ?', (new_username, hashed_password, session['username']))
        cursor.execute('UPDATE results SET username = ? WHERE username = ?', (new_username, session['username']))
        conn.commit()

    session['username'] = new_username
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))
@app.route('/test')
def test():
    return "Test route is working!"
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
