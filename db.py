import sqlite3

def connect():
    return sqlite3.connect("system.db")


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        job_type TEXT,
        grade INTEGER,
        stage INTEGER,
        last_date TEXT,
        join_date TEXT DEFAULT (date('now'))
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS letters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        number TEXT,
        authority TEXT,
        letter_date TEXT
    )
    """)

    conn.commit()
    conn.close()
