import os
import subprocess
import time
import threading
from json import load
from tkinter import *
from customtkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog as fd


config = load(open("./config.json"))

status_running = {
    "is_canceled": False
}


root = CTk()
root.configure(**config['window_config'])
root.iconphoto(False, PhotoImage(file=config['icon']))
root.title(config['title'])
root.resizable(width=False, height=False)


style = ttk.Style()
style.configure("TFrame", background=config["background_color"])

frame = ttk.Frame(root, padding=12)
frame.grid()


file_path_label = CTkLabel(frame, font=('arial', 18), wraplength=250)
file_path_label.configure(**config['file_path_label'])


status_message_label = CTkLabel(frame, font=('arial', 16))
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


def start_spector_thread():
    threading.Thread(target=start_spector).start()


def start_spector():
    position = 0
    logs_list_box.delete(0, END)
    status_running['is_canceled'] = False
    try:
        status_message_label.configure(**config['status_message']['verify'])

        for file in os.listdir(folder_path):
            if file.endswith(".tst"):
                logs_list_box.update()
                full_path = f"{folder_path}/{file}"
                file_name = file.split(".")[0]

                if status_running['is_canceled']:
                    status_message_label.configure(
                        **config['status_message']['canceled'])
                    break

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

        if not status_running['is_canceled']:
            status_message_label.configure(
                **config['status_message']['finished'])
            logs_list_box.see(position)

    except:
        status_message_label.configure(**config['status_message']['error'])


def stop_process():
    if status_running['is_canceled']:
        status_running['is_canceled'] = False
    status_running['is_canceled'] = True


controls_container = ttk.Frame(frame)

separator = Frame(frame, height=1, width=450, background="#eee")

button_select_folder = CTkButton(controls_container, command=select_folder)
button_select_folder.configure(**config['button_select_folder'])


button_start_spector = CTkButton(
    controls_container, command=start_spector_thread)
button_start_spector.configure(**config['button_start_spector'])

button_stop_process = CTkButton(controls_container, command=stop_process)
button_stop_process.configure(**config['button_stop_process'])


if __name__ == "__main__":
    file_path_label.grid(column=0, row=0, pady=2)
    logs_list_box.grid(column=0, row=2, pady=20)
    separator.grid(column=0, row=3, pady=12)
    status_message_label.grid(column=0, row=4, pady=2)
    controls_container.grid(column=0, row=5)
    button_select_folder.grid(column=1, row=1, padx=5, pady=10)
    button_stop_process.grid(column=2, row=1, padx=5, pady=10)
    button_start_spector.grid(column=3, row=1, padx=5, pady=10)
    root.mainloop()
