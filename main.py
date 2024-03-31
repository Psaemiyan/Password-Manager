import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    generated_password = "".join(password_list)
    pass_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    web = web_entry.get()
    e_mail = email_entry.get()
    pass_word = pass_entry.get()
    new_data = {
        web: {
        "email": e_mail,
        "password": pass_word
        }
    }

    if len(web) == 0 or len(pass_word) == 0 or len(e_mail) == 0:
        messagebox.showinfo(title="Oops", message="Information incomplete!")

    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # If the file doesn't exist or is empty, create an empty dictionary
            data = {}
            #updating new data to old data
        data.update(new_data)

        with open("data.json", "w") as data_file:
            #saving updated data
            json.dump(data, data_file, indent=4)

            web_entry.delete(0, END)
            email_entry.delete(0, END)
            pass_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    web_entered = web_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="File not found!")
    else:
        if web_entered in data:
            email = data[web_entered]["email"]
            password = data[web_entered]["password"]
            messagebox.showinfo(title=web_entered, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message="Website not found!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# labels
website = Label(text="Website")
website.grid(column=0, row=1)

email = Label(text="Email/Username")
email.grid(column=0, row=2)

password = Label(text="Password")
password.grid(column=0, row=3)

# Entries
web_entry = Entry(width=21)
web_entry.grid(column=1, row=1)
web_entry.focus()

email_entry = Entry(width=38)
email_entry.grid(column=1, row=2, columnspan=2)


pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3)

# Buttons

search = Button(text="Search", width=13, command=find_password)
search.grid(column=2, row=1)

generate_pass = Button(text="Generate password", command=gen_password)
generate_pass.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
