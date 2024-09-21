import tkinter.messagebox
from tkinter import *
from tkinter import messagebox
import pandas
import random


from_language = input("Choose from language: ")
to_language = input ("Choose to language: ")


BACKGROUND_COLOR = "#B1DDC6"
to_learn= {}

try:
    data = pandas.read_csv('./data/to_learn_words.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('./data/EtoB.csv')
    to_learn = original_data.to_dict(orient='records')

else:
    to_learn = data.to_dict(orient='records')

word_list= {}


def next_word():
    global word_list, flip_timer
    window.after_cancel(flip_timer)
    word_list= random.choice(to_learn)
    answer_word= word_list[f"{from_language}"]
    canvas.itemconfig(card_title, text=f"{from_language}", font=("Arial", 40, "italic", "bold"),fill="black")
    canvas.itemconfig(card_word, text=f"{answer_word}", font=("Arial", 60, "italic", "bold"), fill="black")
    canvas.itemconfig(card_background, image=front_image)
    flip_timer=window.after(5000, show_answer)


def show_answer():
    burmese_word = word_list[f"{to_language}"]
    canvas.itemconfig(card_title, text=f"{to_language}", font=("Arial", 40, "italic", "bold"),fill= "white")
    canvas.itemconfig(card_word, text=f"{burmese_word}", font=("Arial", 60, "italic", "bold"), fill="white")
    canvas.itemconfig(card_background, image=back_image)


def learned_words():
    next_word()
    to_learn.remove(word_list)
    pandas.DataFrame(to_learn).to_csv("./data/to_learn_words.csv", index=False)



window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, show_answer)


canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)


canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


card_title = canvas.create_text(400,150, text=f"{from_language}", font=("Arial", 40, "italic", "bold"))
card_word = canvas.create_text(400, 350, text=f"{to_language}", font=("Arial", 60, "italic", "bold"))

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image , highlightthickness=0, bg=BACKGROUND_COLOR, command= lambda: next_word())
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image , highlightthickness=0, bg=BACKGROUND_COLOR,command= lambda: learned_words())
right_button.grid(column=1, row=1)


window.mainloop()