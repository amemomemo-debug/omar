import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

from db import init_db
from employees import add_employee, get_employees
from letters import add_letter, get_letters

init_db()

root = tk.Tk()
root.title("نظام شؤون الموظفين")
root.geometry("1250x780")

selected_emp_id = None

# ================= TITLE =================
tk.Label(root, text="نظام شؤون الموظفين", font=("Arial", 18, "bold")).pack(pady=10)

# ================= EMPLOYEE INPUT =================
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="الاسم").grid(row=0, column=0)
name = tk.Entry(frame)
name.grid(row=0, column=1)

tk.Label(frame, text="المنصب").grid(row=0, column=2)
position = ttk.Combobox(frame, values=[
    "رئيس الجامعة",
    "الوزير",
    "رئيس الوزراء",
    "رئيس الجمهورية",
    "عميد كلية"
])
position.grid(row=0, column=3)

# 🟢 الجديد: نوع التعيين
tk.Label(frame, text="نوع التعيين").grid(row=0, column=4)
job_type = ttk.Combobox(frame, values=[
    "تدريسي",
    "درجة خاصة"
])
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

# ================= SAVE EMP =================
def save_emp():
    if name.get() == "":
        messagebox.showerror("خطأ", "اسم الموظف فارغ")
        return

    data = (
        name.get(),
        position.get(),
        job_type.get(),   # 🟢 الجديد
        grade.get(),
        stage.get(),
        last_date.get()
    )

    add_employee(data)
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
    global selected_emp_id
    selected = emp_tree.selection()
    if selected:
        emp = emp_tree.item(selected[0])["values"]
        selected_emp_id = emp[0]
        load_letters()

# ================= ADD LETTER =================
def add_letter_ui():
    if not selected_emp_id:
        messagebox.showwarning("تنبيه", "اختر موظف أولاً")
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

# ================= EMP TABLE =================
emp_tree = ttk.Treeview(root, columns=("id","name","position","type","grade","stage","date"), show="headings")

for c in emp_tree["columns"]:
    emp_tree.heading(c, text=c)

emp_tree.pack(fill="x")
emp_tree.bind("<ButtonRelease-1>", select_emp)

load_emps()

# ================= LETTER INPUT =================
letter_frame = tk.Frame(root)
letter_frame.pack(pady=10)

tk.Label(letter_frame, text="رقم الكتاب").grid(row=0, column=0)
letter_number = tk.Entry(letter_frame)
letter_number.grid(row=0, column=1)

tk.Label(letter_frame, text="الجهة").grid(row=0, column=2)
authority = ttk.Combobox(letter_frame, values=[
    "رئيس الجامعة",
    "الوزير",
    "رئيس الوزراء",
    "رئيس الجمهورية"
])
authority.grid(row=0, column=3)

tk.Label(letter_frame, text="التاريخ").grid(row=0, column=4)
letter_date = DateEntry(letter_frame, date_pattern="yyyy-mm-dd")
letter_date.grid(row=0, column=5)

tk.Button(letter_frame, text="إضافة كتاب", command=add_letter_ui, bg="green", fg="white").grid(row=0, column=6)

# ================= LETTER TABLES =================
tables_frame = tk.Frame(root)
tables_frame.pack(fill="both", expand=True)

tk.Label(tables_frame, text="الكتب المحتسبة", font=("Arial", 12, "bold")).grid(row=0, column=0)
used_tree = ttk.Treeview(tables_frame, columns=("id","emp","num","auth","date"), show="headings", height=10)
for c in used_tree["columns"]:
    used_tree.heading(c, text=c)
used_tree.grid(row=1, column=0, padx=10)

tk.Label(tables_frame, text="الكتب غير المحتسبة", font=("Arial", 12, "bold")).grid(row=0, column=1)
unused_tree = ttk.Treeview(tables_frame, columns=("id","emp","num","auth","date"), show="headings", height=10)
for c in unused_tree["columns"]:
    unused_tree.heading(c, text=c)
unused_tree.grid(row=1, column=1, padx=10)

root.mainloop()
