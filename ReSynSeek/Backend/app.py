from flask import Flask, request, jsonify, g, session
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
from functools import wraps
import jwt  

app = Flask(__name__)
app.secret_key = 'c05c4797799366e4c8bc970755345cbba58236ba83befa05c00a7f54d2dc8c12'
CORS(app)

# Configuration for sessions and database
app.config['JWT_SECRET_KEY'] = 'c05c4797799366e4c8bc970755345cbba58236ba83befa05c00a7f54d2dc8c12'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Function to generate UUID
def generate_uuid():
    return str(uuid.uuid4())

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create keywords table
    cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (
                        keyword_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL)''')

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        full_name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        creation_account_date DATETIME,
                        interests TEXT,
                        favorites_id TEXT,
                        own_projects_id TEXT,
                        FOREIGN KEY (interests) REFERENCES keywords(keyword_id),
                        FOREIGN KEY (favorites_id) REFERENCES projects(project_id),
                        FOREIGN KEY (own_projects_id) REFERENCES projects(project_id))''')

    # Create projects table
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        project_id TEXT PRIMARY KEY,
                        topic TEXT NOT NULL,
                        brief_description TEXT,
                        detailed_description TEXT,
                        keywords TEXT,
                        creation_project_date DATETIME,
                        image_url TEXT,
                        user_id_ownership TEXT,
                        email TEXT,
                        phone TEXT,
                        city_country TEXT,
                        facebook_link TEXT,
                        linkedin_link TEXT,
                        twitter_link TEXT,
                        instagram_link TEXT,
                        FOREIGN KEY (user_id_ownership) REFERENCES users(user_id),
                        FOREIGN KEY (keywords) REFERENCES keywords(keyword_id))''')

    # Create vacancies table
    cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id TEXT PRIMARY KEY,
                        project_id TEXT NOT NULL,
                        vacancy_name TEXT NOT NULL,
                        FOREIGN KEY (project_id) REFERENCES projects(project_id))''')

    # Create favorites table
    cursor.execute('''CREATE TABLE IF NOT EXISTS favorites (
                        favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        project_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (project_id) REFERENCES projects(project_id))''')

    # Create sessions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        created_at DATETIME,
                        expires_at DATETIME,
                        FOREIGN KEY (user_id) REFERENCES users(user_id))''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to connect to the database
def connect_db():
    return sqlite3.connect('database.db')

# Function to get a connection to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({"message": "Unauthorized access, please login!"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    interests = data.get('interests')

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if the user already exists
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return jsonify({'error': 'User already exists!'}), 409
        
        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database with the hashed password
        cursor.execute('INSERT INTO users (user_id, full_name, email, password, interests) VALUES (?, ?, ?, ?, ?)',
                       (generate_uuid(), full_name, email, hashed_password, interests))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Database error occurred!'}), 500

# API for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"message": "User not found!"}), 404

    stored_password = user[3]
    if not check_password_hash(stored_password, password):
        conn.close()
        return jsonify({"message": "Incorrect password!"}), 401

    # Create JWT token
    token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['JWT_SECRET_KEY'], algorithm='HS256')

    # Store session in the sessions table
    session_id = generate_uuid()
    created_at = datetime.datetime.utcnow()
    expires_at = created_at + datetime.timedelta(minutes=30)
    
    cursor.execute('INSERT INTO sessions (session_id, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)',
                   (session_id, user[0], created_at, expires_at))
    conn.commit()

    conn.close()
    return jsonify({"token": token, "session_id": session_id}), 200

# User logout, which clears the session
@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.json.get('session_id')  # Получаем session_id из запроса
    if not session_id:
        return jsonify({"message": "Session ID is required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Удаляем сессию из таблицы sessions
    cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()

    session.clear()  # Очищаем все данные сессии
    return jsonify({"message": "Logout successful!"}), 200

# Protect a route with login required
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing!"}), 401
    
    try:
        token = token.split(" ")[1]  # Split "Bearer token"
        decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']  # Get user ID from token
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401

    return jsonify({"message": "This is a protected route accessible only to logged-in users.", "user_id": user_id})

@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()

    # Get all users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    # Return list of users in JSON format
    return jsonify(users), 200

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')

    if not full_name or not email:
        return jsonify({"message": "Full name and email are required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Update user in the database
    cursor.execute('UPDATE users SET full_name = ?, email = ? WHERE user_id = ?',
                   (full_name, email, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "User updated successfully!"}), 200

# Add project route
@app.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    project_id = generate_uuid()
    topic = data.get('topic')
    brief_description = data.get('brief_description')
    detailed_description = data.get('detailed_description')
    keywords = data.get('keywords')
    user_id_ownership = data.get('user_id_ownership')

    if not topic or not user_id_ownership:
        return jsonify({"message": "Topic and user ownership ID are required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO projects (project_id, topic, brief_description, detailed_description, keywords, creation_project_date, user_id_ownership) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (project_id, topic, brief_description, detailed_description, keywords, datetime.datetime.utcnow(), user_id_ownership))
    conn.commit()
    conn.close()

    return jsonify({"message": "Project created successfully!", "project_id": project_id}), 201

# Delete project route
@app.route('/projects/<string:project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM projects WHERE project_id = ?', (project_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Project deleted successfully!"}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
