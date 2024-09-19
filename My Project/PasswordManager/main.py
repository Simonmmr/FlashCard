
from tkinter import *
import random
import string
from tkinter import messagebox
import pyperclip
import json
from PIL import Image, ImageTk

window = Tk()
window.title('Password Manager', )
window.config(padx=10, pady=10)

canvas = Canvas(width=350, height=200, highlightthickness=0)


logo_image = Image.open('logo.png')
logo_photo = ImageTk.PhotoImage(logo_image)
canvas.create_image(110, 110, image=logo_photo)
canvas.grid(column=1, row=0,columnspan=2)

website_label = Label(text='Website')
website_label.grid(column=0, row=1)

web_entry = Entry(width=35)
web_entry.grid(column=1, row=1)

search_button = Button(text='Search', width=18,height=2, command=lambda :search())
search_button.grid(column=2, row=1, rowspan=2)

email_label = Label(text='Email/Username')
email_label.grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2)
email_entry.insert(0, 'zinkolaymgy@gmail.com')


password_label = Label(text='Password')
password_label.grid(column=0, row=3)

password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)


password_length = Label(text='Password Length')
password_length.grid(column=0, row=4)


password_length = Entry(width=35)
password_length.grid(column=1, row=4)
password_length.focus()


generate_password_button = Button(text='Generate Password',width=18,height=2, command=lambda:generate_password())
generate_password_button.grid(column=2, row=3, rowspan=2)

add_button = Button(text='Click To Save Information', width=50, command=lambda : save_password())
add_button.grid(row=5, column=1,columnspan=2)


def save_password():
    website = web_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            "Email":email,
            "Password":password
        }
    }


    if len(website) == 0 or len(password) == 0:
        messagebox.showerror('Error', 'Please make sure you do not left any filed empty.')

    else:
        try:
            with open('data.json', 'r') as data_file:
                #reading the file
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # updating the old file with new file
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                #writing the file to the existing file
                json.dump(data, data_file, indent=4)
        finally:
            password_entry.delete(0, END)
            web_entry.delete(0, END)
            password_length.delete(0, END)


def generate_password():
    try:
        length_choice = int(password_length.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter a valid number for the password length.')
        return
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length_choice))
    password_entry.insert(0, password)
    pyperclip.copy(password)


def search():
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)

        if web_entry.get() not in data:
            messagebox.showerror('Error', 'Website does not exist. PLease double check the spelling')
            return
        else:
            website = web_entry.get()
            email = data[website]["Email"]
            password = data[website]["Password"]

    is_ok =messagebox.showinfo('Your Search', f'Website:{website}\n Email:{email}\n Password:{password}')
    if is_ok:
        password_entry.insert(0, password)
        messagebox.showinfo("Info", "Your password has been copied to clipboard. Just paste at where you want")
        pyperclip.copy(password)

window.mainloop()