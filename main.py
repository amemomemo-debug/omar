import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import sqlite3
import shutil
import pandas as pd

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("hr_system.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
title TEXT,
hire_date TEXT,
minister_books INTEGER,
university_books INTEGER,
pm_books INTEGER,
president_books INTEGER
)
""")

conn.commit()

# =========================
# LOGIN
# =========================

USERNAME = "admin"
PASSWORD = "1234"

def check_login():
    if user_entry.get() == USERNAME and pass_entry.get() == PASSWORD:
        login.destroy()
        open_main()
    else:
        messagebox.showerror("خطأ", "بيانات الدخول غير صحيحة")

# =========================
# CALCULATION
# =========================

def calculate_service(minister, university, pm, president):

    counted = min(minister + university, 3)
    counted += min(pm + president, 2) * 3

    total = minister + university + pm + president
    not_counted = total - counted

    return counted, not_counted

# =========================
# ADD EMPLOYEE
# =========================

def add_employee():

    cursor.execute("""
    INSERT INTO employees
    (name,title,hire_date,minister_books,university_books,pm_books,president_books)
    VALUES (?,?,?,?,?,?,?)
    """,(
        name_entry.get(),
        title_combo.get(),
        date_entry.get(),
        int(minister_entry.get() or 0),
        int(university_entry.get() or 0),
        int(pm_entry.get() or 0),
        int(president_entry.get() or 0)
    ))

    conn.commit()
    load_data()

# =========================
# LOAD DATA
# =========================

def load_data():

    for i in table.get_children():
        table.delete(i)

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    for r in rows:

        counted, not_counted = calculate_service(
            r[4], r[5], r[6], r[7]
        )

        table.insert("", "end", values=(
            r[1], r[2], r[3], counted, not_counted
        ))

# =========================
# DELETE
# =========================

def delete_employee():

    selected = table.focus()
    if not selected:
        return

    data = table.item(selected)["values"]

    cursor.execute("DELETE FROM employees WHERE name=?", (data[0],))
    conn.commit()

    load_data()

# =========================
# BACKUP
# =========================

def backup_db():

    file = filedialog.asksaveasfilename(defaultextension=".db")

    if file:
        shutil.copy("hr_system.db", file)
        messagebox.showinfo("تم", "تم إنشاء نسخة احتياطية")

# =========================
# EXPORT EXCEL
# =========================

def export_excel():

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    data = []

    for r in rows:

        counted, not_counted = calculate_service(
            r[4], r[5], r[6], r[7]
        )

        data.append([
            r[1],
            r[2],
            r[3],
            counted,
            not_counted
        ])

    df = pd.DataFrame(data, columns=[
        "الاسم",
        "الصفة",
        "تاريخ التعيين",
        "القدم المحتسبة",
        "القدم غير المحتسبة"
    ])

    file = filedialog.asksaveasfilename(defaultextension=".xlsx")

    if file:
        df.to_excel(file, index=False)
        messagebox.showinfo("تم", "تم التصدير")

# =========================
# MAIN APP
# =========================

def open_main():

    global table
    global name_entry, title_combo, date_entry
    global minister_entry, university_entry, pm_entry, president_entry

    root = tk.Tk()
    root.title("نظام الموارد البشرية")
    root.geometry("1000x600")

    frame = tk.Frame(root)
    frame.pack()

    tk.Label(frame, text="الاسم").grid(row=0, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1)

    tk.Label(frame, text="الصفة").grid(row=0, column=2)
    title_combo = ttk.Combobox(frame, values=["موظف", "تدريسي", "درجة خاصة"])
    title_combo.grid(row=0, column=3)

    tk.Label(frame, text="تاريخ التعيين").grid(row=1, column=0)
    date_entry = DateEntry(frame)
    date_entry.grid(row=1, column=1)

    tk.Label(frame, text="كتب الوزير").grid(row=2, column=0)
    minister_entry = tk.Entry(frame)
    minister_entry.grid(row=2, column=1)

    tk.Label(frame, text="كتب الجامعة").grid(row=2, column=2)
    university_entry = tk.Entry(frame)
    university_entry.grid(row=2, column=3)

    tk.Label(frame, text="كتب رئيس الوزراء").grid(row=3, column=0)
    pm_entry = tk.Entry(frame)
    pm_entry.grid(row=3, column=1)

    tk.Label(frame, text="كتب الرئيس").grid(row=3, column=2)
    president_entry = tk.Entry(frame)
    president_entry.grid(row=3, column=3)

    tk.Button(frame, text="إضافة موظف", command=add_employee).grid(row=4, column=0)
    tk.Button(frame, text="حذف", command=delete_employee).grid(row=4, column=1)
    tk.Button(frame, text="Backup", command=backup_db).grid(row=4, column=2)
    tk.Button(frame, text="Excel", command=export_excel).grid(row=4, column=3)

    columns = (
        "الاسم",
        "الصفة",
        "التعيين",
        "القدم المحتسبة",
        "القدم غير المحتسبة"
    )

    table = ttk.Treeview(root, columns=columns, show="headings")

    for c in columns:
        table.heading(c, text=c)

    table.pack(fill="both", expand=True)

    load_data()

    root.mainloop()

# =========================
# LOGIN WINDOW
# =========================

login = tk.Tk()
login.title("تسجيل الدخول")

tk.Label(login, text="Username").pack()
user_entry = tk.Entry(login)
user_entry.pack()

tk.Label(login, text="Password").pack()
pass_entry = tk.Entry(login, show="*")
pass_entry.pack()

tk.Button(login, text="دخول", command=check_login).pack()

login.mainloop()
