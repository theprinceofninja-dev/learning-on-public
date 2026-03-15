import hashlib
import os
import tkinter as tk
from tkinter import messagebox


# Function to generate a secret key
def generate_secret_key(username):
    return hashlib.sha256(username.encode()).hexdigest()


# Function to check if the program is activated
def is_activated():
    return os.path.exists("activation.flag")


# Function to activate the program
def activate_program():
    with open("activation.flag", "w") as f:
        f.write("Activated")


# Function to check the secret key and activate the program
def check_secret_key():
    username = username_entry.get()
    secret_key = generate_secret_key(username)
    input_key = secret_key_entry.get()

    if input_key == secret_key:
        if not is_activated():
            activate_program()
            messagebox.showinfo("Activation", "Program activated successfully!")
        else:
            messagebox.showinfo("Activation", "Program already activated!")
    else:
        messagebox.showerror("Error", "Invalid secret key!")


# GUI setup
root = tk.Tk()
root.title("Secret Key Activation")

username_label = tk.Label(root, text="Enter Username:")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

secret_key_label = tk.Label(root, text="Enter Secret Key:")
secret_key_label.pack()

secret_key_entry = tk.Entry(root, show="*")
secret_key_entry.pack()

activate_button = tk.Button(root, text="Activate", command=check_secret_key)
activate_button.pack()

root.mainloop()
