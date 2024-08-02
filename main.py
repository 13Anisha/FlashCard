import random
from tkinter import *
import pandas


score = 0
current_word = {}
words = []

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("flashcard_data.csv")
    words = original_data.to_dict(orient="records")
else:
    words = data.to_dict(orient="records")


# -------------------------------Exit--------------------------------------------------------------
def Exit_window():
    window.destroy()


# ---------------------Generating Words------------------------------------------------------------
def generate():
    global current_word, flip_timer, words
    window.after_cancel(flip_timer)

    current_word = random.choice(words)
    canvas.itemconfig(card_title, text="French", fill="black", font=("Arial", 40, "italic"))
    canvas.itemconfig(card_word, text=current_word['French'], fill="black", font=("Arial", 30, "bold"))
    canvas.itemconfig(background_image, image=bg_image)
    flip_timer = window.after(3000, func=flip_cards)


# --------------------------flip cards----------------------------------------------------------------
def flip_cards():
    global current_word
    canvas.itemconfig(card_title, text="English", fill="white", font=("Arial", 40, "italic"))
    canvas.itemconfig(card_word, text=current_word['English'], fill="white", font=("Arial", 30, "bold"))
    canvas.itemconfig(background_image, image=bg_image2)


# ------------------------------known words---------------------------------------------------------
def is_known():
    global current_word, score
    words.remove(current_word)
    info = pandas.DataFrame(words)
    info.to_csv("words_to_learn.csv", index=False)
    score += 1
    canvas.itemconfig(score_label, text=f"{score}/100")

    generate()


# ---------------------------UI Setup---------------------------------------------------------------
window = Tk()
window.title("Flash Cards")
window.config(padx=70, pady=10, bg="#B1DDC6")

canvas = Canvas(width=750, height=500, bg="#B1DDC6", highlightthickness=0)

bg_image = PhotoImage(file="card_front.png")
background_image = canvas.create_image(400, 268, image=bg_image)
bg_image2 = PhotoImage(file="card_back.png")
card_title = canvas.create_text(400, 150, text="", font=("Arial", 20, "italic"))
card_word = canvas.create_text(400, 250, text="", font=("Arial", 40, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

score_label = canvas.create_text(680, 60, text=f"{score}/100", fill="blue", font=("Arial", 24, "bold"))

tick_image = PhotoImage(file="right.png")
right_button = Button(image=tick_image, highlightthickness=0, command=is_known, height=86, bg="#B1DDC6")
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate, height=86, bg="#B1DDC6")
wrong_button.grid(row=1, column=0)

exit_button = Button(text="Exit", width=10, height=2, highlightthickness=0, command=Exit_window,
                     font=("Arial", 12, "bold"))
exit_button.grid(row=1, column=2)

flip_timer = window.after(3000, func=flip_cards)

generate()

window.mainloop()
