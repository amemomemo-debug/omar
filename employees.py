import sqlite3

def db():
    return sqlite3.connect("system.db")

# إضافة موظف
def add_employee(data):
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO employees
    (name, position, allowance_type, grade, stage, last_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# جلب الموظفين
def get_employees():
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()

    conn.close()
    return rows


# حذف موظف
def delete_employee(emp_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))

    conn.commit()
    conn.close()
