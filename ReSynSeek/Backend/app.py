from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# баба данных пользователей
def init_db():
    conn_users = sqlite3.connect('users.db')
    cursor_users = conn_users.cursor()
    cursor_users.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            full_name TEXT NOT NULL,
                            email_or_phone TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            interests INTEGER,
                            favorites_id INTEGER,
                            own_projects_id INTEGER)''')
    conn_users.commit()
    conn_users.close()

    # баба данных проект
    conn_projects = sqlite3.connect('projects.db')
    cursor_projects = conn_projects.cursor()
    cursor_projects.execute('''CREATE TABLE IF NOT EXISTS projects (
                            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            topic TEXT NOT NULL,
                            brief_description TEXT,
                            user_id_ownership INTEGER,
                            keywords TEXT,
                            vacancies TEXT,
                            image_url)''')
    conn_projects.commit()
    conn_projects.close()

# Рут для реги нового пользователя
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    full_name = data.get('full_name')
    email_or_phone = data.get('email_or_phone')
    password = data.get('password')
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (full_name, email_or_phone, password) VALUES (?, ?, ?)',
                       (full_name, email_or_phone, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already exists!'}), 409

# Рут для входа пользователя
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email_or_phone = data.get('email_or_phone')
    password = data.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email_or_phone = ? AND password = ?', (email_or_phone, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'error': 'Invalid credentials!'}), 401

# Рут для создания новой статьи
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    topic = data.get('topic')
    brief_description = data.get('brief_description')
    authors = data.get('authors')
    keywords = data.get('keywords')
    vacancies = data.get('vacancies')

    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (topic, brief_description, authors, keywords, vacancies) VALUES (?, ?, ?, ?, ?)',
                   (topic, brief_description, authors, keywords, vacancies))
    conn.commit()
    conn.close()

    return jsonify({'message': 'project created successfully!'}), 201


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from the backend!'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})

@app.route('/project_profile', methods=['GET'])
def project_profile():
    return jsonify({'message': 'Welcome to the Flask API!'})

# Запуск всея всего
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
