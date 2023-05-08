import os
import subprocess
import time
from json import load
from tkinter import *
from customtkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog as fd

config = load(open("./config.json"))


root = CTk()
root.configure(**config['window_config'])
root.iconphoto(False, PhotoImage(file=config['icon']))
root.title(config['title'])
root.resizable(width=False, height=False)


frame = ttk.Frame(root, padding=12)
frame.pack()


controls_container = ttk.Frame(frame)


file_path_label = CTkLabel(frame, font=('arial', 18))
file_path_label.configure(**config['file_path_label'])


status_message_label = CTkLabel(frame, font=('arial', 15))
status_message_label.configure(**config['status_message_label'])


logs_list_box = Listbox(frame)
logs_list_box.configure(config['logs_list_box'])


def select_folder():
    global folder_path
    folder_path = fd.askdirectory()
    file_path_label.configure(text=folder_path)


def is_port_success(port):
    command = ["java", "-jar", "./lib/hdl.jar", port]
    results = subprocess.run(command, capture_output=True, text=True)
    return results.stdout


def start_spector():
    position = 0
    logs_list_box.delete(0, END)

    try:
        status_message_label.configure(**config['status_message']['verify'])

        for file in os.listdir(folder_path):
            if file.endswith(".tst"):
                logs_list_box.update()
                full_path = f"{folder_path}/{file}"
                file_name = file.split(".")[0]

                if is_port_success(full_path):
                    logs_list_box.insert(
                        position, f"[PASSOU]: {file_name} ✓")
                    logs_list_box.itemconfig(
                        position, fg=config['status_color']['success'])

                else:
                    logs_list_box.insert(
                        position, f"[NÃO PASSOU]: {file_name} ✖")
                    logs_list_box.itemconfig(
                        position, fg=config['status_color']['error'])

                time.sleep(1)
                position += 1
                logs_list_box.see(position)

        status_message_label.configure(**config['status_message']['finished'])
        logs_list_box.see(position)

    except:
        status_message_label.configure(**config['status_message']['error'])


style = ttk.Style()
style.configure("TFrame", background=config["background_color"])


button_select_folder = CTkButton(controls_container, command=select_folder)
button_select_folder.configure(**config['button_select_folder'])


button_start_spector = CTkButton(controls_container, command=start_spector)
button_start_spector.configure(**config['button_start_spector'])


if __name__ == "__main__":
    controls_container.grid(column=0, row=3)
    file_path_label.grid(column=0, row=0)
    status_message_label.grid(column=0, row=1, pady=12)
    button_select_folder.grid(column=0, row=0, padx=12, pady=12)
    logs_list_box.grid(column=0, row=2)
    button_start_spector.grid(column=1, row=0, padx=12, pady=12)
    root.mainloop()
