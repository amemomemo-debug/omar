import sqlite3
from datetime import datetime

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


# ================= ترقيات تلقائية =================

def check_promotion(employee):
    """
    employee = (id, name, position, job_type, grade, stage, last_date, join_date)
    """

    emp_id = employee[0]
    grade = int(employee[4])
    stage = int(employee[5])
    last_date = employee[6]

    today = datetime.today()
    last = datetime.strptime(last_date, "%Y-%m-%d")

    years = (today - last).days // 365

    promotion = None

    # ================= علاوة كل سنة =================
    if years >= 1:
        stage -= 1
        last = today
        promotion = "علاوة"

    # ================= ترفيع كل 4 سنوات =================
    if grade > 1 and years >= 4:
        grade -= 1
        stage = 5
        last = today
        promotion = "ترفيع"

    conn = db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE employees
    SET grade=?, stage=?, last_date=?
    WHERE id=?
    """, (grade, stage, last.strftime("%Y-%m-%d"), emp_id))

    conn.commit()
    conn.close()

    return promotion


def run_promotions():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    conn.close()

    results = []

    for emp in rows:
        res = check_promotion(emp)
        if res:
            results.append((emp[1], res))

    return results
