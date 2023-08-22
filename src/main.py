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
    thread = threading.Thread(target=run_batch_file)
    thread.start()
    fb = FacebookBot(entry1.get(), entry2.get(), 1)
    fb.login()
    app.toplevel_window = Home(fb)
    app.withdraw()

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=20, padx=10)

entry1 = ctk.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button1 = ctk.CTkButton(master=frame, text="Login from here", command=entry_login)
button1.pack(pady=12, padx=10)

button2 = ctk.CTkButton(master=frame, text="Login from Browser", command=brower_login)
button2.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text="Remember me")
checkbox.pack(pady=12, padx=10)

app.mainloop()