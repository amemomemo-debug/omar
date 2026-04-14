import sqlite3

def db():
    return sqlite3.connect("system.db")

# إضافة كتاب شكر
def add_letter(data):
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO letters (emp_id, number, authority, letter_date)
    VALUES (?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# جلب كتب موظف معين
def get_letters(emp_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM letters WHERE emp_id=?
    """, (emp_id,))

    rows = cur.fetchall()
    conn.close()
    return rows
