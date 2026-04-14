import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import sqlite3
import csv
import os

from db import init_db
from employees import add_employee, get_employees, run_promotions
from letters import add_letter, get_letters

init_db()

# ================= WINDOW =================
root = tk.Tk()
root.title("HR SYSTEM - نظام إدارة الموظفين")
root.geometry("1400x850")

selected_emp_id = None

# ================= TITLE =================
tk.Label(root, text="نظام إدارة الموارد البشرية", font=("Arial", 20, "bold")).pack(pady=10)

# ================= DATABASE HELP =================
def db():
    return sqlite3.connect("system.db")

# ================= EMPLOYEE FUNCTIONS =================
def save_emp():
    if name.get() == "":
        messagebox.showerror("خطأ", "اسم الموظف فارغ")
        return

    add_employee((
        name.get(),
        position.get(),
        job_type.get(),
        grade.get(),
        stage.get(),
        last_date.get()
    ))

    load_emps()
    messagebox.showinfo("تم", "تم إضافة الموظف")

def load_emps():
    for i in emp_tree.get_children():
        emp_tree.delete(i)

    for row in get_employees():
        emp_tree.insert("", "end", values=row)

def select_emp(event):
    global selected_emp_id
    selected = emp_tree.selection()
    if selected:
        emp = emp_tree.item(selected[0])["values"]
        selected_emp_id = emp[0]
        load_letters()

# ================= EMPLOYEE DELETE =================
def delete_emp():
    if not selected_emp_id:
        return

    conn = db()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id=?", (selected_emp_id,))
    conn.commit()
    conn.close()

    load_emps()
    messagebox.showinfo("تم", "تم حذف الموظف")

# ================= SEARCH =================
def search_emp():
    keyword = search.get()

    for i in emp_tree.get_children():
        emp_tree.delete(i)

    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + keyword + '%',))
    rows = cur.fetchall()
    conn.close()

    for r in rows:
        emp_tree.insert("", "end", values=r)

# ================= LETTERS =================
def add_letter_ui():
    if not selected_emp_id:
        messagebox.showwarning("تنبيه", "اختر موظف")
        return

    result = add_letter((
        selected_emp_id,
        letter_number.get(),
        authority.get(),
        letter_date.get()
    ))

    if result == "duplicate":
        messagebox.showerror("خطأ", "رقم الكتاب مكرر")
        return

    load_letters()

# ================= LOAD LETTERS =================
def load_letters():
    for i in used_tree.get_children():
        used_tree.delete(i)
    for i in unused_tree.get_children():
        unused_tree.delete(i)

    if not selected_emp_id:
        return

    letters = get_letters(selected_emp_id)

    used = 0
    unused = 0

    for l in letters:
        auth = l[3]

        if auth in ["رئيس الجامعة", "الوزير"] and used < 3:
            used_tree.insert("", "end", values=l)
            used += 1
        elif auth in ["رئيس الوزراء", "رئيس الجمهورية"] and used < 2:
            used_tree.insert("", "end", values=l)
            used += 1
        else:
            unused_tree.insert("", "end", values=l)

# ================= PROMOTION =================
def check_auto_promotions():
    results = run_promotions()
    if results:
        msg = "\n".join([f"{r[0]} => {r[1]}" for r in results])
        messagebox.showinfo("ترقيات تلقائية", msg)

# ================= EMP DETAIL =================
def open_profile():
    if not selected_emp_id:
        return

    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id=?", (selected_emp_id,))
    emp = cur.fetchone()
    conn.close()

    win = tk.Toplevel(root)
    win.title("ملف الموظف")
    win.geometry("400x400")

    tk.Label(win, text="ملف الموظف", font=("Arial", 16, "bold")).pack()

    tk.Label(win, text=str(emp)).pack(pady=20)

# ================= EXPORT CSV =================
def export_excel():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    conn.close()

    file = filedialog.asksaveasfilename(defaultextension=".csv")

    if file:
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","Name","Position","Type","Grade","Stage","Date"])
            writer.writerows(rows)

        messagebox.showinfo("تم", "تم التصدير")

# ================= UI =================
top = tk.Frame(root)
top.pack()

tk.Label(top, text="بحث").grid(row=0, column=0)
search = tk.Entry(top)
search.grid(row=0, column=1)

tk.Button(top, text="بحث", command=search_emp).grid(row=0, column=2)
tk.Button(top, text="حذف", command=delete_emp).grid(row=0, column=3)
tk.Button(top, text="ملف الموظف", command=open_profile).grid(row=0, column=4)
tk.Button(top, text="تصدير CSV", command=export_excel).grid(row=0, column=5)

# ================= EMP INPUT =================
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="الاسم").grid(row=0, column=0)
name = tk.Entry(frame)
name.grid(row=0, column=1)

tk.Label(frame, text="المنصب").grid(row=0, column=2)
position = ttk.Combobox(frame, values=[
    "رئيس الجامعة","الوزير","رئيس الوزراء","رئيس الجمهورية","عميد كلية"
])
position.grid(row=0, column=3)

tk.Label(frame, text="نوع").grid(row=0, column=4)
job_type = ttk.Combobox(frame, values=["تدريسي","درجة خاصة"])
job_type.grid(row=0, column=5)

tk.Label(frame, text="الدرجة").grid(row=1, column=0)
grade = tk.Entry(frame)
grade.grid(row=1, column=1)

tk.Label(frame, text="المرحلة").grid(row=1, column=2)
stage = tk.Entry(frame)
stage.grid(row=1, column=3)

tk.Label(frame, text="آخر علاوة").grid(row=1, column=4)
last_date = DateEntry(frame, date_pattern="yyyy-mm-dd")
last_date.grid(row=1, column=5)

tk.Button(frame, text="حفظ", command=save_emp, bg="green", fg="white").grid(row=1, column=6)

# ================= EMP TABLE =================
emp_tree = ttk.Treeview(root, columns=("id","name","position","type","grade","stage","date"), show="headings")
for c in emp_tree["columns"]:
    emp_tree.heading(c, text=c)

emp_tree.pack(fill="x")
emp_tree.bind("<ButtonRelease-1>", select_emp)

load_emps()

# ================= LETTER INPUT =================
letter_frame = tk.Frame(root)
letter_frame.pack()

tk.Label(letter_frame, text="رقم").grid(row=0,column=0)
letter_number = tk.Entry(letter_frame)
letter_number.grid(row=0,column=1)

tk.Label(letter_frame, text="الجهة").grid(row=0,column=2)
authority = ttk.Combobox(letter_frame, values=[
    "رئيس الجامعة","الوزير","رئيس الوزراء","رئيس الجمهورية"
])
authority.grid(row=0,column=3)

tk.Label(letter_frame, text="تاريخ").grid(row=0,column=4)
letter_date = DateEntry(letter_frame, date_pattern="yyyy-mm-dd")
letter_date.grid(row=0,column=5)

tk.Button(letter_frame, text="إضافة كتاب", command=add_letter_ui).grid(row=0,column=6)

# ================= TABLES =================
tables = tk.Frame(root)
tables.pack(fill="both", expand=True)

tk.Label(tables, text="محتسبة").grid(row=0,column=0)
used_tree = ttk.Treeview(tables, columns=("id","emp","num","auth","date"), show="headings", height=10)
for c in used_tree["columns"]:
    used_tree.heading(c, text=c)
used_tree.grid(row=1,column=0)

tk.Label(tables, text="غير محتسبة").grid(row=0,column=1)
unused_tree = ttk.Treeview(tables, columns=("id","emp","num","auth","date"), show="headings", height=10)
for c in unused_tree["columns"]:
    unused_tree.heading(c, text=c)
unused_tree.grid(row=1,column=1)

# ================= AUTO =================
root.after(3000, check_auto_promotions)

root.mainloop()
