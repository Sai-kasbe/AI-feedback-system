import sqlite3

conn = sqlite3.connect("feedback.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    event TEXT,
                    text TEXT,
                    sentiment TEXT,
                    score REAL
                )''')
    conn.commit()
