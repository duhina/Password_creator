from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json

BLACK = "#010326"
GREY = "#F2F2F2"
YELLOW = "#F2EEAC"
DARK_BLUE = "#010B40"
BLUE = "#94C6F2"

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['@', '!', '#', '$', '%', '&', '(', ')', '*', '+', ';', ':', '[', ']', '/']

def show_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def generate_password():

    password_letters = [choice(LETTERS) for _ in range(randint(10, 12))]
    password_symbols = [choice(SYMBOLS) for _ in range(randint(3, 6))]
    password_numbers = [choice(NUMBERS) for _ in range(randint(3, 6))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website:
        {
        "email": email,
        "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=YELLOW)

canvas = Canvas(width=470, height=400, highlightthickness=0, bg=YELLOW)
logo_img = PhotoImage(file="icon.png")
canvas.create_image(240, 180, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", fg=BLACK, bg=YELLOW, font="Arial, 14")
website_label.grid(column=0, row=1, padx=5, pady=5)

email_label = Label(text="Email/Username:", fg=BLACK, bg=YELLOW, font="Arial, 14")
email_label.grid(column=0, row=2, padx=5, pady=5)

password_label = Label(text="Password:", fg=BLACK, bg=YELLOW, font="Arial, 14")
password_label.grid(column=0, row=3, padx=5, pady=5)

website_entry = Entry(width=77)
website_entry.grid(column=1, row=1, sticky="w")
website_entry.focus()

email_entry = Entry(width=77)
email_entry.grid(column=1, row=2, columnspan=2, sticky="w")
email_entry.insert(0, "daria@gmail.com")

password_entry = Entry(window, width=77, show="*")
password_entry.grid(column=1, row=3, sticky="w")

search_button = Button(text="Search", width=20, command=find_password, bg=BLACK, fg=GREY)
search_button.grid(column=2, row=1)

generate_password_button = Button(text="Generate Password", width=20, command=generate_password, bg=BLACK, fg=GREY)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=40, command=save, fg=BLACK, bg=BLUE)
add_button.grid(column=1, row=4, columnspan=2, sticky="w", padx=90, pady=5)

show_button = Checkbutton(window, text="Show password", width=37, command=show_password, fg=BLACK)
show_button.grid(column=1, row=5, columnspan=2, sticky="w", padx=90, pady=5)

window.mainloop()
