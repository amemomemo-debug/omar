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

# ================= DATABASE =================
def db():
    return sqlite3.connect("system.db")

# ================= LOGIN SYSTEM =================
USERS = {
    "admin": "1234",
    "omar": "0000"
}

login_root = tk.Tk()
login_root.title("تسجيل الدخول")
login_root.geometry("300x200")

def open_main():
    login_root.destroy()
    main_app()

def check_login():
    u = user.get()
    p = password.get()

    if u in USERS and USERS[u] == p:
        open_main()
    else:
        messagebox.showerror("خطأ", "بيانات الدخول غير صحيحة")

tk.Label(login_root, text="اسم المستخدم").pack()
user = tk.Entry(login_root)
user.pack()

tk.Label(login_root, text="كلمة المرور").pack()
password = tk.Entry(login_root, show="*")
password.pack()

tk.Button(login_root, text="دخول", command=check_login).pack(pady=10)

# ================= MAIN APP =================
def main_app():

    root = tk.Tk()
    root.title("HR SYSTEM")
    root.geometry("1400x850")

    selected_emp_id = None

    # ================= SAVE EMP =================
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

    # ================= LOAD EMP =================
    def load_emps():
        for i in emp_tree.get_children():
            emp_tree.delete(i)

        for row in get_employees():
            emp_tree.insert("", "end", values=row)

    # ================= SELECT EMP =================
    def select_emp(event):
        nonlocal selected_emp_id
        selected = emp_tree.selection()
        if selected:
            emp = emp_tree.item(selected[0])["values"]
            selected_emp_id = emp[0]
            load_letters()

    # ================= DELETE =================
    def delete_emp():
        if not selected_emp_id:
            return

        conn = db()
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=?", (selected_emp_id,))
        conn.commit()
        conn.close()

        load_emps()
        messagebox.showinfo("تم", "تم الحذف")

    # ================= SEARCH =================
    def search_emp():
        k = search.get()

        for i in emp_tree.get_children():
            emp_tree.delete(i)

        conn = db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE name LIKE ?", ('%'+k+'%',))
        rows = cur.fetchall()
        conn.close()

        for r in rows:
            emp_tree.insert("", "end", values=r)

    # ================= BACKUP MANUAL =================
    def backup_db():
        file = filedialog.asksaveasfilename(defaultextension=".db")
        if file:
            conn = sqlite3.connect("system.db")
            backup = sqlite3.connect(file)

            with backup:
                conn.backup(backup)

            backup.close()
            conn.close()

            messagebox.showinfo("تم", "تم إنشاء نسخة احتياطية")

    # ================= LETTERS =================
    def add_letter_ui():
        if not selected_emp_id:
            return

        result = add_letter((
            selected_emp_id,
            letter_number.get(),
            authority.get(),
            letter_date.get()
        ))

        if result == "duplicate":
            messagebox.showerror("خطأ", "رقم مكرر")

        load_letters()

    def load_letters():
        for i in used_tree.get_children():
            used_tree.delete(i)
        for i in unused_tree.get_children():
            unused_tree.delete(i)

        if not selected_emp_id:
            return

        letters = get_letters(selected_emp_id)

        used = 0

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

    # ================= AUTO PROMO =================
    def check_auto_promotions():
        res = run_promotions()
        if res:
            msg = "\n".join([f"{r[0]} => {r[1]}" for r in res])
            messagebox.showinfo("ترقيات", msg)

    # ================= UI =================
    top = tk.Frame(root)
    top.pack()

    tk.Label(top, text="بحث").grid(row=0, column=0)
    search = tk.Entry(top)
    search.grid(row=0, column=1)

    tk.Button(top, text="بحث", command=search_emp).grid(row=0, column=2)
    tk.Button(top, text="حذف", command=delete_emp).grid(row=0, column=3)
    tk.Button(top, text="نسخة احتياطية", command=backup_db).grid(row=0, column=4)

    # ================= EMP =================
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

    tk.Button(frame, text="حفظ", command=save_emp).grid(row=1, column=6)

    # ================= TABLE =================
    emp_tree = ttk.Treeview(root, columns=("id","name","pos","type","grade","stage","date"), show="headings")
    for c in emp_tree["columns"]:
        emp_tree.heading(c, text=c)

    emp_tree.pack(fill="x")
    emp_tree.bind("<ButtonRelease-1>", select_emp)

    load_emps()

    # ================= LETTER =================
    letter_frame = tk.Frame(root)
    letter_frame.pack()

    tk.Label(letter_frame, text="رقم").grid(row=0, column=0)
    letter_number = tk.Entry(letter_frame)
    letter_number.grid(row=0, column=1)

    tk.Label(letter_frame, text="الجهة").grid(row=0, column=2)
    authority = ttk.Combobox(letter_frame, values=[
        "رئيس الجامعة","الوزير","رئيس الوزراء","رئيس الجمهورية"
    ])
    authority.grid(row=0, column=3)

    tk.Label(letter_frame, text="تاريخ").grid(row=0, column=4)
    letter_date = DateEntry(letter_frame)
    letter_date.grid(row=0, column=5)

    tk.Button(letter_frame, text="إضافة كتاب", command=add_letter_ui).grid(row=0, column=6)

    # ================= TABLES =================
    tables = tk.Frame(root)
    tables.pack()

    tk.Label(tables, text="محتسبة").grid(row=0, column=0)
    used_tree = ttk.Treeview(tables, columns=("id","emp","num","auth","date"), show="headings", height=10)
    for c in used_tree["columns"]:
        used_tree.heading(c, text=c)
    used_tree.grid(row=1, column=0)

    tk.Label(tables, text="غير محتسبة").grid(row=0, column=1)
    unused_tree = ttk.Treeview(tables, columns=("id","emp","num","auth","date"), show="headings", height=10)
    for c in unused_tree["columns"]:
        unused_tree.heading(c, text=c)
    unused_tree.grid(row=1, column=1)

    root.after(2000, check_auto_promotions)

    root.mainloop()

login_root.mainloop()
