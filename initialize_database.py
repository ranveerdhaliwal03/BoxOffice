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

    
def populate_database(cursor, conn):

      # Insert USERS
    cursor.executescript("""
    INSERT INTO USERS (email, password) VALUES
    ('admin@email.com', '123'),
    ('user1@email.com', 'password1'),
    ('user2@email.com', 'password2'),
    ('user3@email.com', 'password3'),
    ('user4@email.com', 'password4');
    """)

    # Insert MOVIES
    cursor.executescript("""
    INSERT INTO MOVIES (title, director, year, length, description) VALUES
    ('Inception', 'Christopher Nolan', 2010, 148, 'A mind-bending thriller.'),
    ('The Matrix', 'Wachowskis', 1999, 136, 'A hacker discovers a hidden reality.'),
    ('The Dark Knight', 'Christopher Nolan', 2008, 152, 'A gritty superhero tale.'),
    ('Forrest Gump', 'Robert Zemeckis', 1994, 142, 'The life of an extraordinary man.'),
    ('Pulp Fiction', 'Quentin Tarantino', 1994, 154, 'A story of intertwining lives.'),
    ('Interstellar', 'Christopher Nolan', 2014, 169, 'A journey through space and time.'),
    ('The Godfather', 'Francis Ford Coppola', 1972, 175, 'A story of a crime family.'),
    ('Fight Club', 'David Fincher', 1999, 139, 'An underground fight club emerges.'),
    ('The Shawshank Redemption', 'Frank Darabont', 1994, 144, 'Hope and redemption in prison.'),
    ('Gladiator', 'Ridley Scott', 2000, 155, 'A betrayed Roman general seeks revenge.');
    """)

    # Insert ACTORS
    cursor.executescript("""
    INSERT INTO ACTORS (firstName, lastName, nationality, birthday) VALUES
    ('Leonardo', 'DiCaprio', 'American', '1974-11-11'),
    ('Joseph', 'Gordon-Levitt', 'American', '1981-02-17'),
    ('Keanu', 'Reeves', 'Canadian', '1964-09-02'),
    ('Carrie-Anne', 'Moss', 'Canadian', '1967-08-21'),
    ('Christian', 'Bale', 'British', '1974-01-30'),
    ('Heath', 'Ledger', 'Australian', '1979-04-04'),
    ('Tom', 'Hanks', 'American', '1956-07-09'),
    ('Robin', 'Wright', 'American', '1966-04-08'),
    ('John', 'Travolta', 'American', '1954-02-18'),
    ('Samuel', 'Jackson', 'American', '1948-12-21'),
    ('Matthew', 'McConaughey', 'American', '1969-11-04'),
    ('Anne', 'Hathaway', 'American', '1982-11-12'),
    ('Marlon', 'Brando', 'American', '1924-04-03'),
    ('Al', 'Pacino', 'American', '1940-04-25'),
    ('Edward', 'Norton', 'American', '1969-08-18'),
    ('Brad', 'Pitt', 'American', '1963-12-18'),
    ('Morgan', 'Freeman', 'American', '1937-06-01'),
    ('Tim', 'Robbins', 'American', '1958-10-16'),
    ('Russell', 'Crowe', 'Australian', '1964-04-07'),
    ('Joaquin', 'Phoenix', 'American', '1974-10-28');
    """)

    # Insert MOVIE_ACTOR relationships
    cursor.executescript("""
    INSERT INTO MOVIE_ACTOR (movie_ID, actor_ID) VALUES
    (1, 1), (1, 2), (2, 3), (2, 4),
    (3, 5), (3, 6), (4, 7), (4, 8),
    (5, 9), (5, 10), (6, 11), (6, 12),
    (7, 13), (7, 14), (8, 15), (8, 16),
    (9, 17), (9, 18), (10, 19), (10, 20);
    """)

    # Insert REVIEWS for users
    cursor.executescript("""
    INSERT INTO REVIEW (user_ID, reviewType, movie_ID, actor_ID, rating, reviewDate) VALUES
    -- User 1
    (2, 'movie', 1, NULL, 5, '2024-12-01'),
    (2, 'actor', NULL, 1, 4, '2024-12-01'),
    (2, 'movie', 2, NULL, 4, '2024-12-01'),
    -- User 2
    (3, 'movie', 3, NULL, 5, '2024-12-01'),
    (3, 'actor', NULL, 7, 5, '2024-12-01'),
    (3, 'movie', 5, NULL, 4, '2024-12-01'),
    -- User 3
    (4, 'actor', NULL, 14, 5, '2024-12-01'),
    (4, 'movie', 6, NULL, 3, '2024-12-01'),
    (4, 'actor', NULL, 19, 5, '2024-12-01'),
    -- User 4
    (5, 'movie', 9, NULL, 4, '2024-12-01'),
    (5, 'actor', NULL, 20, 5, '2024-12-01'),
    (5, 'movie', 8, NULL, 4, '2024-12-01');
    """)