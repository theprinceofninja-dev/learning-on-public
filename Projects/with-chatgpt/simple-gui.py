import tkinter as tk
from tkinter import messagebox


def calculate_square():
    try:
        number = float(entry.get())
        result = number**2
        messagebox.showinfo("Result", f"The square of {number} is {result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")


# Create the main window
root = tk.Tk()
root.title("Square Calculator")

# Create a label
label = tk.Label(root, text="Enter a number:")
label.pack()

# Create an entry field
entry = tk.Entry(root)
entry.pack()

# Create a button to calculate the square
calculate_button = tk.Button(root, text="Calculate Square", command=calculate_square)
calculate_button.pack()

# Run the Tkinter event loop
root.mainloop()
