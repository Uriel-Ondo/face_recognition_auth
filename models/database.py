import sqlite3
import pickle
import numpy as np

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            face_encoding BLOB NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_user(username, password, face_encoding):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Convertir l'encodage facial en binaire
    face_encoding_blob = pickle.dumps(face_encoding)

    cursor.execute("INSERT INTO users (username, password, face_encoding) VALUES (?, ?, ?)",
                   (username, password, face_encoding_blob))
    
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT username, password, face_encoding FROM users")
    users = cursor.fetchall()

    conn.close()
    
    return [(username, password, pickle.loads(face_encoding)) for username, password, face_encoding in users]

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password, face_encoding FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password, stored_face_encoding = result
        return stored_password == password, pickle.loads(stored_face_encoding)
    
    return False, None
