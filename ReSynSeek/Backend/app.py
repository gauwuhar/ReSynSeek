from flask import Flask, request, jsonify, g, session
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Создаем таблицу keywords
    cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (
                        keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL)''')

    # Создаем таблицу users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        interests INTEGER,
                        favorites_id INTEGER,
                        own_projects_id INTEGER,
                        FOREIGN KEY (interests) REFERENCES keywords(keyword_id),
                        FOREIGN KEY (favorites_id) REFERENCES projects(project_id),
                        FOREIGN KEY (own_projects_id) REFERENCES projects(project_id))''')

    # Создаем таблицу projects
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT NOT NULL,
                        brief_description TEXT,
                        keywords INTEGER,
                        image_url TEXT,
                        user_id_ownership INTEGER,
                        email TEXT,
                        phone TEXT,
                        city_country TEXT,
                        facebook_link TEXT,
                        linkedin_link TEXT,
                        twitter_link TEXT,
                        instagram_link TEXT,
                        FOREIGN KEY (user_id_ownership) REFERENCES users(user_id),
                        FOREIGN KEY (keywords) REFERENCES keywords(keyword_id))''')

    # Создаем таблицу vacancies для хранения списка вакансий
    cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_id INTEGER NOT NULL,
                        vacancy_name TEXT NOT NULL,
                        FOREIGN KEY (project_id) REFERENCES projects(project_id))''')

    conn.commit()
    conn.close()

# Функция для получения подключения к базе данных
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

# Закрытие подключения к базе данных
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Регистрация нового пользователя
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    interests = data.get('interests')

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (full_name, email, password, interests) VALUES (?, ?, ?, ?)',
                        (full_name, email, password, interests))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already exists!'}), 409

# Вход пользователя
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'error': 'Invalid credentials!'}), 401

# Создание нового проекта
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    topic = data.get('topic')
    brief_description = data.get('brief_description')
    keywords = data.get('keywords')
    image_url = data.get('image_url')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (topic, brief_description, keywords, image_url) VALUES (?, ?, ?, ?)',
                   (topic, brief_description, keywords, image_url))
    conn.commit()
    return jsonify({'message': 'Project created successfully!'}), 201

# Эндпоинт для добавления проекта в избранное
@app.route('/add_fav', methods=['POST'])
def add_fav():
    project_id = request.json.get('project_id')
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
    project = cursor.fetchone()

    if project:
        user_id = session.get('user_id')
        cursor.execute('INSERT INTO favorites (user_id, project_id) VALUES (?, ?)', (user_id, project_id))
        conn.commit()
        return jsonify({"message": "Project added to favorites"}), 200
    else:
        return jsonify({"error": "Project not found"}), 404

# Запуск приложения
if __name__ == '__main__':
    init_db()
    app.run(debug=False)
