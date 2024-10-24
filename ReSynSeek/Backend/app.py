from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# баба данных пользователей
def init_db():
    # Подключение и создание базы данных database.db
    conn = connect_db()
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
                        creation_account_date DATETIME,
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
                        detailed_description TEXT,
                        keywords INTEGER,
                        creation_project_date DATETIME,
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

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def connect_db():
    return sqlite3.connect('database.db')

# Рут для реги нового пользователя
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)',
                       (full_name, email, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already exists!'}), 409

# Рут для входа пользователя
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
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
    article_id = request.json.get('article_id')
    if not article_id:
        return jsonify({"error": "Article ID is required"}), 400

    article = next((a for a in articles if a['id'] == article_id), None)
    if article and article not in favorites:
        favorites.append(article)
        return jsonify({"message": "Article added to favorites"}), 200
    else:
        return jsonify({"error": "Article not found or already in favorites"}), 404

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
    app.run(debug=True)
