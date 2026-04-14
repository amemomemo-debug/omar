import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import sqlite3
import shutil
import pandas as pd

# ========================
# DATABASE
# ========================

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

# ========================
# LOGIN SYSTEM
# ========================

USERNAME = "admin"
PASSWORD = "1234"

def check_login():

    if user_entry.get() == USERNAME and pass_entry.get() == PASSWORD:
        login.destroy()
        open_main()
    else:
        messagebox.showerror("خطأ", "اسم المستخدم او كلمة المرور غير صحيحة")

# ========================
# SERVICE CALCULATION
# ========================

def calculate_service(date, minister, university, pm, president):

    counted = min(minister + university,3)
    counted += min(pm + president,2) * 3

    not_counted = (minister + university + pm + president) - counted

    return counted, not_counted


# ========================
# ADD EMPLOYEE
# ========================

def add_employee():

    name = name_entry.get()
    title = title_combo.get()
    hire = date_entry.get()

    minister = int(minister_entry.get() or 0)
    university = int(university_entry.get() or 0)
    pm = int(pm_entry.get() or 0)
    president = int(president_entry.get() or 0)

    cursor.execute("""
    INSERT INTO employees
    (name,title,hire_date,minister_books,university_books,pm_books,president_books)
    VALUES(?,?,?,?,?,?,?)
    """,(name,title,hire,minister,university,pm,president))

    conn.commit()

    load_data()

# ========================
# LOAD TABLE
# ========================

def load_data():

    for row in table.get_children():
        table.delete(row)

    cursor.execute("SELECT * FROM employees")

    for r in cursor.fetchall():

        counted, not_counted = calculate_service(
        r[3],r[4],r[5],r[6],r[7]
        )

        table.insert("",tk.END,values=(
        r[1],
        r[2],
        r[3],
        counted,
        not_counted
        ))

# ========================
# DELETE
# ========================

def delete_employee():

    selected = table.focus()

    if not selected:
        return

    values = table.item(selected,"values")

    cursor.execute("DELETE FROM employees WHERE name=?",(values[0],))
    conn.commit()

    load_data()

# ========================
# BACKUP
# ========================

def backup():

    path = filedialog.asksaveasfilename(defaultextension=".db")

    if path:
        shutil.copy("hr_system.db",path)
        messagebox.showinfo("تم","تم اخذ نسخة احتياطية")


# ========================
# EXPORT EXCEL
# ========================

def export_excel():

    cursor.execute("SELECT * FROM employees")

    data = cursor.fetchall()

    rows = []

    for r in data:

        counted,not_counted = calculate_service(
        r[3],r[4],r[5],r[6],r[7]
        )

        rows.append({
        "الاسم":r[1],
        "الصفة":r[2],
        "تاريخ التعيين":r[3],
        "القدم المحتسبة":counted,
        "غير المحتسبة":not_counted
        })

    df = pd.DataFrame(rows)

    path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    if path:
        df.to_excel(path,index=False)
        messagebox.showinfo("تم","تم تصدير الملف")


# ========================
# MAIN WINDOW
# ========================

def open_main():

    global table
    global name_entry
    global title_combo
    global date_entry
    global minister_entry
    global university_entry
    global pm_entry
    global president_entry

    root = tk.Tk()
    root.title("نظام الموارد البشرية")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame,text="الاسم").grid(row=0,column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0,column=1)

    tk.Label(frame,text="الصفة").grid(row=0,column=2)
    title_combo = ttk.Combobox(frame,values=["موظف","تدريسي","درجة خاصة"])
    title_combo.grid(row=0,column=3)

    tk.Label(frame,text="تاريخ التعيين").grid(row=1,column=0)
    date_entry = DateEntry(frame)
    date_entry.grid(row=1,column=1)

    tk.Label(frame,text="كتب الوزير").grid(row=2,column=0)
    minister_entry = tk.Entry(frame,width=5)
    minister_entry.grid(row=2,column=1)

    tk.Label(frame,text="كتب رئيس الجامعة").grid(row=2,column=2)
    university_entry = tk.Entry(frame,width=5)
    university_entry.grid(row=2,column=3)

    tk.Label(frame,text="كتب رئيس الوزراء").grid(row=3,column=0)
    pm_entry = tk.Entry(frame,width=5)
    pm_entry.grid(row=3,column=1)

    tk.Label(frame,text="كتب رئيس الجمهورية").grid(row=3,column=2)
    president_entry = tk.Entry(frame,width=5)
    president_entry.grid(row=3,column=3)

    tk.Button(frame,text="اضافة موظف",command=add_employee).grid(row=4,column=1,pady=10)

    tk.Button(frame,text="حذف",command=delete_employee).grid(row=4,column=2)

    tk.Button(frame,text="Backup",command=backup).grid(row=4,column=3)

    tk.Button(frame,text="تصدير Excel",command=export_excel).grid(row=4,column=4)

    columns=("الاسم","الصفة","تاريخ التعيين","القدم المحتسبة","غير المحتسبة")

    table = ttk.Treeview(root,columns=columns,show="headings")

    for c in columns:
        table.heading(c,text=c)

    table.pack(fill="both",expand=True)

    load_data()

    root.mainloop()


# ========================
# LOGIN WINDOW
# ========================

login = tk.Tk()
login.title("تسجيل الدخول")

tk.Label(login,text="Username").pack()

user_entry = tk.Entry(login)
user_entry.pack()

tk.Label(login,text="Password").pack()

pass_entry = tk.Entry(login,show="*")
pass_entry.pack()

tk.Button(login,text="Login",command=check_login).pack(pady=10)

login.mainloop()
