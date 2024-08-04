import tkinter as tk
from tkinter import messagebox
import random
import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('rps_game.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    user_score INTEGER,
                    computer_score INTEGER)''')
conn.commit()

def get_scores():
    cursor.execute("SELECT user_score, computer_score FROM scores WHERE id=1")
    row = cursor.fetchone()
    if row:
        return row
    else:
        cursor.execute("INSERT INTO scores (user_score, computer_score) VALUES (0, 0)")
        conn.commit()
        return (0, 0)

def update_scores(user_score, computer_score):
    cursor.execute("UPDATE scores SET user_score=?, computer_score=? WHERE id=1", (user_score, computer_score))
    conn.commit()

# Initialize scores
user_score, computer_score = get_scores()

# Game logic
def determine_winner(user_choice):
    global user_score, computer_score
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        result = "You win!"
        user_score += 1
        messagebox.showinfo("Result", result)
    else:
        result = "You lose!"
        computer_score += 1
        messagebox.showinfo("Result", result)

    update_scores(user_score, computer_score)

    result_label.config(text=f"Your choice: {user_choice}\nComputer's choice: {computer_choice}\n{result}")
    score_label.config(text=f"User: {user_score} | Computer: {computer_score}")

# User Interface
root = tk.Tk()
root.title("Rock-Paper-Scissors")

# Widgets
font_style = ("Helvetica", 16)

instruction_label = tk.Label(root, text="Choose Rock, Paper, or Scissors:", font=font_style)
instruction_label.pack(pady=20, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(expand=True)

rock_button = tk.Button(button_frame, text="Rock", bg="light pink", font=font_style, command=lambda: determine_winner('rock'))
rock_button.grid(row=0, column=0, padx=20, pady=20)

paper_button = tk.Button(button_frame, text="Paper", bg="light blue", font=font_style, command=lambda: determine_winner('paper'))
paper_button.grid(row=0, column=1, padx=20, pady=20)

scissors_button = tk.Button(button_frame, text="Scissors", bg="orange", font=font_style, command=lambda: determine_winner('scissors'))
scissors_button.grid(row=0, column=2, padx=20, pady=20)

result_label = tk.Label(root, text="Make your choice to start the game!", font=font_style)
result_label.pack(pady=20, expand=True)

score_label = tk.Label(root, text=f"User: {user_score} | Computer: {computer_score}", font=font_style)
score_label.pack(pady=20, expand=True)

def play_again():
    result_label.config(text="Make your choice to start the game!")
    score_label.config(text=f"User: {user_score} | Computer: {computer_score}")

play_again_button = tk.Button(root, text="Play Again", font=font_style, command=play_again)
play_again_button.pack(pady=20, expand=True)

# Center the window on the screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Start the Tkinter event loop
root.mainloop()

# Close the SQLite connection when done
conn.close()