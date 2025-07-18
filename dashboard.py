import tkinter as tk
from tkinter import StringVar, OptionMenu, Button

# Calm Dashboard --------------------
def calm_dash():
    root = tk.Tk()
    root.title("Calm")
    root.geometry("350x200")
    root.configure(bg="#92B780")  # Light green background

    label = tk.Label(
        root, 
        text="You're feeling calm. \n\nKeep up the good work!", 
        bg="#92B780",        # Match the label background to the window
        fg="white",            # Text color
        font=("Arial", 14)     # nicer font
    )
    label.place(relx=0.5, rely=0.5, anchor="center")  # Center both axes
    root.mainloop() 



# Stressed Dashboard ---------------------
def stressed_dash():
    root = tk.Tk()
    root.title("Stressed")
    root.geometry("350x200")
    root.configure(bg="#CD4B4B")

    label = tk.Label(
        root, 
        text="It seems like you are stressed. \n\nYou could: \n -Take a 10 minute break. \n -Listen to your favorite song.", 
        bg="#CD4B4B",        # Match the label background to the window
        fg="white",            # Text color
        font=("Arial", 14)     # nicer font
    )
    label.place(relx=0.5, rely=0.5, anchor="center")  # Center both axes
    root.mainloop() 


# testing the dashboards
print("started")
calm_dash()
print(" dash")