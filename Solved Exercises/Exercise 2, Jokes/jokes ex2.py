import tkinter as tk
from tkinter import messagebox
import random


# Loading in jokes from an external text file 
def load_jokes(filename="31312.txt"):
    jokes = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup.strip() + "?", punchline.strip()))
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found!")
    return jokes



# Defining/creating functions to control buttons for actions on the GUI 


def show_setup():
    """Display a random joke's setup."""  #(Shows the question part of the joke)
    global current_joke
    if not jokes:
        messagebox.showerror("Error", "No jokes loaded!")
        return
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0], fg="#28aea8")
    punchline_label.config(text="")
    next_btn.config(state="normal")
    punchline_btn.config(state="normal")


def show_punchline(): #(Shows the punchline/the funny answer of the joke)
    """Reveal the punchline."""
    if current_joke:
        punchline_label.config(text=current_joke[1], fg="#e60e40", font=("Comic Sans MS", 14, "bold"))
        punchline_btn.config(state="disabled")


def next_joke(): #(When clicked shows the next joke picked randomly)
    """Get a new random joke."""
    show_setup()


def quit_app(): #(When clicked it closes the app)
    """Exit the app."""
    root.destroy()



#  Setup of the GUI 

root = tk.Tk()
root.title("😂 Alexa, Tell Me a Joke!")
root.geometry("500x400")
root.configure(bg="#fdfcdc")
root.resizable(False, False)

title_label = tk.Label(root, text="🎤 Alexa, Tell Me a Joke!", font=("Helvetica", 18, "bold"),
                       bg="#00b4d8", fg="#ffffff", width=35, pady=10)
title_label.pack(pady=10)

setup_label = tk.Label(root, text="", wraplength=400, justify="center",
                       font=("Comic Sans MS", 14, "italic"), bg="#fdfcdc")
setup_label.pack(pady=40)

punchline_label = tk.Label(root, text="", wraplength=400, justify="center",
                           font=("Comic Sans MS", 13), bg="#fdfcdc", fg="#d00000")
punchline_label.pack(pady=10)


# The Buttons


button_frame = tk.Frame(root, bg="#fdfcdc")
button_frame.pack(pady=20)

joke_btn = tk.Button(button_frame, text="🤣 Alexa tell me a Joke", bg="#00b4d8", fg="white",
                     font=("Helvetica", 13, "bold"), width=25, command=show_setup)
joke_btn.grid(row=0, column=0, padx=5, pady=5) 

punchline_btn = tk.Button(button_frame, text="😂 Show Punchline", bg="#ffd166", fg="#000",
                          font=("Helvetica", 13, "bold"), width=18, state="disabled", command=show_punchline)
punchline_btn.grid(row=1, column=0, padx=5, pady=5)

next_btn = tk.Button(button_frame, text="🔁 Next Joke", bg="#06d6a0", fg="#fff",
                     font=("Helvetica", 13, "bold"), width=15, state="disabled", command=next_joke)
next_btn.grid(row=2, column=0, padx=5, pady=5)

quit_btn = tk.Button(button_frame, text="🚪 Quit", bg="#ef476f", fg="#fff",
                     font=("Helvetica", 13, "bold"), width=10, command=quit_app)
quit_btn.grid(row=3, column=0, padx=5, pady=5)


# Initialzing the app 


jokes = load_jokes()
current_joke = None

root.mainloop()
