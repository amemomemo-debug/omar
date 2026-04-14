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
root.geometry("1100x700")

selected_emp_id = None

# ================= TITLE =================
tk.Label(root, text="نظام شؤون الموظفين", font=("Arial", 18, "bold")).pack(pady=10)

# ================= EMPLOYEE FRAME =================
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


# ================= FUNCTIONS =================
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


def select_emp(event):
    global selected_emp_id
    selected = tree.selection()
    if selected:
        emp = tree.item(selected[0])["values"]
        selected_emp_id = emp[0]


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

    letters = get_letters(selected_emp_id)

    if len(letters) > 3:
        messagebox.showinfo("تنبيه", "تم الحفظ لكن الكتاب غير محسوب (تجاوز 3 كتب)")
    else:
        messagebox.showinfo("تم", "تم إضافة كتاب شكر")


# ================= BUTTONS =================
tk.Button(root, text="حفظ موظف", command=save_emp, bg="green", fg="white").pack(pady=5)

# ================= TABLE =================
tree = ttk.Treeview(root, columns=("id","name","position","type","grade","stage","date"), show="headings")

for col in tree["columns"]:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)
tree.bind("<ButtonRelease-1>", select_emp)

load()


# ================= LETTERS =================
letter_frame = tk.Frame(root)
letter_frame.pack(pady=10)

tk.Label(letter_frame, text="رقم الكتاب").grid(row=0, column=0)
letter_number = tk.Entry(letter_frame)
letter_number.grid(row=0, column=1)

tk.Label(letter_frame, text="الجهة").grid(row=0, column=2)
authority = ttk.Combobox(letter_frame, values=[
    "رئيس الجمهورية",
    "رئيس الوزراء",
    "الوزير",
    "رئيس الجامعة"
])
authority.grid(row=0, column=3)

tk.Label(letter_frame, text="التاريخ").grid(row=1, column=0)
letter_date = DateEntry(letter_frame, date_pattern="yyyy-mm-dd")
letter_date.grid(row=1, column=1)

tk.Button(letter_frame, text="إضافة كتاب شكر", command=add_letter_ui).grid(row=2, column=1)

root.mainloop()
