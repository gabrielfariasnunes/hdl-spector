import os
import compiler
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


file_path_label = CTkLabel(
    frame,
    font=('arial', 18),
    wraplength=250)


file_path_label.configure(**config['file_path_label'])


status_progress_bar = CTkProgressBar(frame, width=385,  height=5)
status_progress_bar.set(0)

status_message_label = CTkLabel(frame, text="")

logs_list_box = Listbox(frame)
logs_list_box.configure(config['logs_list_box'])


def select_folder():
    global folder_path
    folder_path = fd.askdirectory()
    file_path_label.configure(text=folder_path)


def start_spector_thread():
    threading.Thread(target=spector).start()


def total_tst(ports):

    total = 0
    for port in ports:
        if port.endswith(".tst"):
            total += 1
    return total


def message_alert(type, message):
    status_message_label.configure(text=message)
    status_message_label.configure(**config['status_message'][type])


def spector():
    position = 0
    total_faillure_ports = 0
    logs_list_box.delete(0, END)
    status_running['is_canceled'] = False

    try:

        ports = os.listdir(folder_path)
        total = total_tst(ports)
        message_alert('verify', 'Verificando...')

        for file in ports:

            if file.endswith(".tst"):
                logs_list_box.update()
                full_path = f"{folder_path}/{file}"
                file_name = file.split(".")[0]

                if status_running['is_canceled']:
                    status_progress_bar.set(0)
                    message_alert('error', 'Verificação cancelada!')
                    break

                if compiler.build(full_path):
                    logs_list_box.insert(
                        position, f"[PASSOU]: {file_name} ✓")
                    logs_list_box.itemconfig(
                        position, fg=config['status_color']['success'])

                else:
                    total_faillure_ports += 1
                    logs_list_box.insert(
                        position, f"[NÃO PASSOU]: {file_name} ✖")
                    logs_list_box.itemconfig(
                        position, fg=config['status_color']['error'])

                position += 1
                time.sleep(1)
                logs_list_box.see(position)
                status_progress_bar.set(((position / total)))

        if not status_running['is_canceled']:
            if total_faillure_ports > 0:
                message_alert(
                    'finished_error', f"Teste finalizado!, {total_faillure_ports} portas com erro de implentação!")
            else:
                message_alert(
                    'finished_success', f"Teste finalizado!, sem nenhuma porta com error, Parabéns!")

    except:
        message_alert('error', 'Error essa pasta não contem testes hdl!')


def stop_process():
    if status_running['is_canceled']:
        status_running['is_canceled'] = False
    status_running['is_canceled'] = True


controls_container = ttk.Frame(frame)


separator = Frame(frame, height=1, width=450, background="#eee")


button_select_folder = CTkButton(controls_container, command=select_folder)
button_select_folder.configure(**config['button_select_folder'])


button_start_spector = CTkButton(
    controls_container,
    command=start_spector_thread)

button_start_spector.configure(**config['button_start_spector'])


button_stop_process = CTkButton(controls_container, command=stop_process)
button_stop_process.configure(**config['button_stop_process'])


if __name__ == "__main__":
    file_path_label.grid(column=0, row=0, pady=2)
    logs_list_box.grid(column=0, row=2, pady=20)
    status_progress_bar.grid(column=0, row=3, pady=2)
    status_message_label.grid(column=0, row=4, pady=2)
    controls_container.grid(column=0, row=5)
    button_select_folder.grid(column=1, row=1, padx=5, pady=10)
    button_stop_process.grid(column=2, row=1, padx=5, pady=10)
    button_start_spector.grid(column=3, row=1, padx=5, pady=10)
    root.mainloop()
