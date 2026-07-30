"""
Rock-Paper-Scissors Game (GUI)
-------------------------------
A polished, user-friendly Rock-Paper-Scissors game built with Tkinter.

Features:
    - Click Rock, Paper, or Scissors to make your move
    - Computer picks randomly
    - A "battle box" shows your choice and the computer's choice
      face-to-face with large emoji, separated by a VS badge
    - The winning side's box lights up green; a tie lights both orange
    - Running score is tracked across rounds
    - "Play Again" is just picking your next move — no restart needed
    - "Reset Score" clears the scoreboard
"""

import tkinter as tk
import random

CHOICES = ["Rock", "Paper", "Scissors"]
EMOJI = {"Rock": "\U0001FAA8", "Paper": "\U0001F4C4", "Scissors": "\U00002702\uFE0F"}

# Rules: key beats value
BEATS = {
    "Rock": "Scissors",
    "Scissors": "Paper",
    "Paper": "Rock",
}

# Palette
BG = "#1e1e2f"
PANEL_BG = "#2a2a40"
ACCENT = "#00e5ff"
WIN_COLOR = "#00e676"
LOSE_COLOR = "#ff5252"
TIE_COLOR = "#ffb300"
NEUTRAL_BORDER = "#44445a"
TEXT_LIGHT = "#f5f5f5"

user_score = 0
computer_score = 0
ties = 0
round_number = 0


def set_box_state(frame, color):
    frame.config(highlightbackground=color, highlightcolor=color)


def play(user_choice):
    global user_score, computer_score, ties, round_number

    computer_choice = random.choice(CHOICES)
    round_number += 1

    if user_choice == computer_choice:
        outcome = "It's a Tie!"
        outcome_color = TIE_COLOR
        ties += 1
        set_box_state(you_box, TIE_COLOR)
        set_box_state(cpu_box, TIE_COLOR)
    elif BEATS[user_choice] == computer_choice:
        outcome = "YOU WIN! \U0001F389"
        outcome_color = WIN_COLOR
        user_score += 1
        set_box_state(you_box, WIN_COLOR)
        set_box_state(cpu_box, LOSE_COLOR)
    else:
        outcome = "YOU LOSE"
        outcome_color = LOSE_COLOR
        computer_score += 1
        set_box_state(you_box, LOSE_COLOR)
        set_box_state(cpu_box, WIN_COLOR)

    you_emoji.config(text=EMOJI[user_choice])
    you_name.config(text=user_choice)
    cpu_emoji.config(text=EMOJI[computer_choice])
    cpu_name.config(text=computer_choice)

    result_label.config(text=outcome, fg=outcome_color)
    update_scoreboard()


def update_scoreboard():
    score_label.config(
        text=f"ROUND {round_number}     YOU {user_score}  —  {computer_score} COMPUTER     (Ties: {ties})"
    )


def reset_score():
    global user_score, computer_score, ties, round_number
    user_score = 0
    computer_score = 0
    ties = 0
    round_number = 0
    update_scoreboard()

    you_emoji.config(text="\u2753")
    you_name.config(text="—")
    cpu_emoji.config(text="\u2753")
    cpu_name.config(text="—")
    set_box_state(you_box, NEUTRAL_BORDER)
    set_box_state(cpu_box, NEUTRAL_BORDER)
    result_label.config(text="Make your move to start!", fg=TEXT_LIGHT)


# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Rock - Paper - Scissors")
root.geometry("520x560")
root.resizable(False, False)
root.configure(bg=BG)

tk.Label(root, text="ROCK  \u2022  PAPER  \u2022  SCISSORS", font=("Arial", 20, "bold"), bg=BG, fg=ACCENT).pack(pady=(20, 4))
tk.Label(
    root,
    text="Rock beats Scissors  \u2022  Scissors beats Paper  \u2022  Paper beats Rock",
    font=("Arial", 9), bg=BG, fg="#aaaaaa"
).pack(pady=(0, 18))

# ---- Battle Box ----
battle_frame = tk.Frame(root, bg=BG)
battle_frame.pack(pady=5)

you_box = tk.Frame(
    battle_frame, bg=PANEL_BG, width=170, height=180,
    highlightthickness=4, highlightbackground=NEUTRAL_BORDER, highlightcolor=NEUTRAL_BORDER
)
you_box.pack_propagate(False)
you_box.grid(row=0, column=0, padx=10)

tk.Label(you_box, text="YOU", font=("Arial", 11, "bold"), bg=PANEL_BG, fg=ACCENT).pack(pady=(12, 0))
you_emoji = tk.Label(you_box, text="\u2753", font=("Arial", 48), bg=PANEL_BG, fg=TEXT_LIGHT)
you_emoji.pack(pady=6)
you_name = tk.Label(you_box, text="—", font=("Arial", 12, "bold"), bg=PANEL_BG, fg=TEXT_LIGHT)
you_name.pack(pady=(0, 10))

tk.Label(battle_frame, text="VS", font=("Arial", 18, "bold"), bg=BG, fg=ACCENT).grid(row=0, column=1, padx=8)

cpu_box = tk.Frame(
    battle_frame, bg=PANEL_BG, width=170, height=180,
    highlightthickness=4, highlightbackground=NEUTRAL_BORDER, highlightcolor=NEUTRAL_BORDER
)
cpu_box.pack_propagate(False)
cpu_box.grid(row=0, column=2, padx=10)

tk.Label(cpu_box, text="COMPUTER", font=("Arial", 11, "bold"), bg=PANEL_BG, fg=ACCENT).pack(pady=(12, 0))
cpu_emoji = tk.Label(cpu_box, text="\u2753", font=("Arial", 48), bg=PANEL_BG, fg=TEXT_LIGHT)
cpu_emoji.pack(pady=6)
cpu_name = tk.Label(cpu_box, text="—", font=("Arial", 12, "bold"), bg=PANEL_BG, fg=TEXT_LIGHT)
cpu_name.pack(pady=(0, 10))

# ---- Result ----
result_label = tk.Label(root, text="Make your move to start!", font=("Arial", 16, "bold"), bg=BG, fg=TEXT_LIGHT)
result_label.pack(pady=20)

# ---- Move buttons ----
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=5)

button_style = {
    "font": ("Arial", 13, "bold"), "width": 10, "height": 2,
    "bg": ACCENT, "fg": "#0a0a0a", "activebackground": "#33eaff",
    "relief": "flat", "bd": 0, "cursor": "hand2"
}

for choice in CHOICES:
    tk.Button(
        btn_frame, text=f"{EMOJI[choice]}\n{choice}",
        command=lambda c=choice: play(c), **button_style
    ).pack(side="left", padx=8)

# ---- Scoreboard ----
score_label = tk.Label(
    root, text="ROUND 0     YOU 0  —  0 COMPUTER     (Ties: 0)",
    font=("Arial", 11, "bold"), bg=BG, fg=TEXT_LIGHT
)
score_label.pack(pady=(28, 6))

tk.Button(
    root, text="Reset Score", command=reset_score, width=14,
    bg=PANEL_BG, fg=TEXT_LIGHT, relief="flat", activebackground="#3a3a55"
).pack(pady=6)

root.mainloop()