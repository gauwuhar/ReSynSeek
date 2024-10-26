import sqlite3

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

  cursor.execute('''CREATE TABLE IF NOT EXISTS scientific_interests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title INTEGER NOT NULL,
                        user_id INTEGER NOT NULL)''')

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
