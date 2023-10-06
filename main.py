from tkinter import *
from tkinter import messagebox
import json
import random

# ------------------------------- CONSTANTS ------------------------------- #
WIDTH = 960
HEIGHT = 540
TITLE_FONT = ("Ariel", 20, "bold")
TIMER_FONT = ("Ariel", 20, "bold")
LABEL_FONT = ("Ariel", 18, "italic")
FRENCH_FONT = ("Ariel", 30, "bold")

timer = None
word = []
learned_words = []

# ------------------------------- WORDS IMPORT ------------------------------- #
with open('data/fr2000.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()

words = []
for line in data:
    line = line.lstrip('.1234567890 ')
    line = line.replace('\n', '')
    line = line.split(' – ')
    words.append(line)
word_list_length = len(words)


def load():
    try:
        with open('data/learned_words.json', 'r') as data_file:
            loaded_words = json.load(data_file)

        update_list(loaded_words)
    except:
        pass


def save():
    print(f"Learned words: {learned_words}")
    with open('data/learned_words.json', 'w') as data_file:
        json.dump(learned_words, data_file)


def update_list(loaded_words):
    global word
    print("Removing learned words.")
    for x in loaded_words:
        word = x
        remove_word()
    word = []


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count=3):
    global timer
    canvas.itemconfig(timer_text, text=f"{count}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        canvas.itemconfig(header, text='English', fill='white')
        canvas.itemconfig(background, image=background_image_flipped)
        canvas.itemconfig(text, text=word[1], fill='white')


def cancel_count_down():
    global timer
    try:
        window.after_cancel(timer)
    except ValueError:
        pass


# ------------------------------- BUTTON CONTROLS ------------------------------- #
def correct():
    if word:
        cancel_count_down()
        remove_word()
    new_word()


def incorrect():
    if word:
        cancel_count_down()
    new_word()


def end_game():
    save()
    window.destroy()


def reset():
    global learned_words
    if messagebox.askokcancel(title="Reset Progress?", message="Are you sure you want to remove all progress?"):
        learned_words = []
    else:
        pass


# ------------------------------- WORD CONTROLS ------------------------------- #
def remove_word():
    try:
        learned_words.append(word)
        words.pop(words.index(word))
    except ValueError:
        pass


def new_word():
    global word
    try:
        word = random.choice(words)
    except:
        print(f"All words learned! You win.")
        messagebox.showinfo(title="You Win!", message="You've learned all the words!\n")
    else:
        canvas.itemconfig(completion_text, text=f"{100*len(learned_words) / word_list_length}%")
        canvas.itemconfig(header, text='French', fill='black')
        canvas.itemconfig(background, image=background_image)
        canvas.itemconfig(text, text=word[0], fill='black')
        count_down()


# ------------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card Game")
window.minsize(width=WIDTH, height=HEIGHT)
window.config(bg='white')

# Photo
background_image = PhotoImage(file="images/background.png")
background_image_flipped = PhotoImage(file="images/background2.png")
# Get photo dimensions
image_width = background_image.width()
image_height = background_image.height()

# Scale down the photo
scale_factor = 0.5
new_width = int(image_width * scale_factor)
new_height = int(image_height * scale_factor)
background_image = background_image.subsample(int(1 / scale_factor), int(1 / scale_factor))
background_image_flipped = background_image_flipped.subsample(int(1 / scale_factor), int(1 / scale_factor))

canvas = Canvas(width=WIDTH, height=HEIGHT, highlightthickness=0)
background = canvas.create_image(new_width / 2, new_height / 2, image=background_image)
canvas.grid(row=0, column=0, columnspan=2, rowspan=2)

timer_text = canvas.create_text(new_width / 2, new_height / 5, text='', fill='grey', font=TIMER_FONT)

completion_text = canvas.create_text(new_width / 2, new_height / 20, text=f"{100*len(learned_words) / word_list_length}%",
                                     fill='grey', font=TIMER_FONT)

header = canvas.create_text(new_width / 2, new_height / 3 - 20, text="Language", fill='black', font=LABEL_FONT)
text = canvas.create_text(new_width / 2, new_height / 2 - 20, text="Word", fill='black', font=FRENCH_FONT)

checkmark_image = PhotoImage(file="images/checkmark50.png")
yes_button = Button(image=checkmark_image, highlightthickness=0, borderwidth=0)
yes_button.grid(row=1, column=1, sticky='sw', padx=50, pady=50)
yes_button.config(command=correct)

x_mark_image = PhotoImage(file="images/x mark 50.png")
no_button = Button(image=x_mark_image, highlightthickness=0, borderwidth=0)
no_button.grid(row=1, column=0, sticky='se', padx=50, pady=50)
no_button.config(command=incorrect)

quit_button = Button(window, text="Reset Progress", command=reset)
quit_button.grid(row=0, column=0, sticky='nw', padx=15, pady=15)

quit_button = Button(window, text="Save & Quit", command=end_game)
quit_button.grid(row=0, column=1, sticky='ne', padx=15, pady=15)

load()
# ------------------------------- END ------------------------------- #
window.mainloop()
