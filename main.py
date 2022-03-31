from tkinter import *
import pandas
import random

KNOWN_WORDS_SAVED_PATH = "./data/words_to_learn.csv"
NEW_WORDS_PATH = "./data/french_words.csv"
BACKGROUND_COLOR = "#B1DDC6"
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 536
LANGUAGE_LABEL_FONT = ("Arial", 40, "italic")
WORD_LABEL_FONT = ("Arial", 60, "bold")

# ---------------------------- Get Word DataFrame ------------------------------- #
try:
    word_df = pandas.read_csv(KNOWN_WORDS_SAVED_PATH)
except FileNotFoundError:
    word_df = pandas.read_csv(NEW_WORDS_PATH)

words_unknown = word_df.to_dict(orient="records")
current_word_pair = {}


def get_random_word_pair():
    return random.choice(words_unknown)


def set_state_english():
    global current_word_pair
    canvas.itemconfig(current_canvas, image=card_back_img)
    canvas.itemconfig(current_language, text="English", fill="white")
    canvas.itemconfig(current_word, text=f"{current_word_pair['English']}", fill="white")


def set_state_french_and_reset():
    global current_word_pair, state_switch_timer
    current_word_pair = get_random_word_pair()
    window.after_cancel(state_switch_timer)
    canvas.itemconfig(current_canvas, image=card_front_img)
    canvas.itemconfig(current_language, text="French", fill="black")
    canvas.itemconfig(current_word, text=f"{current_word_pair['French']}", fill="black")
    state_switch_timer = window.after(3000, func=set_state_english)


# ---------------------------- Set Word DataFrame ------------------------------- #
def remove_known_word():
    words_unknown.remove(current_word_pair)
    set_state_french_and_reset()
    words_to_learn = pandas.DataFrame(words_unknown)
    words_to_learn.to_csv("./data/words_to_learn.csv", index=False)


# ---------------------------- Window ------------------------------- #
window = Tk()
window.title("Learn French Demo")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

state_switch_timer = window.after(3000, func=set_state_english)

# ---------------------------- Canvas ------------------------------- #
canvas_center_x = int(CANVAS_WIDTH / 2)
canvas_center_y = int(CANVAS_HEIGHT / 2)

card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
current_canvas = canvas.create_image(canvas_center_x, canvas_center_y, image=card_front_img)


canvas.grid(column=0, row=0, columnspan=2)

# ---------------------------- Labels ------------------------------- #

current_language = canvas.create_text(400, 150, text="French", font=LANGUAGE_LABEL_FONT)
current_word = canvas.create_text(400, 263, text=f"French Fries", font=WORD_LABEL_FONT)

# ---------------------------- Buttons ------------------------------- #
right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=remove_known_word)
right_button.grid(column=1, row=1, pady=20)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=set_state_french_and_reset)
wrong_button.grid(column=0, row=1)

set_state_french_and_reset()
window.mainloop()
