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
from flask_sqlalchemy import SQLAlchemy
import datetime
from functools import wraps
<<<<<<< Updated upstream
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
=======
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
>>>>>>> Stashed changes

# Initialize database
def init_db():
    db.create_all()

<<<<<<< Updated upstream
# Вызов инициализации базы данных сразу после создания приложения
with app.app_context():
    init_db()

# Роуты приложения
@app.route('/register', methods=['POST'], endpoint='register')
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
=======
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
                        creation_account_date DATETIME DEFAULT CURRENT_TIMESTAMP,
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
                        creation_project_date DATETIME DEFAULT CURRENT_TIMESTAMP,
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
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        expires_at DATETIME DEFAULT CURRENT_TIMESTAMP,
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
    full_name = data.get('fullName')  # Changed to match the incoming key
    email = data.get('email')
    password = data.get('password')
    # interests = data.get('interests', None)  # Optional field
>>>>>>> Stashed changes

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

<<<<<<< Updated upstream
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'], endpoint='login')
=======
        # Check if the user already exists
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return jsonify({'error': 'User already exists!'}), 409
        
        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database with the hashed password
        cursor.execute(
            '''INSERT INTO users (user_id, full_name, email, password) 
            VALUES (?, ?, ?, ?)''',
            (generate_uuid(), full_name, email, hashed_password)
        )

        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 200
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")  # Log error for debugging
        return jsonify({'error': 'Database error occurred!'}), 500
    except Exception as e:
        print(f"An error occurred: {e}")  # Log any other exceptions
        return jsonify({'error': 'An error occurred!'}), 500




# API for user login
@app.route('/login', methods=['POST'])
>>>>>>> Stashed changes
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

<<<<<<< Updated upstream
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
=======
    # Проверка наличия email и пароля
    if not email or not password:
        return jsonify({"message": "Email and password are required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Поиск пользователя по email
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"message": "User not found!"}), 404

    stored_password = user[3]
    # Проверка пароля
    if not check_password_hash(stored_password, password):
        conn.close()
        return jsonify({"message": "Incorrect password!"}), 401

    # Генерация идентификатора сессии
    session_id = generate_uuid()
    created_at = datetime.datetime.utcnow()
    expires_at = created_at + datetime.timedelta(minutes=30)

    # Сохранение сессии в таблице sessions
    cursor.execute('INSERT INTO sessions (session_id, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)',
                   (session_id, user[0], created_at, expires_at))
    conn.commit()

    conn.close()

    # Возврат токена и идентификатора сессии
    return jsonify({"session_id": session_id}), 200


@app.route('/api/check_auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:  # или любое другое условие проверки сессии
        return jsonify({"logged_in": True})
    return jsonify({"logged_in": False})


# User logout, which clears the session
@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.json.get('session_id')  # Получаем session_id из запроса
    if not session_id:
        return jsonify({"message": "Session ID is required!"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Удаляем сессию из таблицы sessions
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"message": "Session not found!"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

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



@app.route('/update-user/<string:user_id>', methods=['PUT'])
def update_user(user_id):
>>>>>>> Stashed changes
    data = request.get_json()
    new_project = Project(name=data['name'], user_id=current_user.id)

<<<<<<< Updated upstream
    db.session.add(new_project)
    db.session.commit()
=======
    if not full_name or not email:
        return jsonify({"message": "Full name and email are required!"}), 400
>>>>>>> Stashed changes

    for keyword_text in data['keywords']:
        keyword = Keyword(keyword=keyword_text, project_id=new_project.id)
        db.session.add(keyword)

<<<<<<< Updated upstream
    db.session.commit()
    return jsonify({'message': 'Project created successfully'})
=======
    # Update user in the database
    cursor.execute('UPDATE users SET full_name = ?, email = ? WHERE user_id = ?',
                   (full_name, email, user_id))
    conn.commit()
    conn.close()
>>>>>>> Stashed changes

@app.route('/favorites', methods=['POST'], endpoint='favorites')
@token_required
def add_favorite(current_user):
    data = request.get_json()
    project = Project.query.filter_by(id=data['project_id'], user_id=current_user.id).first()

<<<<<<< Updated upstream
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
=======

@app.route('/api/save_interests', methods=['POST'])
def save_interests():
    data = request.json
    user_id = data.get('user_id')
    interests = data.get('interests')  # Список выбранных интересов

    if user_id and interests:
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Преобразуйте список интересов в строку для хранения в БД
            interests_str = ','.join(interests)

            # Обновите запись пользователя с выбранными интересами
            cursor.execute('''UPDATE users SET interests = ? WHERE user_id = ?''', (interests_str, user_id))
            conn.commit()

            return jsonify({'message': 'Interests saved successfully!'}), 200
        except sqlite3.Error as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()

    return jsonify({'error': 'Invalid data'}), 400




# Эндпоинт для вывода информации о пользователе (имя, фамилия, почта)
@app.route('/profile/<uuid:user_id>', methods=['GET'])
# @login_required
def get_user_profile(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT full_name, email FROM users WHERE user_id = ?', (str(user_id),))
    user_data = cursor.fetchone()
    conn.close()
    
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"full_name": user_data[0], "email": user_data[1]}), 200


# руты от гпт, надо будет поправить --------------------------------------------------------------------------------------------------------------------------------------------


# Эндпоинт для вывода интересов пользователя (максимум 3)
@app.route('/profile-interests', methods=['GET'])
@login_required
def get_user_interests():
    user_id = session.get('user_id')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT interests FROM users WHERE user_id = ?', (user_id,))
    interests = cursor.fetchone()
    conn.close()
    
    if interests:
        interests_list = interests[0].split(',')[:3]
        return jsonify({"interests": interests_list}), 200
    return jsonify({"error": "Interests not found"}), 404

# Эндпоинт для вывода проектов пользователя
@app.route('/profile-my-projects', methods=['GET'])
@login_required
def get_user_projects():
    user_id = session.get('user_id')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT project_id, topic, brief_description, keywords FROM projects WHERE user_id_ownership = ?', (user_id,))
    projects = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "project_id": p[0],
            "topic": p[1],
            "brief_description": p[2],
            "keywords": p[3].split(',')  # Преобразуем ключевые слова в список
        }
        for p in projects
    ]), 200


# Эндпоинт для удаления проекта пользователя
@app.route('/profile-my-projects/delete/<uuid:project_id>', methods=['DELETE'])
@login_required
def delete_user_project(project_id):
    user_id = session.get('user_id')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projects WHERE project_id = ? AND user_id_ownership = ?', (project_id, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Project deleted successfully"}), 200

# Эндпоинт для редактирования проекта пользователя
@app.route('/profile-my-projects/edit/<uuid:project_id>', methods=['PUT'])
@login_required
def edit_user_project(project_id):
    user_id = session.get('user_id')
    data = request.get_json()
    topic = data.get('topic')
    description = data.get('description')
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE projects SET topic = ?, detailed_description = ? WHERE project_id = ? AND user_id_ownership = ?',
                   (topic, description, project_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Project updated successfully"}), 200

# Эндпоинт для отображения избранных проектов пользователя
@app.route('/profile-favorites/<user_id>', methods=['GET'])
# @login_required
def get_user_favorites(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Изменяем SQL-запрос для извлечения дополнительных полей
    cursor.execute('''SELECT p.project_id, p.topic, p.brief_description, p.keywords, p.image_url 
                      FROM projects p
                      JOIN favorites f ON f.project_id = p.project_id
                      WHERE f.user_id = ?''', (user_id,))
    
    favorites = cursor.fetchall()
    conn.close()

    # Формируем JSON-ответ с новыми полями
    return jsonify([
        {
            "project_id": f[0],
            "topic": f[1],
            "brief_description": f[2],
            "keywords": f[3],
            "image_url": f[4]
        } for f in favorites
    ]), 200


@app.route('/profile-favorites/delete/<project_id>', methods=['DELETE'])
# @login_required
def delete_user_favorite(project_id):
    user_id = 'f1c43a04-b50f-436b-acfd-bdbade8220e1'  # Используйте хардкод, как указано
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM favorites WHERE project_id = ? AND user_id = ?''', (project_id, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Favorite deleted successfully"}), 200




# Эндпоинт для ленты проектов с фильтром и пагинацией
@app.route('/projects-feed', methods=['GET'])
def get_projects_feed():
    offset = int(request.args.get('offset', 0))
    limit = 4
    keyword_filter = request.args.get('keyword')

    conn = connect_db()
    cursor = conn.cursor()
    if keyword_filter:
        cursor.execute('''
            SELECT project_id, topic, description, keywords, image_url
            FROM projects
            WHERE keywords LIKE ?
            LIMIT ? OFFSET ?
        ''', (f"%{keyword_filter}%", limit, offset))
    else:
        cursor.execute('''
            SELECT project_id, topic, description, keywords, image_url
            FROM projects
            LIMIT ? OFFSET ?
        ''', (limit, offset))

    projects = cursor.fetchall()
    conn.close()

    # Formatting the JSON response with full project details
    project_data = [
        {
            "project_id": p[0],
            "topic": p[1],
            "description": p[2],
            "keywords": p[3].split(','),  # Assuming keywords are stored as a comma-separated string
            "image_url": p[4]
        }
        for p in projects
    ]

    return jsonify(project_data), 200


# руты от гпт выше, надо будет поправить --------------------------------------------------------------------------------------------------------------------------------------------




# Add project route
@app.route('/create-project', methods=['POST'])
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


#Рут для просмотра профиля статьи
@app.route('/project-profile/<int:project_id>', methods=['GET'])
>>>>>>> Stashed changes
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

# Эндпоинт для добавления проекта в избранное
@app.route('/add-fav', methods=['POST'])
def add_fav():
    project_id = request.json.get('project_id')
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

<<<<<<< Updated upstream
# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
=======

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

# Delete project route
@app.route('/delete-project/<string:project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM projects WHERE project_id = ?', (project_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Project deleted successfully!"}), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from the backend!'})


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})



# #заполнение ключевый слов/интересов

# def add_keywords():
#     # Список ключевых слов
#     keywords = [
#         "Project Management",
#         "Прикладная аналитика данных",
#         "Цифровые государственное управление и услуги",
#         "Computer Science",
#         "Software Engineering",
#         "Big Data Analysis",
#         "Media Technologies",
#         "Mathematical and Computational Science",
#         "Big Data in Healthcare",
#         "Cybersecurity",
#         "Smart Technologies",
#         "Industrial Internet of Things",
#         "Electronic Engineering",
#         "IT Management",
#         "IT Entrepreneurship",
#         "AI Business",
#         "Digital Journalism",
#         "Вычислительная техника и информационные сети"
#     ]

#     # Подключение к базе данных
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # Добавление каждого ключевого слова в таблицу
#     for keyword in keywords:
#         #keyword_id = str(uuid.uuid4())  # Создание уникального идентификатора
#         cursor.execute('INSERT INTO keywords (keyword_id, title) VALUES (?, ?)', (generate_uuid, keyword))

#     # Сохранение изменений и закрытие подключения
#     conn.commit()
#     conn.close()

def populate_test_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert test data into keywords table
    keywords_data = [
        (str(uuid.uuid4()), 'Machine Learning'),
        (str(uuid.uuid4()), 'Cybersecurity'),
        (str(uuid.uuid4()), 'Blockchain')
    ]
    cursor.executemany('INSERT INTO keywords (keyword_id, title) VALUES (?, ?)', keywords_data)

    # Insert test data into users table
    users_data = [
        (str(uuid.uuid4()), 'Alice Smith', 'alice@example.com', 'password123', None, None, None),
        (str(uuid.uuid4()), 'Bob Johnson', 'bob@example.com', 'password456', None, None, None),
        (str(uuid.uuid4()), 'Charlie Lee', 'charlie@example.com', 'password789', None, None, None)
    ]
    cursor.executemany('INSERT INTO users (user_id, full_name, email, password, creation_account_date, interests, favorites_id, own_projects_id) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?)', users_data)

    # Insert test data into projects table
    projects_data = [
        (str(uuid.uuid4()), 'AI Research', 'Research in AI advancements', 'Detailed AI project description', keywords_data[0][0], users_data[0][0], 'ai@example.com', '+123456789', 'New York, USA', 'facebook.com/ai', 'linkedin.com/in/ai', 'twitter.com/ai', 'instagram.com/ai'),
        (str(uuid.uuid4()), 'Cyber Defense', 'Developing cyber defense tools', 'Detailed cybersecurity project description', keywords_data[1][0], users_data[1][0], 'cyber@example.com', '+987654321', 'Los Angeles, USA', 'facebook.com/cyber', 'linkedin.com/in/cyber', 'twitter.com/cyber', 'instagram.com/cyber')
    ]
    
    cursor.executemany('''INSERT INTO projects (
                            project_id, topic, brief_description, detailed_description, 
                            keywords, user_id_ownership, email, phone, 
                            city_country, facebook_link, linkedin_link, 
                            twitter_link, instagram_link) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', projects_data)

    # Insert test data into vacancies table
    vacancies_data = [
        (str(uuid.uuid4()), projects_data[0][0], 'AI Specialist'),
        (str(uuid.uuid4()), projects_data[1][0], 'Cybersecurity Analyst')
    ]
    cursor.executemany('INSERT INTO vacancies (vacancy_id, project_id, vacancy_name) VALUES (?, ?, ?)', vacancies_data)

    # Insert test data into favorites table
    favorites_data = [
        (users_data[0][0], projects_data[0][0]),
        (users_data[1][0], projects_data[1][0])
    ]
    cursor.executemany('INSERT INTO favorites (user_id, project_id) VALUES (?, ?)', favorites_data)

    # Insert test data into sessions table with arbitrary dates as strings
    sessions_data = [
        (str(uuid.uuid4()), users_data[0][0], '2023-10-01 00:00:00', '2023-10-02 00:00:00'),  # Example dates as strings
        (str(uuid.uuid4()), users_data[1][0], '2023-10-03 00:00:00', '2023-10-04 00:00:00')
    ]
    cursor.executemany('INSERT INTO sessions (session_id, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)', sessions_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    # populate_test_data()
    app.run(debug=True)
    
>>>>>>> Stashed changes
