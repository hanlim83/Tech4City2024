import sqlite3

DATABASE = 'image_recognition.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        label TEXT,
        recognition_result TEXT
    )
    ''')
    conn.commit()
    conn.close()