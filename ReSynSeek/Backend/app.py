from flask import Flask, request, jsonify, g, session
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Функции для подключения к базе данных
def get_db_users():
    db = getattr(g, '_database_users', None)
    if db is None:
        db = g._database_users = sqlite3.connect('users.db')
    return db

def get_db_projects():
    db = getattr(g, '_database_projects', None)
    if db is None:
        db = g._database_projects = sqlite3.connect('projects.db')
    return db

def get_db_favorites():
    db = getattr(g, '_database_favorites', None)
    if db is None:
        db = g._database_favorites = sqlite3.connect('favorites.db')
    return db


# Закрытие подключения к базе данных
@app.teardown_appcontext
def close_connection(exception):
    db_users = getattr(g, '_database_users', None)
    if db_users is not None:
        db_users.close()
    db_projects = getattr(g, '_database_projects', None)
    if db_projects is not None:
        db_projects.close()

# Инициализация базы данных пользователей и проектов
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

    # Инициализация базы данных проектов
    conn_projects = sqlite3.connect('projects.db')
    cursor_projects = conn_projects.cursor()
    cursor_projects.execute('''CREATE TABLE IF NOT EXISTS projects (
                            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            topic TEXT NOT NULL,
                            brief_description TEXT,
                            user_id_ownership INTEGER,
                            keywords TEXT,
                            vacancies TEXT,
                            image_url TEXT)''')
    conn_projects.commit()
    conn_projects.close()

    cursor_users.execute('''CREATE TABLE IF NOT EXISTS favorites (
                        favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        project_id INTEGER,
                        FOREIGN KEY(user_id) REFERENCES users(user_id),
                        FOREIGN KEY(project_id) REFERENCES projects(project_id))''')
    conn_projects.commit()
    conn_projects.close()


# Рут для реги нового пользователя
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    full_name = data.get('full_name')
    email_or_phone = data.get('email_or_phone')
    password = data.get('password')
    scientific_interest = data.get('scientific_interest')
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (full_name, email_or_phone, password, interests) VALUES (?, ?, ?, ?)',
                        (full_name, email_or_phone, password, scientific_interest))
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


#Рут для добавления статьи в избранное
@app.route('/add_fav', methods=['POST'])
def add_fav():
    project_id = request.json.get('project_id')
    if not project_id:
        return jsonify({"error": "project ID is required"}), 400

    conn = get_db_projects()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
    project = cursor.fetchone()

    if project:
        # Допустим, вы хотите добавлять проект в таблицу favorites
        conn = get_db_users()
        cursor = conn.cursor()
        user_id = session.get('user_id')  # или используйте JWT токен
        cursor.execute('INSERT INTO favorites (user_id, project_id) VALUES (?, ?)', (user_id, project_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Project added to favorites"}), 200
    else:
        return jsonify({"error": "Project not found"}), 404



# Эндпоинт для поиска статей
@app.route('/search_project', methods=['GET'])
def search_project():
    query = request.args.get('query', '')
    conn = get_db_projects()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM projects WHERE topic LIKE ? OR keywords LIKE ?''', (f'%{query}%', f'%{query}%'))
    projects = cursor.fetchall()

    if projects:
        result = [{
            'project_id': project[0],
            'topic': project[1],
            'brief_description': project[2],
            'user_id_ownership': project[3],
            'keywords': project[4].split(','),
            'vacancies': project[5],
            'image_url': project[6]
        } for project in projects]

        return jsonify(result), 200
    else:
        return jsonify({"message": "No projects found"}), 404

    

# Эндпоинт для получения списка всех проектов
@app.route('/projects', methods=['GET'])
def get_projects():
    conn = get_db_projects()
    cursor = conn.cursor()
    
    search_query = request.args.get('search', '')
    
    if search_query:
        cursor.execute('''SELECT * FROM projects 
                          WHERE topic LIKE ? OR keywords LIKE ?''', 
                       (f'%{search_query}%', f'%{search_query}%'))
    else:
        cursor.execute('SELECT * FROM projects')
    
    projects = cursor.fetchall()
    
    project_list = [{
        'project_id': project[0],
        'topic': project[1],
        'brief_description': project[2],
        'user_id_ownership': project[3],
        'keywords': project[4].split(','),
        'vacancies': project[5],
        'image_url': project[6]
    } for project in projects]
    
    return jsonify(project_list), 200

# Эндпоинт для получения проекта по ID
@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    conn = get_db_projects()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
    project = cursor.fetchone()
    
    if project is None:
        return jsonify({"error": "Project not found"}), 404
    
    project_data = {
        'project_id': project[0],
        'topic': project[1],
        'brief_description': project[2],
        'user_id_ownership': project[3],
        'keywords': project[4].split(','),
        'vacancies': project[5],
        'image_url': project[6]
    }
    
    return jsonify(project_data), 200

# Эндпоинт для добавления нового проекта
@app.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    
    conn = get_db_projects()
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO projects (topic, brief_description, user_id_ownership, keywords, vacancies, image_url)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (data['topic'], data.get('brief_description', ''), 
                    data['user_id_ownership'], ','.join(data['keywords']),
                    data.get('vacancies', ''), data.get('image_url', '')))
    
    conn.commit()
    
    return jsonify({"message": "Project created successfully"}), 201

# Эндпоинт для обновления проекта
@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.get_json()
    
    conn = get_db_projects()
    cursor = conn.cursor()
    
    cursor.execute('''UPDATE projects 
                      SET topic = ?, brief_description = ?, user_id_ownership = ?, keywords = ?, vacancies = ?, image_url = ?
                      WHERE project_id = ?''', 
                   (data.get('topic'), data.get('brief_description', ''), 
                    data.get('user_id_ownership'), ','.join(data.get('keywords', [])),
                    data.get('vacancies', ''), data.get('image_url', ''), project_id))
    
    conn.commit()
    
    return jsonify({"message": "Project updated successfully"}), 200

# Эндпоинт для удаления проекта
@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn = get_db_projects()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM projects WHERE project_id = ?', (project_id,))
    conn.commit()
    
    return jsonify({"message": "Project deleted successfully"}), 200


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
