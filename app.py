from flask import Flask, jsonify, render_template
from initialize_database import *
import sqlite3

app = Flask(__name__)




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

# Serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
