from flask import Flask, request, jsonify, g, session
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key_here'

# Функция для генерации UUID
def generate_uuid():
    return str(uuid.uuid4())

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Создаем таблицу keywords
    cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (
                        keyword_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL)''')

    # Создаем таблицу users
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

    # Создаем таблицу projects
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

    # Создаем таблицу vacancies для хранения списка вакансий
    cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id TEXT PRIMARY KEY,
                        project_id TEXT NOT NULL,
                        vacancy_name TEXT NOT NULL,
                        FOREIGN KEY (project_id) REFERENCES projects(project_id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS favorites (
                    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    project_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (project_id) REFERENCES projects(project_id))''')


    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

# Функция для подключения к базе данных
def connect_db():
    return sqlite3.connect('database.db')

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

def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')


    try:
        conn = get_db()
        cursor = conn.cursor()

        # Проверяем, существует ли уже пользователь с таким email
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'User already exists!'}), 409

        # Если пользователя нет, создаем нового
        cursor.execute('INSERT INTO users (full_name, email, password, interests) VALUES (?, ?, ?, ?)',
                        (full_name, email, password, interests))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Database error occurred!'}), 500


    conn = connect_db()
    cursor = conn.cursor()

    # Проверяем, есть ли уже пользователь с таким email
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return jsonify({"message": "Email already registered!"}), 400

    # Хэшируем пароль перед сохранением
    hashed_password = generate_password_hash(password)

    # Вставляем нового пользователя в базу данных с зашифрованным паролем
    cursor.execute('INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)',
                   (full_name, email, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

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

    # Проверяем, существует ли пользователь с таким email
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"message": "User not found!"}), 404

    # Проверяем хэшированный пароль
    stored_password = user[3]  
    if not check_password_hash(stored_password, password):
        conn.close()
        return jsonify({"message": "Incorrect password!"}), 401

    conn.close()
    return jsonify({"message": "Login successful!"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()

    # Получаем всех пользователей
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    # Возвращаем список пользователей в формате JSON
    return jsonify(users), 200

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')

    if not full_name or not email:
        return jsonify({"message": "All fields are required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Обновляем информацию о пользователе по UUID
    cursor.execute('UPDATE users SET full_name = ?, email = ? WHERE user_id = ?',
                   (full_name, email, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "User updated successfully!"}), 200

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Удаляем пользователя по ID
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted successfully!"}), 200



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
        user_id = session.get('user_id')  # Получаем user_id из сессии
        if not user_id:
            return jsonify({"error": "User is not logged in"}), 401
        cursor.execute('INSERT INTO favorites (user_id, project_id) VALUES (?, ?)', (user_id, project_id))
        conn.commit()
        return jsonify({"message": "Project added to favorites"}), 200
    else:
        return jsonify({"error": "Project not found"}), 404


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from the backend!'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})


#Рут для просмотра профиля статьи
@app.route('/project_profile/<int:project_id>', methods=['GET'])
def get_project_profile(project_id):
    # Если проект не найден, выводим сообщение
    conn = connect_db()
    cursor = conn.cursor()

    # Выполняем запрос для получения проекта по его ID
    cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
    project = cursor.fetchone()

    conn.close()

    # Если проект не найден
    if project is None:
        return jsonify({'message': 'ERROR: Project not found'}), 404

    # Формируем данные проекта в виде словаря
    project_data = {
    'id': project[0],
    'topic': project[1],
    'brief_description': project[2],
    'detailed_description': project[3],
    'keywords': project[4],
    'creation_project_date': project[5],
    'image_url': project[6],
    'user_id_ownership': project[7],
    'email': project[8],
    'phone': project[9],
    'city_country': project[10],
    'facebook_link': project[11],
    'linkedin_link': project[12],
    'twitter_link': project[13],
    'instagram_link': project[14]
}

    return jsonify(project_data), 200


def fill_db():
    # Подключаемся к базе данных
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM projects')
    cursor.execute('DELETE FROM vacancies')
    cursor.execute('DELETE FROM keywords')

    # Вставляем данные в таблицу keywords
    keywords_data = [
        ('Technology',),
        ('Science',),
        ('AI',),
        ('Cybersecurity',)
    ]
    cursor.executemany('INSERT INTO keywords (title) VALUES (?)', keywords_data)

    # Вставляем данные в таблицу users
    users_data = [
        ('John Doe', 'john.doe@example.com', 'password123', '2023-01-15 10:00:00', 1, 1, 1),
        ('Jane Smith', 'jane.smith@example.com', 'password456', '2023-02-20 14:30:00', 2, 2, 2),
        ('Alice Brown', 'alice.brown@example.com', 'password789', '2023-03-05 09:15:00', 3, 1, 2)
    ]
    cursor.executemany('INSERT INTO users (full_name, email, password, creation_account_date, interests, favorites_id, own_projects_id) VALUES (?, ?, ?, ?, ?, ?, ?)', users_data)

    # Вставляем данные в таблицу projects
    projects_data = [
    (1, 'AI for Good', 'A project focused on using AI for social good.', 'Detailed description for AI for Good', 3, '2023-04-01 11:45:00', 'https://example.com/image1.jpg', 1, 'ai@example.com', '123-456-7890', 'New York, USA', 'https://facebook.com/ai', 'https://linkedin.com/ai', 'https://twitter.com/ai', 'https://instagram.com/ai'),
    (2, 'Cybersecurity Innovations', 'New techniques to secure digital systems.', 'Detailed description for Cybersecurity Innovations', 4, '2023-05-10 16:00:00', 'https://example.com/image2.jpg', 2, 'security@example.com', '098-765-4321', 'London, UK', 'https://facebook.com/security', 'https://linkedin.com/security', 'https://twitter.com/security', 'https://instagram.com/security')
    ]
    cursor.executemany('INSERT INTO projects (project_id, topic, brief_description, detailed_description, keywords, creation_project_date, image_url, user_id_ownership, email, phone, city_country, facebook_link, linkedin_link, twitter_link, instagram_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', projects_data)

    # Вставляем данные в таблицу vacancies
    vacancies_data = [
        (1, 'AI Engineer'),
        (1, 'Data Scientist'),
        (2, 'Cybersecurity Analyst'),
        (2, 'Penetration Tester')
    ]
    cursor.executemany('INSERT INTO vacancies (project_id, vacancy_name) VALUES (?, ?)', vacancies_data)

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


# Запуск всея всего
if __name__ == '__main__':
    init_db()
    fill_db()
    app.run(debug=False)
