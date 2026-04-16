import sqlite3

conn = sqlite3.connect("feedback.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        event_id INTEGER,
        text TEXT,
        sentiment TEXT,
        score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
