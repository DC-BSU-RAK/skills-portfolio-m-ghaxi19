import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os


# Loading in the student data

FILENAME = "data.txt"

def load_students():
    students = []
    if not os.path.exists(FILENAME):
        messagebox.showerror("Error", f"{FILENAME} not found!")
        return students
    
    with open(FILENAME, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 6:
                sid, name, c1, c2, c3, exam = parts
                students.append({
                    "id": sid,
                    "name": name,
                    "c1": int(c1),
                    "c2": int(c2),
                    "c3": int(c3),
                    "exam": int(exam)
                })
    return students

def save_students(students):
    with open(FILENAME, "w") as file:
        file.write(f"{len(students)}\n")
        for s in students:
            file.write(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")


# Functions for different calculations 

def total_coursework(s): 
    return s["c1"] + s["c2"] + s["c3"]

def total_marks(s): 
    return total_coursework(s) + s["exam"]

def percentage(s): 
    return round(total_marks(s) / 160 * 100, 1)

def grade(s):
    pct = percentage(s)
    if pct >= 70: return "A"
    elif pct >= 60: return "B"
    elif pct >= 50: return "C"
    elif pct >= 40: return "D"
    else: return "F"


# Functions for display, Output fucntions 

def clear_text():
    output.config(state="normal")
    output.delete(1.0, tk.END)
    output.config(state="disabled")

def show_all():
    clear_text()
    students = load_students()
    total_pct = 0
    for s in students:
        info = f"""
Name: {s['name']}
ID: {s['id']}
Coursework Total: {total_coursework(s)}/60
Exam Mark: {s['exam']}/100
Percentage: {percentage(s)}%
Grade: {grade(s)}
--------------------------------------"""
        output.config(state="normal")
        output.insert(tk.END, info)
        output.config(state="disabled")
        total_pct += percentage(s)
    if students:
        avg = round(total_pct / len(students), 1)
        output.config(state="normal")
        output.insert(tk.END, f"\nTotal Students: {len(students)}\nAverage Percentage: {avg}%")
        output.config(state="disabled")

def show_individual():
    students = load_students()
    code = simpledialog.askstring("Search Student", "Enter Student ID or Name:")
    found = False
    clear_text()
    for s in students:
        if s["id"] == code or s["name"].lower() == code.lower():
            found = True
            info = f"""
Name: {s['name']}
ID: {s['id']}
Coursework Total: {total_coursework(s)}/60
Exam Mark: {s['exam']}/100
Percentage: {percentage(s)}%
Grade: {grade(s)}"""
            output.config(state="normal")
            output.insert(tk.END, info)
            output.config(state="disabled")
    if not found:
        messagebox.showinfo("Not Found", "Student not found!")

def show_highest():
    students = load_students()
    if not students: return
    top = max(students, key=total_marks)
    clear_text()
    output.config(state="normal")
    output.insert(tk.END, f"Highest Scorer:\n\nName: {top['name']}\nID: {top['id']}\nTotal: {total_marks(top)}/160\nPercentage: {percentage(top)}%\nGrade: {grade(top)}")
    output.config(state="disabled")

def show_lowest():
    students = load_students()
    if not students: return
    low = min(students, key=total_marks)
    clear_text()
    output.config(state="normal")
    output.insert(tk.END, f"Lowest Scorer:\n\nName: {low['name']}\nID: {low['id']}\nTotal: {total_marks(low)}/160\nPercentage: {percentage(low)}%\nGrade: {grade(low)}")
    output.config(state="disabled")


# Extended Task Features, Sorting, Adding new student, Deleting Student, Updating existing student

def sort_records():
    students = load_students()
    if not students: return
    choice = messagebox.askquestion("Sort", "Sort in Ascending order?")
    reverse = False if choice == "yes" else True
    students.sort(key=total_marks, reverse=reverse)
    clear_text()
    for s in students:
        output.config(state="normal")
        output.insert(tk.END, f"{s['name']} ({s['id']}) - {percentage(s)}%\n")
        output.config(state="disabled")

def add_student():
    students = load_students()
    sid = simpledialog.askstring("Add Student", "Enter Student ID:")
    name = simpledialog.askstring("Add Student", "Enter Student Name:")
    c1 = int(simpledialog.askstring("Add Student", "Coursework 1 (out of 20):"))
    c2 = int(simpledialog.askstring("Add Student", "Coursework 2 (out of 20):"))
    c3 = int(simpledialog.askstring("Add Student", "Coursework 3 (out of 20):"))
    exam = int(simpledialog.askstring("Add Student", "Exam Mark (out of 100):"))
    students.append({"id": sid, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam})
    save_students(students)
    messagebox.showinfo("Success", f"{name} added successfully!")

def delete_student():
    students = load_students()
    code = simpledialog.askstring("Delete Student", "Enter Student ID or Name to Delete:")
    new_list = [s for s in students if not (s["id"] == code or s["name"].lower() == code.lower())]
    if len(new_list) != len(students):
        save_students(new_list)
        messagebox.showinfo("Deleted", "Student record deleted!")
    else:
        messagebox.showinfo("Not Found", "No matching record found!")

def update_student():
    students = load_students()
    code = simpledialog.askstring("Update Student", "Enter Student ID or Name to Update:")
    for s in students:
        if s["id"] == code or s["name"].lower() == code.lower():
            field = simpledialog.askstring("Update", "Enter field to update (name/c1/c2/c3/exam):")
            if field in s:
                new_value = simpledialog.askstring("Update", f"Enter new value for {field}:")
                s[field] = int(new_value) if field != "name" else new_value
                save_students(students)
                messagebox.showinfo("Success", f"{s['name']}'s record updated!")
                return
    messagebox.showinfo("Not Found", "Student not found!")


# Dark Theme 

root = tk.Tk()
root.title("🎓 Student Management Database")
root.geometry("750x650")

# Dark Theme Colors
BG_WINDOW = "#121212"
BG_TITLE = "#1f1f1f"
BG_BUTTON = "#333333"
BG_BUTTON2 = "#444444"
BG_OUTPUT = "#1a1a1a"
TEXT_COLOR = "#00eaff"

root.configure(bg=BG_WINDOW)

title = tk.Label(
    root,
    text="📚 STUDENT MANAGEMENT DATABASE",
    font=("Helvetica", 20, "bold"),
    bg=BG_TITLE,
    fg=TEXT_COLOR,
    pady=12
)
title.pack(fill="x")

frame = tk.Frame(root, bg=BG_WINDOW)
frame.pack(pady=10)

btn_style = {
    "font": ("Helvetica", 12, "bold"),
    "width": 28,
    "pady": 5,
    "fg": "white"
}

buttons = [
    ("1️⃣  View All Records", show_all),
    ("2️⃣  View Individual Record", show_individual),
    ("3️⃣  Show Highest Score", show_highest),
    ("4️⃣  Show Lowest Score", show_lowest),
    ("5️⃣  Sort Records", sort_records),
    ("6️⃣  Add Student", add_student),
    ("7️⃣  Delete Student", delete_student),
    ("8️⃣  Update Student", update_student)
]

for i, (text, cmd) in enumerate(buttons):
    color = BG_BUTTON if i % 2 == 0 else BG_BUTTON2
    tk.Button(frame, text=text, command=cmd, bg=color, **btn_style).pack(pady=4)

output = tk.Text(
    root,
    height=15,
    width=80,
    bg=BG_OUTPUT,
    fg=TEXT_COLOR,
    font=("Courier New", 12),
    state="disabled",
    insertbackground="white"
)
output.pack(pady=10)

quit_btn = tk.Button(
    root,
    text="🚪 Exit",
    command=root.destroy,
    font=("Helvetica", 12, "bold"),
    bg="#8b0000",
    fg="white",
    width=20,
    pady=5
)
quit_btn.pack(pady=10)

root.mainloop()
