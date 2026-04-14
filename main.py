import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

from db import init_db
from employees import add_employee, get_employees

init_db()

root = tk.Tk()
root.title("نظام شؤون الموظفين")
root.geometry("1000x650")

# ================= عنوان =================
tk.Label(root, text="نظام شؤون الموظفين", font=("Arial", 18, "bold")).pack(pady=10)

# ================= إدخال بيانات =================
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="الاسم").grid(row=0, column=0)
name = tk.Entry(frame)
name.grid(row=0, column=1)

tk.Label(frame, text="المنصب").grid(row=0, column=2)
position = ttk.Combobox(frame, values=[
    "رئيس الجامعة",
    "عميد كلية",
    "مساعد رئيس الجامعة"
])
position.grid(row=0, column=3)

tk.Label(frame, text="الدرجة").grid(row=1, column=0)
grade = tk.Entry(frame)
grade.grid(row=1, column=1)

tk.Label(frame, text="المرحلة").grid(row=1, column=2)
stage = tk.Entry(frame)
stage.grid(row=1, column=3)

tk.Label(frame, text="آخر علاوة").grid(row=2, column=0)
last_date = DateEntry(frame, date_pattern="yyyy-mm-dd")
last_date.grid(row=2, column=1)

# ================= وظائف =================

def save_emp():
    if name.get() == "":
        messagebox.showerror("خطأ", "اسم الموظف فارغ")
        return

    data = (
        name.get(),
        position.get(),
        "تدريسي",
        grade.get(),
        stage.get(),
        last_date.get()
    )

    add_employee(data)
    load()
    messagebox.showinfo("تم", "تم إضافة الموظف")

def load():
    for i in tree.get_children():
        tree.delete(i)

    for row in get_employees():
        tree.insert("", "end", values=row)

def delete_emp():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("تنبيه", "اختر موظف للحذف")
        return

    emp = tree.item(selected[0])["values"]
    emp_id = emp[0]

    conn = sqlite3.connect("system.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()

    load()
    messagebox.showinfo("تم", "تم حذف الموظف")

def search_emp():
    keyword = search_entry.get()

    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect("system.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + keyword + '%',))
    rows = cur.fetchall()

    conn.close()

    for r in rows:
        tree.insert("", "end", values=r)

# ================= أزرار التحكم =================
control = tk.Frame(root)
control.pack(pady=10)

search_entry = tk.Entry(control)
search_entry.pack(side="left")

tk.Button(control, text="بحث", command=search_emp).pack(side="left", padx=5)
tk.Button(control, text="عرض الكل", command=load).pack(side="left", padx=5)
tk.Button(control, text="حذف موظف", command=delete_emp).pack(side="left", padx=5)
tk.Button(control, text="حفظ موظف", command=save_emp, bg="green", fg="white").pack(side="left", padx=5)

# ================= جدول =================
tree = ttk.Treeview(root, columns=("id","name","position","type","grade","stage","date"), show="headings")

for col in tree["columns"]:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)

load()

root.mainloop()
