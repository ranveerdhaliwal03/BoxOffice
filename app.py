from flask import Flask, jsonify, render_template, session,  request, redirect
from initialize_database import *
import sqlite3

app = Flask(__name__)
app.secret_key = 'temp'  # Replace with a secure random string


# Fetch movies from the database
@app.route('/movies')
def get_movies():
    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM MOVIES")
    movies = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(movies)

# Fetch actors from the database
@app.route('/actors')
def get_actors():
    conn = sqlite3.connect('box_office.db')
    cursor = conn.cursor()
    cursor.execute("SELECT firstName || ' ' || lastName FROM ACTORS")
    actors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(actors)

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

# Serve the main HTML page
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
        
    return render_template('index.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
