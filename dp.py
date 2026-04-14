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
        allowance_type TEXT,
        grade TEXT,
        stage INTEGER,
        last_date TEXT
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
