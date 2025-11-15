import tkinter as tk
from tkinter import messagebox
import random


# Defining the functions


def displayMenu():
    """Display difficulty menu"""
    clear_window()
    title_label.config(text="DIFFICULTY LEVEL")

    for widget in button_frame.winfo_children():
        widget.destroy()

    tk.Button(button_frame, text="1. Easy (1-digit)", width=20, command=lambda: start_quiz('easy')).pack(pady=5)
    tk.Button(button_frame, text="2. Moderate (2-digit)", width=20, command=lambda: start_quiz('moderate')).pack(pady=5)
    tk.Button(button_frame, text="3. Advanced (4-digit)", width=20, command=lambda: start_quiz('advanced')).pack(pady=5)


def randomInt(level):
    """Return a random integer based on difficulty level"""
    if level == 'easy':
        return random.randint(1, 9)
    elif level == 'moderate':
        return random.randint(10, 99)
    elif level == 'advanced':
        return random.randint(1000, 9999)


def decideOperation():
    """Randomly return '+' or '-'"""
    return random.choice(['+', '-'])


def displayProblem():
    """Display the current problem to the user"""
    global num1, num2, operation, attempts
    clear_window()

    # Reseting the attempt counter
    attempts = 0

    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    title_label.config(text=f"Question {question_count + 1}/10")

    question_label.config(text=f"{num1} {operation} {num2} = ")
    question_label.pack(pady=10)

    answer_entry.pack(pady=5)
    answer_entry.delete(0, tk.END)
    answer_entry.focus()

    submit_btn.pack(pady=10)


def isCorrect(user_answer):
    """Check if user's answer is correct and update score"""
    global score, question_count, attempts

    try:
        user_answer = int(user_answer)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    correct_answer = num1 + num2 if operation == '+' else num1 - num2

    if user_answer == correct_answer:
        if attempts == 0:
            score += 10
            messagebox.showinfo("Correct!", "✅ Correct! +10 points.")
        else:
            score += 5
            messagebox.showinfo("Correct!", "✅ Correct on second try! +5 points.")
        question_count += 1
        if question_count < 10:
            displayProblem()
        else:
            displayResults()
    else:
        if attempts == 0:
            attempts += 1
            messagebox.showwarning("Try Again", "❌ Wrong answer. Try again!")
        else:
            messagebox.showinfo("Incorrect", f"Wrong again! The correct answer was {correct_answer}.")
            question_count += 1
            if question_count < 10:
                displayProblem()
            else:
                displayResults()


def displayResults():
    """Display the user's final results"""
    clear_window()
    title_label.config(text="QUIZ COMPLETE 🎉")

    result_text = f"Your Final Score: {score}/100\n"
    if score >= 90:
        grade = "A+"
    elif score >= 75:
        grade = "A"
    elif score >= 60:
        grade = "B"
    elif score >= 45:
        grade = "C"
    else:
        grade = "F"

    result_label.config(text=result_text + f"Your Grade: {grade}")
    result_label.pack(pady=20)

    for widget in button_frame.winfo_children():
        widget.destroy()

    tk.Button(button_frame, text="Play Again", width=15, command=displayMenu).pack(pady=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.destroy).pack(pady=5)


def submitAnswer():
    """Handle submit button click"""
    answer = answer_entry.get()
    isCorrect(answer)


def clear_window():
    """Helper function to clear question/result area"""
    question_label.pack_forget()
    result_label.pack_forget()
    answer_entry.pack_forget()
    submit_btn.pack_forget()


def start_quiz(level):
    """Initialize quiz variables and start"""
    global difficulty, score, question_count
    difficulty = level
    score = 0
    question_count = 0
    displayProblem()



# SETUP OF MAIN GUI 


root = tk.Tk()
root.title("🧮 Arithmetic Quiz Game")
root.geometry("600x400")
root.resizable(False, False)

# Background image window
try:
    bg_image = tk.PhotoImage(file="2.png")  
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)
except:
    background_label = tk.Label(root, bg="#f1faee")
    background_label.place(relwidth=1, relheight=1)

title_label = tk.Label(root, text="ARITHMETIC QUIZ GAME", font=("Arial", 20, "bold"), bg="#f1faee", fg="#1d3557")
title_label.pack(pady=20)

# The Frames and Widgets 
question_label = tk.Label(root, font=("Arial", 16, "bold"), bg="#f1faee")
result_label = tk.Label(root, font=("Arial", 16), bg="#f1faee")

answer_entry = tk.Entry(root, width=10, font=("Arial", 16))
submit_btn = tk.Button(root, text="Submit", width=10, bg="#457b9d", fg="white", command=submitAnswer)

button_frame = tk.Frame(root, bg="#f1faee")
button_frame.pack(pady=20)

displayMenu()

root.mainloop()
