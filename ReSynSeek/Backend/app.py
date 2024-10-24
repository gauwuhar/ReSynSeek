from flask import Flask, request, jsonify, g, session
import sqlite3
from flask_cors import CORS
import database as db

app = Flask(__name__)
CORS(app)


# Закрытие подключения к базе данных
@app.teardown_appcontext
def close_connection(exception):
    db_users = getattr(g, '_database_users', None)
    if db_users is not None:
        db_users.close()
    db_projects = getattr(g, '_database_projects', None)
    if db_projects is not None:
        db_projects.close()


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

    conn = db.get_db_projects()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
    project = cursor.fetchone()

    if project:
        # Допустим, вы хотите добавлять проект в таблицу favorites
        conn = db.get_db_users()
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
    conn = db.get_db_projects()
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
    conn = db.get_db_projects()
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

@app.route('/add_scientific_interest', methods=['POST'])
def add_scientific_interest():
  data = request.json
  title = data.get('title')
  user_id = data.get('user_id')

  if not title or not user_id:
    return jsonify({"error": "Both title and user_id are required"}), 400

  try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert into the scientific_interests table
    cursor.execute('''INSERT INTO scientific_interests (title, user_id) VALUES (?, ?)''', (title, user_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Scientific interest added successfully!"}), 201
  except sqlite3.Error as e:
    return jsonify({"error": str(e)}), 500


# Эндпоинт для получения проекта по ID
@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    conn = db.get_db_projects()
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

    conn = db.get_db_projects()
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

    conn = db.get_db_projects()
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
    conn = db.get_db_projects()
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
    db.init_db()
    app.run(debug=False)
