import mysql.connector
import bcrypt
from datetime import datetime

# Connexion à la base de données MySQL
import os
import mysql.connector

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306))
)
cursor = conn.cursor()

# Fonction pour créer les tables si elles n'existent pas
def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_tracking (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            mood INT NOT NULL,
            note TEXT,
            date DATETIME NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)
    conn.commit()

# Appel à cette fonction pour s'assurer que les tables sont créées
create_tables()

# Ajouter un utilisateur
def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False

# Vérifier les informations d'un utilisateur
def check_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    return result and bcrypt.checkpw(password.encode(), result[0].encode())

# Sauvegarder l'humeur d'un utilisateur
def save_mood(username, mood, note):
    cursor.execute("INSERT INTO mood_tracking (username, mood, note, date) VALUES (%s, %s, %s, %s)",
                   (username, mood, note, datetime.now()))
    conn.commit()

# Récupérer l'historique des humeurs d'un utilisateur
def get_user_moods(username):
    cursor.execute("SELECT date, mood, note FROM mood_tracking WHERE username = %s ORDER BY date DESC", (username,))
    return cursor.fetchall()
