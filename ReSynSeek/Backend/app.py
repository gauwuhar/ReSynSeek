from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import jwt
import datetime

app = Flask(__name__)
db_filename = "online_cinema.db"

def create_table():
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                actors TEXT,
                description TEXT,
                release_year INTEGER,
                video_url TEXT,
                rating TEXT,
                stream_url TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Ошибка😡 при создании таблицы: ", e)

@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie = {
            'title': request.form['title'],
            'genre': request.form['genre'],
            'actors': request.form['actors'],
            'description': request.form['description'],
            'release_year': request.form['release_year'],
            'video_url': request.form['video_url'],
            'rating': request.form['rating'],
            'stream_url': request.form['stream_url'],
        }
        add_movie_to_db(movie)
        return redirect(url_for('list_movies'))
    return render_template('add_movie.html')

def add_movie_to_db(movie):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movies (title, genre, actors, description, release_year, video_url, rating, stream_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (movie['title'], movie['genre'], movie['actors'], movie['description'], movie['release_year'], movie['video_url'], movie['rating'], movie['stream_url']))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Ошибка😡 при добавлении фильма: ", e)

@app.route('/list_movies', methods=['GET', 'POST'])
def list_movies():
    create_table()

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        movies = search_movies_in_db(search_query)
    else:
        try:
            conn = sqlite3.connect(db_filename)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM movies')
            movies = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print("Ошибка😡 при выводе списка фильмов: ", e)

    return render_template('list_movies.html', movies=movies)

def search_movies_in_db(query):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movies WHERE title LIKE ?', ('%' + query + '%',))
        movies = cursor.fetchall()
        conn.close()
        return movies
    except sqlite3.Error as e:
        print("Ошибка😡 при поиске фильмов: ", e)
@app.route('/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(movie_id):
    if request.method == 'POST':
        field = request.form['field']
        new_value = request.form['new_value']
        update_movie_in_db(movie_id, field, new_value)
        return redirect(url_for('list_movies'))

    return render_template('update_movie.html', movie_id=movie_id)

def update_movie_in_db(movie_id, field, new_value):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        field_mapping = {
            'title': 'title',
            'genre': 'genre',
            'actors': 'actors',
            'description': 'description',
            'release_year': 'release_year',
            'video_url': 'video_url',
            'rating': 'rating',
            'stream_url': 'stream_url'
        }

        if field in field_mapping:
            db_field = field_mapping[field]
            cursor.execute(f'UPDATE movies SET {db_field}=? WHERE id=?', (new_value, movie_id))
            conn.commit()
            conn.close()
        else:
            print("Ошибка😡: Недопустимое поле для обновления.")
    except sqlite3.Error as e:
        print("Ошибка😡 при обновлении фильма: ", e)

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    delete_movie_from_db(movie_id)
    return redirect(url_for('list_movies'))

def delete_movie_from_db(movie_id):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movies WHERE id=?', (movie_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Ошибка😡 при удалении фильма: ", e)

@app.route('/clear_movies', methods=['GET', 'POST'])
def clear_movies():
    if request.method == 'POST':
        clear_movies_in_db()
        return redirect(url_for('list_movies'))

    return render_template('clear_movies.html')

app.config['SECRET_KEY'] = 'DiasCyberDoter228'
admin_username = "admin"
admin_password = "1337"

def verify_user(username, password):
    return username == admin_username and password == admin_password

@app.route('/loginform')
def login_page():
    return render_template('protected.html')


@app.route('/protected', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if verify_user(username, password):
        jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        return render_template('clear_movies.html')
    else:
        # Display an HTML error message for invalid username or password
        return """
        <h1>Вы - Ошибка</h1>
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.istockphoto.com%2Fphotos%2Fman-searching-a-dark-room-picture-id510614150%3Fk%3D6%26m%3D510614150%26s%3D612x612%26w%3D0%26h%3DREdeKEA7DHcxCGugd_iLIgnn3gHggMYFi64ewq1nT_s%3D&f=1&nofb=1&ipt=84b0bf92f1d4e5ed773fc038474417cdf598fbff9b6faf6728ed4a3d830dade3&ipo=images" class="card-img-top" alt="">
        <h1>Хотели как лучше, а получилось как всегда, да?</h1>
        """

@app.route('/protected_verify')
def protected():
    token = verify_user('token')
    try:
        return jsonify({'token': token})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Срок токена истек⏳. Войдите еще раз'}), 401

    except jwt.InvalidTokenError:
        return jsonify({'message': 'Неверный токен😡. Войдите в систему'}), 401


def clear_movies_in_db():
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movies')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Ошибка😡 при очистке библиотеки: ", e)

if __name__ == '__main__':
    app.run(debug=True)
