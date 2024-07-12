import sqlite3

DATABASE = 'image_recognition.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    ### uploads table ###
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS uploads(
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        uploadPath TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        label TEXT,
        recognition_result TEXT,
        upload_id INTEGER,
        FOREIGN KEY (upload_id) REFERENCES uploads (id)
    )
    ''')
    conn.commit()
    conn.close()