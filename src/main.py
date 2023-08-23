import customtkinter as ctk
import pywinstyles
import os, time, subprocess, threading
from home import Home
from fbot import FacebookBot

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
app = ctk.CTk()
pywinstyles.apply_style(app, style="acrylic")
app.geometry("450x500")

app.title("Login Interface")

def entry_login():
    # print(f'{entry1.get()} + {entry2.get()}')
    # print(f"Check Box value: {checkbox.get()}") #checkbox.get() either 1 or 0
    if remember_var.get():
        save_login()
    fb = FacebookBot(entry1.get(), entry2.get())
    fb.login()
    app.toplevel_window = Home(fb)
    app.withdraw()

def run_batch_file():
    batch_file_path = r"cmd_note.bat"
    subprocess.run([batch_file_path], shell=True, check=True)

def start_thread():
    thread = threading.Thread(target=run_batch_file)
    thread.start()

def brower_login():
    # thread = threading.Thread(target=run_batch_file)
    # thread.start()
    if remember_var.get():
        save_login()
    fb = FacebookBot(entry1.get(), entry2.get(), browser_type=1)
    fb.login()
    app.toplevel_window = Home(fb)
    app.withdraw()
username_var = ctk.StringVar()
password_var = ctk.StringVar()
remember_var = ctk.BooleanVar()

def load_saved_login():
        try:
            with open("login_info.txt", "r") as file:
                lines = file.readlines()
                if len(lines) == 3:
                    username = lines[0].strip()
                    password = lines[1].strip()
                    remember = lines[2].strip()
                    username_var.set(username)
                    password_var.set(password)
                    remember_var.set(remember == "True")
        except FileNotFoundError:
            pass

def save_login():
    with open("login_info.txt", "w") as file:
        file.write(username_var.get() + "\n")
        file.write(password_var.get() + "\n")
        file.write(str(remember_var.get()))

def login():
    # Perform login logic here
    if remember_var.get():
        save_login()

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=20, padx=10)

load_saved_login()

entry1 = ctk.CTkEntry(master=frame, placeholder_text="Username", textvariable=username_var)
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame, placeholder_text="Password", textvariable=password_var, show="*")
entry2.pack(pady=12, padx=10)

button1 = ctk.CTkButton(master=frame, text="Login from here", command=entry_login)
button1.pack(pady=12, padx=10)

button2 = ctk.CTkButton(master=frame, text="Login from Browser", command=brower_login)
button2.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text="Remember me", variable=remember_var)
checkbox.pack(pady=12, padx=10)

app.mainloop()