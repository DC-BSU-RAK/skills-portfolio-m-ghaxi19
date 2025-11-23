import tkinter as tk
from tkinter import messagebox, ttk


# Loading in the student data

def load_students(filename="data.txt"):
    students = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            num_students = int(lines[0].strip())

            for line in lines[1:]:
                data = line.strip().split(",")
                if len(data) != 6:
                    continue
                student_id = data[0]
                name = data[1]
                c1, c2, c3, exam = map(int, data[2:])
                coursework_total = c1 + c2 + c3
                overall = coursework_total + exam
                percent = (overall / 160) * 100

                if percent >= 70:
                    grade = "A"
                elif percent >= 60:
                    grade = "B"
                elif percent >= 50:
                    grade = "C"
                elif percent >= 40:
                    grade = "D"
                else:
                    grade = "F"

                students.append({
                    "id": student_id,
                    "name": name,
                    "coursework": coursework_total,
                    "exam": exam,
                    "overall": overall,
                    "percent": percent,
                    "grade": grade
                })

        return students, num_students
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found!")
        return [], 0
    except Exception as e:
        messagebox.showerror("Error", f"Could not load data: {e}")
        return [], 0



# Output Functions


def clear_output():
    output_text.config(state="normal")
    output_text.delete(1.0, tk.END)
    output_text.config(state="disabled")

def append_output(text):
    output_text.config(state="normal")
    output_text.insert(tk.END, text + "\n")
    output_text.config(state="disabled")

def view_all_records():
    clear_output()
    append_output("📘 ALL STUDENT RECORDS:\n")
    total_percent = 0

    for s in students:
        append_output(f"Name: {s['name']}")
        append_output(f"Student Number: {s['id']}")
        append_output(f"Coursework Total: {s['coursework']}/60")
        append_output(f"Exam Mark: {s['exam']}/100")
        append_output(f"Overall %: {s['percent']:.2f}%")
        append_output(f"Grade: {s['grade']}")
        append_output("-" * 40)
        total_percent += s["percent"]

    avg = total_percent / len(students) if students else 0
    append_output(f"\nTotal Students: {len(students)}")
    append_output(f"Average Percentage: {avg:.2f}%")

def view_individual_record():
    clear_output()
    query = student_entry.get().strip().lower()

    if not query:
        messagebox.showwarning("Input Required", "Enter a student name or number.")
        return

    found = False
    for s in students:
        if query == s['id'].lower() or query in s['name'].lower():
            found = True
            append_output(f"🎓 RECORD FOUND:\n")
            append_output(f"Name: {s['name']}")
            append_output(f"Student Number: {s['id']}")
            append_output(f"Coursework Total: {s['coursework']}/60")
            append_output(f"Exam Mark: {s['exam']}/100")
            append_output(f"Overall %: {s['percent']:.2f}%")
            append_output(f"Grade: {s['grade']}")
            append_output("-" * 40)

    if not found:
        append_output("❌ No student found with that name or number.")

def show_highest_score():
    clear_output()
    if not students:
        append_output("No data available.")
        return
    top_student = max(students, key=lambda s: s['overall'])
    append_output("🏆 STUDENT WITH HIGHEST SCORE:")
    append_output(f"Name: {top_student['name']}")
    append_output(f"Student Number: {top_student['id']}")
    append_output(f"Coursework Total: {top_student['coursework']}/60")
    append_output(f"Exam Mark: {top_student['exam']}/100")
    append_output(f"Overall %: {top_student['percent']:.2f}%")
    append_output(f"Grade: {top_student['grade']}")

def show_lowest_score():
    clear_output()
    if not students:
        append_output("No data available.")
        return
    bottom_student = min(students, key=lambda s: s['overall'])
    append_output("📉 STUDENT WITH LOWEST SCORE:")
    append_output(f"Name: {bottom_student['name']}")
    append_output(f"Student Number: {bottom_student['id']}")
    append_output(f"Coursework Total: {bottom_student['coursework']}/60")
    append_output(f"Exam Mark: {bottom_student['exam']}/100")
    append_output(f"Overall %: {bottom_student['percent']:.2f}%")
    append_output(f"Grade: {bottom_student['grade']}")



# Dark Theme 


root = tk.Tk()
root.title("📚 Student Management Database")
root.geometry("750x500")

# Dark Theme Colors
BG_WINDOW = "#121212"
BG_TITLE = "#1f1f1f"
BG_BUTTON = "#333333"
BG_BUTTON2 = "#444444"
BG_OUTPUT = "#1a1a1a"
TEXT_COLOR = "#00eaff"

root.configure(bg=BG_WINDOW)

# Title Bar
title_label = tk.Label(
    root,
    text="🎓 STUDENT MANAGEMENT DATABASE",
    font=("Helvetica", 18, "bold"),
    bg=BG_TITLE,
    fg="#00eaff",
    pady=10
)
title_label.pack(fill="x")

# Frame for the input and the buttons
menu_frame = tk.Frame(root, bg=BG_WINDOW)
menu_frame.pack(pady=10)

# Search Label And Entry
tk.Label(
    menu_frame,
    text="Search by Name or ID:",
    bg=BG_WINDOW,
    fg=TEXT_COLOR,
    font=("Helvetica", 12)
).grid(row=0, column=0, padx=5)

student_entry = tk.Entry(
    menu_frame,
    width=25,
    font=("Helvetica", 12),
    bg="#2c2c2c",
    fg="white",
    insertbackground="white"
)
student_entry.grid(row=0, column=1, padx=5)

# Template Of Button Style
btn_style = {
    "font": ("Helvetica", 12, "bold"),
    "width": 28,
    "pady": 5,
    "fg": "white"
}

# Buttons, dark theme
tk.Button(menu_frame, text="1️⃣  View All Student Records",
          bg=BG_BUTTON, command=view_all_records, **btn_style).grid(row=1, column=0, columnspan=2, pady=3)

tk.Button(menu_frame, text="2️⃣  View Individual Student Record",
          bg=BG_BUTTON2, command=view_individual_record, **btn_style).grid(row=2, column=0, columnspan=2, pady=3)

tk.Button(menu_frame, text="3️⃣  Show Highest Scorer",
          bg=BG_BUTTON, command=show_highest_score, **btn_style).grid(row=3, column=0, columnspan=2, pady=3)

tk.Button(menu_frame, text="4️⃣  Show Lowest Scorer",
          bg="#8b0000", command=show_lowest_score, **btn_style).grid(row=4, column=0, columnspan=2, pady=3)

tk.Button(menu_frame, text="🚪 Quit",
          bg="#005f73", command=root.destroy, **btn_style).grid(row=5, column=0, columnspan=2, pady=10)

# Output Textbox For Results 
output_text = tk.Text(
    root,
    wrap="word",
    font=("Courier New", 12),
    width=80,
    height=15,
    bg=BG_OUTPUT,
    fg=TEXT_COLOR,
    insertbackground="white",
    state="disabled"
)
output_text.pack(pady=10)

# Loading Student Data
students, num_students = load_students()

root.mainloop()
