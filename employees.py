import sqlite3
from datetime import datetime, timedelta

def db():
    return sqlite3.connect("system.db")


def add_employee(data):
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO employees (name, position, job_type, grade, stage, last_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


def get_employees():
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()

    conn.close()
    return rows


# 🟢 حساب الاستحقاق
def calc_due(last_date):
    last = datetime.strptime(last_date, "%Y-%m-%d")
    due = last + timedelta(days=365)
    return due.date()


def is_due(last_date):
    return datetime.today().date() >= calc_due(last_date)
