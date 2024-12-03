from flask import Flask, jsonify, render_template, session,  request, redirect
from initialize_database import *
import sqlite3

app = Flask(__name__)
app.secret_key = 'temp'  # Replace with a secure random string


#Serve the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        #check to see if user/pass is in the database
        conn = sqlite3.connect('box_office.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_ID FROM USERS WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:  
            #pass to main page
            session['user_id']= user[0]
            return redirect('/')
        else:
            #retry login page
            return render_template('login.html', error="Invalid email or password. Please try again or sign up.")

    return render_template('login.html')

#Serve the signup page 
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('box_office.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO USERS (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('signup.html', error="Email already exists. Please log in.")

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/watchlist')
def watchlist():
    if 'user_id' not in session:
        return redirect('/login')  # If not logged in, redirect to login

    user_id = session['user_id']

    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()

    # Check if the user already has a watchlist
    cursor.execute("SELECT watchlist_ID FROM WATCHLIST WHERE user_ID = ?", (user_id,))
    watchlist = cursor.fetchone()

    if not watchlist:
        # If no watchlist exists, create one
        cursor.execute("INSERT INTO WATCHLIST (user_ID) VALUES (?)", (user_id,))
        conn.commit()
        cursor.execute("SELECT last_insert_rowid()")
        watchlist_id = cursor.fetchone()[0]
    else:
        watchlist_id = watchlist[0]

    # Fetch the movies in the user's watchlist
    cursor.execute("""
        SELECT MOVIES.title, MOVIES.director, MOVIES.year, MOVIES.length, MOVIES.description 
        FROM WATCHLIST_MOVIE
        JOIN MOVIES ON WATCHLIST_MOVIE.movie_ID = MOVIES.movie_ID
        WHERE WATCHLIST_MOVIE.watchlist_ID = ?
    """, (watchlist_id,))
    watchlist_movies = cursor.fetchall()
    conn.close()

    return render_template('watchlist.html', watchlist_movies=watchlist_movies)

    # Route for adding a movie to the watchlist
@app.route('/add_to_watchlist', methods=['GET', 'POST'])
def add_to_watchlist():
    if 'user_id' not in session:
        return redirect('/login')  # If not logged in, redirect to login
    
    if request.method == 'POST':
        user_id = session['user_id']
        selected_movie_id = request.form['selectedMovieID']
        
        if not selected_movie_id:
            return "Error: No movie selected.", 400
        
        conn = sqlite3.connect('box_office.db')
        cursor = conn.cursor()

        # Insert the movie into the watchlist table
        cursor.execute("""
            INSERT INTO WATCHLIST_MOVIE (watchlist_ID, movie_ID)
            SELECT watchlist_ID, ? FROM WATCHLIST WHERE user_ID = ?
        """, (selected_movie_id, user_id))

        conn.commit()
        conn.close()

        return redirect('/watchlist')  # After adding, redirect to watchlist page

    # Fetch the available movies to choose from
    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movie_ID, title, director, year, length, description FROM MOVIES")
    movies = cursor.fetchall()
    conn.close()

    return render_template('add_to_watchlist.html', movies=movies)

@app.route('/reviews')
def my_reviews():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if not logged in

    user_id = session['user_id']

    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()

    # Fetch reviews created by the user
    cursor.execute("""
        SELECT 
            CASE 
                WHEN r.reviewType = 'movie' THEN (SELECT title FROM MOVIES WHERE movie_ID = r.movie_ID)
                WHEN r.reviewType = 'actor' THEN (SELECT firstName || ' ' || lastName FROM ACTORS WHERE actor_ID = r.actor_ID)
            END AS reviewed_entity,
            r.reviewType,
            r.rating,
            r.reviewDate
        FROM REVIEW r
        WHERE r.user_ID = ?
    """, (user_id,))
    user_reviews = cursor.fetchall()
    conn.close()

    return render_template('reviews.html', user_reviews=user_reviews)


# Serve the write review page
@app.route('/api/movies')
def get_movies():
    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movie_ID AS id, title, director, year, length, description FROM MOVIES")
    movies = [
        {"id": row[0], "title": row[1], "director": row[2], "year": row[3], "length": row[4], "description": row[5]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(movies)


@app.route('/api/actors')
def get_actors():
    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()
    cursor.execute("SELECT actor_ID AS id, firstName || ' ' || lastName AS name, nationality, birthday FROM ACTORS")
    actors = [
        {"id": row[0], "name": row[1], "nationality": row[2], "birthday": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(actors)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if request.method == 'POST':  # Only handle POST requests for review submission
        user_id = session.get('user_id')
        review_type = request.form['reviewType']
        selected_id = request.form['selectedID']
        rating = request.form['rating']
        review_date = request.form['reviewDate']

        if not user_id or not selected_id:
            return "Error: Missing user or selection.", 400

        conn = sqlite3.connect('box_office.db')
        cursor = conn.cursor()

        if review_type == 'movie':
            cursor.execute(
                "INSERT INTO REVIEW (user_ID, reviewType, movie_ID, rating, reviewDate) VALUES (?, ?, ?, ?, ?)",
                (user_id, review_type, selected_id, rating, review_date)
            )
        elif review_type == 'actor':
            cursor.execute(
                "INSERT INTO REVIEW (user_ID, reviewType, actor_ID, rating, reviewDate) VALUES (?, ?, ?, ?, ?)",
                (user_id, review_type, selected_id, rating, review_date)
            )
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('write_review.html')  # GET request will render the form

# Serve the main HTML page
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
        
    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()

    # Query for top 10 rated movies
    cursor.execute("""
        SELECT m.title, ROUND(AVG(r.rating), 1) AS avg_rating
        FROM MOVIES m
        JOIN REVIEW r ON m.movie_ID = r.movie_ID
        WHERE r.reviewType = 'movie'
        GROUP BY m.movie_ID
        ORDER BY avg_rating DESC
        LIMIT 5;
    """)
    top_movies = cursor.fetchall()

    # Query for top 5 rated actors
    cursor.execute("""
        SELECT a.firstName || ' ' || a.lastName AS actor_name, ROUND(AVG(r.rating), 1) AS avg_rating
        FROM ACTORS a
        JOIN REVIEW r ON a.actor_ID = r.actor_ID
        WHERE r.reviewType = 'actor'
        GROUP BY a.actor_ID
        ORDER BY avg_rating DESC
        LIMIT 5;
    """)
    top_actors = cursor.fetchall()

    conn.close()

    return render_template('index.html', top_movies=top_movies, top_actors=top_actors)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
