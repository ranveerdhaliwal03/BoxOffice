import sqlite3
import os


# Function to initialize and populate the database
def initialize_database():
    # Check if the database already exists
    if not os.path.exists('box_office.db'):
        conn = sqlite3.connect('box_office.db')
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS USERS (
            user_ID INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS MOVIES (
            movie_ID INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            director TEXT,
            year INTEGER,
            length INTEGER,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS ACTORS (
            actor_ID INTEGER PRIMARY KEY,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            nationality TEXT,
            birthday DATE
        );

        CREATE TABLE IF NOT EXISTS WATCHLIST (
            watchlist_ID INTEGER PRIMARY KEY,
            user_ID INTEGER NOT NULL,
            FOREIGN KEY(user_ID) REFERENCES USERS(user_ID)
        );

        CREATE TABLE IF NOT EXISTS WATCHLIST_MOVIE (
            watchlist_ID INTEGER NOT NULL,
            movie_ID INTEGER NOT NULL,
            PRIMARY KEY (watchlist_ID, movie_ID),
            FOREIGN KEY(watchlist_ID) REFERENCES WATCHLIST(watchlist_ID),
            FOREIGN KEY(movie_ID) REFERENCES MOVIES(movie_ID)
        );

        CREATE TABLE IF NOT EXISTS MOVIE_ACTOR (
            movie_ID INTEGER NOT NULL,
            actor_ID INTEGER NOT NULL,
            PRIMARY KEY (movie_ID, actor_ID),
            FOREIGN KEY(movie_ID) REFERENCES MOVIES(movie_ID),
            FOREIGN KEY(actor_ID) REFERENCES ACTORS(actor_ID)
        );

        CREATE TABLE IF NOT EXISTS REVIEW (
            review_ID INTEGER PRIMARY KEY,
            user_ID INTEGER NOT NULL,
            reviewType TEXT NOT NULL CHECK (reviewType IN ('movie', 'actor')),
            movie_ID INTEGER,
            actor_ID INTEGER,
            rating INTEGER CHECK (rating BETWEEN 1 AND 5),
            reviewDate DATE NOT NULL,
            FOREIGN KEY(user_ID) REFERENCES USERS(user_ID),
            FOREIGN KEY(movie_ID) REFERENCES MOVIES(movie_ID),
            FOREIGN KEY(actor_ID) REFERENCES ACTORS(actor_ID)
        );
        """)

        populate_database(cursor, conn)

        conn.commit()
        conn.close()
        print("Database created and populated.")
    else:
        print("Database already exists.")


    
def populate_database(cursor, conn):

    # Populate tables with sample data
        cursor.executescript("""
        INSERT INTO USERS (email, password) VALUES ('admin@email.com', '123');

        INSERT INTO MOVIES (title, director, year, length, description) VALUES
        ('Inception', 'Christopher Nolan', 2010, 148, 'A mind-bending thriller.'),
        ('The Matrix', 'Wachowskis', 1999, 136, 'A hacker discovers a hidden reality.');

        INSERT INTO ACTORS (firstName, lastName, nationality, birthday) VALUES
        ('Leonardo', 'DiCaprio', 'American', '1974-11-11'),
        ('Keanu', 'Reeves', 'Canadian', '1964-09-02');
        """)
        
        conn.commit()
        