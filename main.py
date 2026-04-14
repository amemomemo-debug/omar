import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from db import init_db
from employees import add_employee, get_employees

init_db()

root = tk.Tk()
root.title("نظام شؤون الموظفين")
root.geometry("1000x600")

# ================= عنوان =================
tk.Label(root, text="نظام شؤون الموظفين", font=("Arial", 18, "bold")).pack(pady=10)

# ================= إدخال =================
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

# ================= حفظ =================
def save():
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

# ================= تحميل =================
def load():
    for i in tree.get_children():
        tree.delete(i)

    for row in get_employees():
        tree.insert("", "end", values=row)

tk.Button(root, text="حفظ الموظف", command=save, bg="green", fg="white").pack(pady=10)

# ================= جدول =================
tree = ttk.Treeview(root, columns=("id","name","position","type","grade","stage","date"), show="headings")

for col in tree["columns"]:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)

load()

root.mainloop()
