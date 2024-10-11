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
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            full_name TEXT NOT NULL,
                            email_or_phone TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')
    conn_users.commit()
    conn_users.close()

    # баба данных статей
    conn_articles = sqlite3.connect('articles.db')
    cursor_articles = conn_articles.cursor()
    cursor_articles.execute('''CREATE TABLE IF NOT EXISTS articles (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            topic TEXT NOT NULL,
                            brief_description TEXT,
                            authors TEXT,
                            keywords TEXT,
                            vacancies TEXT)''')
    conn_articles.commit()
    conn_articles.close()

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
@app.route('/create_article', methods=['POST'])
def create_article():
    data = request.json
    topic = data.get('topic')
    brief_description = data.get('brief_description')
    authors = data.get('authors')
    keywords = data.get('keywords')
    vacancies = data.get('vacancies')

    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (topic, brief_description, authors, keywords, vacancies) VALUES (?, ?, ?, ?, ?)',
                   (topic, brief_description, authors, keywords, vacancies))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Article created successfully!'}), 201


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from the backend!'})

# Запуск всея всего
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
