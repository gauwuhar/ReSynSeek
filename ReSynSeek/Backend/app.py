# from flask import Flask, request, jsonify, g, session, render_template
# import sqlite3
# import uuid
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_cors import CORS
# from flask_session import Session
# import datetime
# from functools import wraps
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# CORS(app)
# app.secret_key = 'your_secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Flask-Session configuration
# app.config['SESSION_TYPE'] = 'filesystem'  # For local development
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True  # Ensures cookies are cryptographically signed
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
# Session(app)  # Initialize session management with Flask-Session
# db = SQLAlchemy(app)

# # Функция для генерации UUID
# def generate_uuid():
#     return str(uuid.uuid4())

# # Инициализация базы данных
# def init_db():
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # Создаем таблицу keywords
#     cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (
#                         keyword_id TEXT PRIMARY KEY,
#                         title TEXT NOT NULL)''')

#     # Создаем таблицу users
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                         user_id TEXT PRIMARY KEY,
#                         full_name TEXT NOT NULL,
#                         email TEXT UNIQUE NOT NULL,
#                         password TEXT NOT NULL,
#                         creation_account_date DATETIME,
#                         interests TEXT,
#                         favorites_id TEXT,
#                         own_projects_id TEXT,
#                         FOREIGN KEY (interests) REFERENCES keywords(keyword_id),
#                         FOREIGN KEY (favorites_id) REFERENCES projects(project_id),
#                         FOREIGN KEY (own_projects_id) REFERENCES projects(project_id))''')

#     # Создаем таблицу projects
#     cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
#                         project_id TEXT PRIMARY KEY,
#                         topic TEXT NOT NULL,
#                         brief_description TEXT,
#                         detailed_description TEXT,
#                         keywords TEXT,
#                         creation_project_date DATETIME,
#                         image_url TEXT,
#                         user_id_ownership TEXT,
#                         email TEXT,
#                         phone TEXT,
#                         city_country TEXT,
#                         facebook_link TEXT,
#                         linkedin_link TEXT,
#                         twitter_link TEXT,
#                         instagram_link TEXT,
#                         FOREIGN KEY (user_id_ownership) REFERENCES users(user_id),
#                         FOREIGN KEY (keywords) REFERENCES keywords(keyword_id))''')

#     # Создаем таблицу vacancies для хранения списка вакансий
#     cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies (
#                         vacancy_id TEXT PRIMARY KEY,
#                         project_id TEXT NOT NULL,
#                         vacancy_name TEXT NOT NULL,
#                         FOREIGN KEY (project_id) REFERENCES projects(project_id))''')
    
#     cursor.execute('''CREATE TABLE IF NOT EXISTS favorites (
#                     favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER,
#                     project_id INTEGER,
#                     FOREIGN KEY (user_id) REFERENCES users(user_id),
#                     FOREIGN KEY (project_id) REFERENCES projects(project_id))''')


#     # Сохраняем изменения и закрываем соединение
#     conn.commit()
#     conn.close()

# # Функция для подключения к базе данных
# def connect_db():
#     return sqlite3.connect('database.db')

# # Функция для получения подключения к базе данных
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect('database.db')
#     return db

# # Decorator to protect routes
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get('logged_in'):
#             return jsonify({"message": "Unauthorized access, please login!"}), 401
#         return f(*args, **kwargs)
#     return decorated_function

# # Закрытие подключения к базе данных
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     full_name = data.get('full_name')
#     email = data.get('email')
#     password = data.get('password')
#     interests = data.get('interests')

#     try:
#         conn = get_db()
#         cursor = conn.cursor()

#         # Проверяем, существует ли уже пользователь с таким email
#         cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
#         existing_user = cursor.fetchone()

#         if existing_user:
#             conn.close()
#             return jsonify({'error': 'User already exists!'}), 409
        
#         # Хэшируем пароль перед сохранением
#         hashed_password = generate_password_hash(password)

#         #Вставляем нового пользователя в базу данных с зашифрованным паролем
#         cursor.execute('INSERT INTO users (full_name, email, password, interests) VALUES (?, ?, ?, ?)',
#                         (full_name, email, hashed_password, interests))
#         conn.commit()
#         return jsonify({'message': 'User registered successfully!'}), 201
#     except sqlite3.IntegrityError:
#         return jsonify({'error': 'Database error occurred!'}), 500


# # API for user login
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')


#     if not email or not password:
#         return jsonify({"message": "Email and password are required!"}), 400

#     conn = connect_db()

#     cursor = conn.cursor()

#     # Проверяем, существует ли пользователь с таким email
#     cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
#     user = cursor.fetchone()
#     if not user:
#         conn.close()
#         return jsonify({"message": "User not found!"}), 404

#     # Проверяем хэшированный пароль
#     stored_password = user[3]  
#     if not check_password_hash(stored_password, password):
#         conn.close()
#         return jsonify({"message": "Incorrect password!"}), 401
    
#     # Set session data
#     session['user_id'] = user[0]  # Store user_id in session
#     session['logged_in'] = True
#     session.permanent = True  # Make session permanent (expires as per config)

#     conn.close()
#     return jsonify({"message": "Login successful!"}), 200

# # User logout, which clears the session
# @app.route('/logout', methods=['POST'])
# def logout():
#     session.clear()  # Clear all session data
#     return jsonify({"message": "Logout successful!"}), 200

# # Protect a route with login required
# @app.route('/protected', methods=['GET'])
# def protected():
#     if not session.get('logged_in'):
#         return jsonify({"message": "Unauthorized access, please login!"}), 401
#     return jsonify({"message": "This is a protected route accessible only to logged-in users."})


# @app.route('/users', methods=['GET'])
# def get_users():
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Получаем всех пользователей
#     cursor.execute('SELECT * FROM users')
#     users = cursor.fetchall()
#     conn.close()

#     # Возвращаем список пользователей в формате JSON
#     return jsonify(users), 200

# @app.route('/users/<string:user_id>', methods=['PUT'])
# def update_user(user_id):
#     data = request.get_json()
#     full_name = data.get('full_name')
#     email = data.get('email')

#     if not full_name or not email:
#         return jsonify({"message": "All fields are required!"}), 400

#     conn = connect_db()
#     cursor = conn.cursor()

#     # Обновляем информацию о пользователе по UUID
#     cursor.execute('UPDATE users SET full_name = ?, email = ? WHERE user_id = ?',
#                    (full_name, email, user_id))
#     conn.commit()
#     conn.close()

#     return jsonify({"message": "User updated successfully!"}), 200

# @app.route('/users/<string:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Удаляем пользователя по ID
#     cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
#     conn.commit()
#     conn.close()

#     return jsonify({"message": "User deleted successfully!"}), 200



# # Создание нового проекта
# @app.route('/create_project', methods=['POST'])
# def create_project():
#     data = request.json
#     topic = data.get('topic')
#     brief_description = data.get('brief_description')
#     keywords = data.get('keywords')
#     image_url = data.get('image_url')

#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO projects (topic, brief_description, keywords, image_url) VALUES (?, ?, ?, ?)',
#                    (topic, brief_description, keywords, image_url))
#     conn.commit()
#     return jsonify({'message': 'Project created successfully!'}), 201

# # Эндпоинт для добавления проекта в избранное
# @app.route('/add_fav', methods=['POST'])
# def add_fav():
#     project_id = request.json.get('project_id')
#     if not project_id:
#         return jsonify({"error": "Project ID is required"}), 400


#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
#     project = cursor.fetchone()

#     if project:

#         user_id = session.get('user_id')  # Получаем user_id из сессии
#         if not user_id:
#             return jsonify({"error": "User is not logged in"}), 401

#         cursor.execute('INSERT INTO favorites (user_id, project_id) VALUES (?, ?)', (user_id, project_id))
#         conn.commit()
#         return jsonify({"message": "Project added to favorites"}), 200
#     else:
#         return jsonify({"error": "Project not found"}), 404


# @app.route('/api/data', methods=['GET'])
# def get_data():
#     return jsonify({'message': 'Hello from the backend!'})


# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Welcome to the Flask API!'})


# #Рут для просмотра профиля статьи
# @app.route('/project_profile/<int:project_id>', methods=['GET'])
# def get_project_profile(project_id):
#     # Подключаемся к базе данных
#     conn = connect_db()
#     cursor = conn.cursor()

#     # Выполняем запрос для получения проекта по его ID
#     cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
#     project = cursor.fetchone()

#     # Если проект не найден
#     if project is None:
#         conn.close()
#         return jsonify({'message': 'ERROR: Project not found'}), 404

#     # Получаем информацию о владельце проекта из таблицы users
#     cursor.execute('SELECT full_name, email FROM users WHERE user_id = ?', (project[7],))
#     owner = cursor.fetchone()

#     conn.close()

#     # Если владелец проекта найден, добавляем его данные в проект
#     owner_data = {
#         'name': owner[0],
#         'email': owner[1]
#     } if owner else {'name': 'Unknown', 'email': 'Unknown'}

#     # Формируем данные проекта с добавлением информации о владельце
#     project_data = {
#         'id': project[0],
#         'topic': project[1],
#         'brief_description': project[2],
#         'detailed_description': project[3],
#         'keywords': project[4],
#         'creation_project_date': project[5],
#         'image_url': project[6],
#         'owner': owner_data,
#         'city_country': project[10],
#         'facebook_link': project[11],
#         'linkedin_link': project[12],
#         'twitter_link': project[13],
#         'instagram_link': project[14]
#     }

#     return jsonify(project_data), 200

# # Функция для заполнения базы данных тестовыми данными
# def fill_db():
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # Добавляем тестовые ключевые слова (все ID и значения представлены строками)
#     keywords = [
#         ('kw1', 'Technology'),
#         ('kw2', 'Education'),
#         ('kw3', 'Health'),
#     ]
#     cursor.executemany('INSERT OR IGNORE INTO keywords (keyword_id, title) VALUES (?, ?)', keywords)

#     # Добавляем тестовых пользователей
#     users = [
#         ('user1', 'Alice Johnson', 'alice@example.com', 'password123', '2022-01-15T10:00:00', 'kw1', None, None),
#         ('user2', 'Bob Smith', 'bob@example.com', 'password123', '2023-06-25T14:30:00', 'kw2', None, None),
#         ('user3', 'Charlie Brown', 'charlie@example.com', 'password123', '2021-11-03T08:45:00', 'kw3', None, None),
#     ]

#     cursor.executemany('''INSERT OR IGNORE INTO users (user_id, full_name, email, password, 
#                         creation_account_date, interests, favorites_id, own_projects_id) 
#                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', users)

#     # Добавляем проекты, назначая каждому проекту владельца из таблицы пользователей
#     projects = [
#         (1, 'Project Alpha', 'Brief description 1', 'Detailed description 1', 'kw1', '2022-01-15T10:00:00', 
#          'image1.jpg', 'user1', 'project1@example.com', '123-456-7890', 'City1, Country1', 
#          'facebook.com/proj1', 'linkedin.com/proj1', 'twitter.com/proj1', 'instagram.com/proj1'),
#         (2, 'Project Beta', 'Brief description 2', 'Detailed description 2', 'kw2', '2023-06-25T14:30:00', 
#          'image2.jpg', 'user2', 'project2@example.com', '098-765-4321', 'City2, Country2', 
#          'facebook.com/proj2', 'linkedin.com/proj2', 'twitter.com/proj2', 'instagram.com/proj2'),
#         (3, 'Project Gamma', 'Brief description 3', 'Detailed description 3', 'kw3', '2021-11-03T08:45:00', 
#          'image3.jpg', 'user3', 'project3@example.com', '567-890-1234', 'City3, Country3', 
#          'facebook.com/proj3', 'linkedin.com/proj3', 'twitter.com/proj3', 'instagram.com/proj3'),
#     ]
#     cursor.executemany('''INSERT OR IGNORE INTO projects (project_id, topic, brief_description, detailed_description, 
#                         keywords, creation_project_date, image_url, user_id_ownership, email, phone, city_country, 
#                         facebook_link, linkedin_link, twitter_link, instagram_link) 
#                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', projects)

#     conn.commit()
#     conn.close()



# # Запуск всея всего
# if __name__ == '__main__':

#     init_db()
#     fill_db()
#     app.run(debug=False)









from flask import Flask, request, jsonify, g, session, render_template
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_session import Session
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Модели базы данных
class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keywords = db.relationship('Keyword', backref='project', lazy=True)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

# Инициализация базы данных
def init_db():
    db.create_all()

# Вызов инициализации базы данных сразу после создания приложения
with app.app_context():
    init_db()

# Роуты приложения
@app.route('/register', methods=['POST'], endpoint='register')
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'], endpoint='login')
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return make_response('Invalid credentials', 401)

    token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

# Проверка токена
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/projects', methods=['POST'], endpoint='projects')
@token_required
def create_project(current_user):
    data = request.get_json()
    new_project = Project(name=data['name'], user_id=current_user.id)

    db.session.add(new_project)
    db.session.commit()

    for keyword_text in data['keywords']:
        keyword = Keyword(keyword=keyword_text, project_id=new_project.id)
        db.session.add(keyword)

    db.session.commit()
    return jsonify({'message': 'Project created successfully'})

@app.route('/favorites', methods=['POST'], endpoint='favorites')
@token_required
def add_favorite(current_user):
    data = request.get_json()
    project = Project.query.filter_by(id=data['project_id'], user_id=current_user.id).first()

    if not project:
        return jsonify({'message': 'Project not found'}), 404

    new_favorite = Favorite(user_id=current_user.id, project_id=project.id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'Project added to favorites'})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from the backend!'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})

@app.route('/project_profile/<int:project_id>', methods=['GET'])
def get_project_profile(project_id):
    # Получаем проект по его ID
    project = Project.query.get(project_id)

    # Если проект не найден
    if project is None:
        return jsonify({'message': 'ERROR: Project not found'}), 404

    # Получаем информацию о владельце проекта
    owner = User.query.get(project.user_id)

    # Если владелец проекта найден, добавляем его данные в проект
    owner_data = {
        'name': owner.username if owner else 'Unknown',  # Assuming 'username' is the field you want
        'email': owner.email if owner else 'unknown@example.com'  # Assuming 'email' is the field you want
    }

    # Формируем данные проекта с добавлением информации о владельце
    project_data = {
        'id': project.id,
        'topic': project.name,  # Предполагаем, что 'topic' соответствует полю 'name' проекта
        'brief_description': '',  # Добавьте соответствующее поле, если оно существует в модели
        'detailed_description': '',  # Добавьте соответствующее поле, если оно существует в модели
        'keywords': [keyword.keyword for keyword in project.keywords],
        'creation_project_date': '',  # Добавьте соответствующее поле, если оно существует в модели
        'image_url': '',  # Добавьте соответствующее поле, если оно существует в модели
        'owner': owner_data,
        'city_country': '',  # Добавьте соответствующее поле, если оно существует в модели
        'facebook_link': '',  # Добавьте соответствующее поле, если оно существует в модели
        'linkedin_link': '',  # Добавьте соответствующее поле, если оно существует в модели
        'twitter_link': '',  # Добавьте соответствующее поле, если оно существует в модели
        'instagram_link': ''  # Добавьте соответствующее поле, если оно существует в модели
    }

    return jsonify(project_data), 200


# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)