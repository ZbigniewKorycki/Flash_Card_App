from tkinter import *
from tkinter import messagebox
import random
import os
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

# TIME IN MILLISECOND
TIME_TO_GUESS = 5000

CURRENT_CARD = None

if os.path.isfile("./data/words_to_learn.csv"):
    words_learn = pd.read_csv("./data/words_to_learn.csv")
    words_dict = words_learn.to_dict(orient="records")
else:
    words_base = pd.read_csv("data/words.csv")
    words_dict = words_base.to_dict(orient="records")


def next_card():
    global CURRENT_CARD, flips
    window.after_cancel(flips)
    CURRENT_CARD = random.choice(words_dict)
    canvas.itemconfig(image, image=front_image)
    canvas.itemconfig(word, text=CURRENT_CARD["English"], fill="black")
    canvas.itemconfig(language, text="ENGLISH", fill="black")
    flips = window.after(TIME_TO_GUESS, flip_card)


def flip_card():
    canvas.itemconfig(image, image=back_image)
    canvas.itemconfig(
        language,
        text="JĘZYK POLSKI",
        fill="white",
    )
    canvas.itemconfig(word, text=CURRENT_CARD["Polish"], fill="white")


def remove_word():
    try:
        words_learn = pd.read_csv("./data/words_to_learn.csv")
        words_to_learn = words_learn.to_dict(orient="records")

    except FileNotFoundError:
        words_base = pd.read_csv("data/words.csv")
        words_to_learn = words_base.to_dict(orient="records")

    words_to_learn.remove(CURRENT_CARD)
    new_words = pd.DataFrame(words_to_learn)
    new_words.to_csv("./data/words_to_learn.csv", index=False)
    if len(words_to_learn) == 0:
        messagebox.showinfo(
            title="Congratulation!", message=f"Congratulation! You know everything!"
        )
    else:
        next_card()


window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flips = window.after(TIME_TO_GUESS, flip_card)

canvas = Canvas(
    width=800, height=526, bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR
)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
image = canvas.create_image(400, 263, image=front_image)
language = canvas.create_text(
    400, 150, text="", font=("Ariel", 40, "italic"), fill="black"
)
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="black")
canvas.grid(column=0, columnspan=2, row=0)

# Labels

known_label = Label(
    text="I know it", font=("Ariel", 20, "bold"), bg=BACKGROUND_COLOR, fg="black"
)
known_label.grid(column=1, row=1)

next_label = Label(
    text="Next", font=("Ariel", 20, "bold"), bg=BACKGROUND_COLOR, fg="black"
)
next_label.grid(column=0, row=1)


# Buttons

true_button_image = PhotoImage(file="./images/right.png")
true_button = Button(
    image=true_button_image,
    highlightthickness=0,
    highlightbackground=BACKGROUND_COLOR,
    command=remove_word,
)
true_button.grid(column=1, row=2)


wrong_button_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(
    image=wrong_button_image,
    highlightthickness=0,
    highlightbackground=BACKGROUND_COLOR,
    command=next_card,
)
wrong_button.grid(column=0, row=2)


next_card()

window.mainloop()
