import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import *
from employees import *
from letters import *

root = tk.Tk()
root.title("نظام إدارة العلاوات والترفيعات")
root.geometry("1100x650")

FONT = ("Tahoma", 11)

# -------------------------
# إدخال بيانات الموظف
# -------------------------

frame = tk.LabelFrame(root, text="معلومات الموظف", font=("Tahoma", 12))
frame.pack(fill="x", padx=10, pady=10)

tk.Label(frame, text="الاسم", font=FONT).grid(row=0, column=0)
name_entry = tk.Entry(frame, font=FONT)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="المنصب", font=FONT).grid(row=0, column=2)

position_combo = ttk.Combobox(frame,font=FONT)
position_combo['values'] = [
"رئيس الجامعة",
"مساعد رئيس الجامعة للشؤون الادارية",
"مساعد رئيس الجامعة للشؤون العلمية",
"عميد كلية"
]
position_combo.grid(row=0,column=3)

tk.Label(frame,text="التشكيل",font=FONT).grid(row=1,column=0)
dept_entry = tk.Entry(frame,font=FONT)
dept_entry.grid(row=1,column=1)

tk.Label(frame,text="الدرجة الوظيفية",font=FONT).grid(row=1,column=2)
grade_entry = tk.Entry(frame,font=FONT)
grade_entry.grid(row=1,column=3)

tk.Label(frame,text="المرحلة",font=FONT).grid(row=2,column=0)
stage_entry = tk.Entry(frame,font=FONT)
stage_entry.grid(row=2,column=1)

tk.Label(frame,text="نوع العلاوة",font=FONT).grid(row=2,column=2)

allowance_combo = ttk.Combobox(frame,font=FONT)
allowance_combo['values'] = [
"علاوة تدريسي",
"علاوة خاصة"
]
allowance_combo.grid(row=2,column=3)

tk.Label(frame,text="تاريخ آخر علاوة",font=FONT).grid(row=3,column=0)
date_entry = DateEntry(frame,font=FONT,date_pattern="yyyy-mm-dd")
date_entry.grid(row=3,column=1)

# -------------------------
# جدول الموظفين
# -------------------------

table_frame = tk.Frame(root)
table_frame.pack(fill="both",expand=True)

columns = (
"الاسم",
"المنصب",
"التشكيل",
"الدرجة",
"المرحلة",
"نوع العلاوة",
"آخر علاوة",
"العلاوة القادمة",
"الترفيع"
)

tree = ttk.Treeview(table_frame,columns=columns,show="headings")

for col in columns:
    tree.heading(col,text=col)
    tree.column(col,width=120)

tree.pack(fill="both",expand=True)

# -------------------------
# جدول كتب الشكر المحتسبة
# -------------------------

counted_frame = tk.LabelFrame(root,text="كتب الشكر المحتسبة",font=("Tahoma",12))
counted_frame.pack(fill="x",padx=10,pady=5)

columns_letters_counted = (
"رقم الكتاب",
"تاريخ الكتاب",
"جهة الإصدار",
"القدم المحتسب"
)

letters_counted = ttk.Treeview(counted_frame,columns=columns_letters_counted,show="headings")

for col in columns_letters_counted:
    letters_counted.heading(col,text=col)
    letters_counted.column(col,width=150)

letters_counted.pack(fill="x")

# -------------------------
# جدول كتب الشكر غير المحتسبة
# -------------------------

not_counted_frame = tk.LabelFrame(root,text="كتب الشكر غير المحتسبة",font=("Tahoma",12))
not_counted_frame.pack(fill="x",padx=10,pady=5)

columns_letters_not = (
"رقم الكتاب",
"تاريخ الكتاب",
"جهة الإصدار",
"سبب عدم الاحتساب"
)

letters_not = ttk.Treeview(not_counted_frame,columns=columns_letters_not,show="headings")

for col in columns_letters_not:
    letters_not.heading(col,text=col)
    letters_not.column(col,width=150)

letters_not.pack(fill="x")

# -------------------------
# إضافة موظف
# -------------------------

def add_employee():

    name = name_entry.get()
    position = position_combo.get()
    dept = dept_entry.get()
    grade = grade_entry.get()
    stage = stage_entry.get()
    allowance = allowance_combo.get()
    date = date_entry.get()

    if name == "":
        messagebox.showerror("خطأ","الرجاء إدخال اسم الموظف")
        return

    save_employee(name,position,dept,grade,stage,allowance,date)

    messagebox.showinfo("تم","تم حفظ الموظف")

# -------------------------
# أزرار التحكم
# -------------------------

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

tk.Button(
buttons_frame,
text="إضافة موظف",
font=("Tahoma",11),
command=add_employee
).grid(row=0,column=0,padx=5)

tk.Button(
buttons_frame,
text="حذف موظف",
font=("Tahoma",11)
).grid(row=0,column=1,padx=5)

tk.Button(
buttons_frame,
text="تعديل بيانات",
font=("Tahoma",11)
).grid(row=0,column=2,padx=5)

tk.Button(
buttons_frame,
text="بحث عن موظف",
font=("Tahoma",11)
).grid(row=0,column=3,padx=5)

tk.Button(
buttons_frame,
text="تصدير إلى Excel",
font=("Tahoma",11)
).grid(row=0,column=4,padx=5)

# -------------------------
# الحقوق
# -------------------------

footer = tk.Label(
root,
text="Developed by: Omar_Basim_AL_RAWE",
font=("Arial",8),
fg="gray"
)

footer.pack(side="bottom")

root.mainloop()
