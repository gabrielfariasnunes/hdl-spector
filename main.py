from os import listdir
from compiler import build
from time import sleep
from threading import Thread
from json import load
from tkinter import *
from customtkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog as fd

INTERVAL_CHECK = 1

config = load(open("./config.json"))

status_running = {
    "is_canceled": False
}

folder_location = {
    "pathname": ""
}

root = CTk()
root.iconphoto(False, PhotoImage(file=config['icon']))
root.title(config['title'])
root.resizable(width=False, height=False)

style = ttk.Style()
style.configure("TFrame", background=config["background_color"])

frame = ttk.Frame(root, padding=12)
frame.grid()

file_path_label = CTkLabel(frame, font=('arial', 16))
file_path_label.configure(**config['file_path_label'])

logs_list_box = Listbox(frame)
logs_list_box.configure(config['logs_list_box'])

status_message_label = CTkLabel(frame, text="")


def get_folder_location():
    return folder_location['pathname']


def select_folder():
    path = fd.askdirectory()
    folder_location['pathname'] = path
    file_path_label.configure(text=path)


def start_spector_thread():
    Thread(target=spector).start()


def list_tsts():
    tsts = []
    path = get_folder_location()
    ports = listdir(path)
    for port in ports:
        if port.endswith(".tst"):
            tsts.append(port)
    return tsts


def log_add_event(position, message, status):
    color_passed = config['status_color']['color_passed']
    color_not_passed = config['status_color']['color_not_passed']

    if status:
        logs_list_box.insert(position, message)
        logs_list_box.itemconfig(position, fg=color_passed)
    else:
        logs_list_box.insert(position, message)
        logs_list_box.itemconfig(position, fg=color_not_passed)


def message_alert(color_name, message):
    status_message_label.configure(text_color=config['status_color'][color_name], text=message)


def log_next_event(position):
    logs_list_box.see(position)


def change_progress_state(position, total):
    progress = int((position / total) * 100)
    message_alert('checking_color', f'Verificando...({progress}%) concluido')


def spector():
    position = 0
    total_faillure_ports = 0
    logs_list_box.delete(0, END)
    status_running['is_canceled'] = False

    try:
        tsts = list_tsts()
        folder_path = get_folder_location()
        for file in list_tsts():
            if file.endswith(".tst"):
                logs_list_box.update()
                full_path = f"{folder_path}/{file}"
                file_name = file.split(".")[0]

                if status_running['is_canceled']:
                    message_alert('canceled_error', 'Verificação cancelada!')
                    break

                if build(full_path):
                    log_add_event(position, f"[PASSOU]: {file_name} ✓", True)
                else:
                    total_faillure_ports += 1
                    log_add_event(position, f"[NÃO PASSOU]: {file_name} ✖", False)

                position += 1
                change_progress_state(position, len(tsts))
                log_next_event(position)
                sleep(INTERVAL_CHECK)

        if not status_running['is_canceled']:
            if total_faillure_ports > 0:
                if total_faillure_ports == 1:
                    message_alert(
                        'finished_error',
                        f"Teste finalizado!, e {total_faillure_ports} porta com erro de implentação!")
                else:
                    message_alert(
                        'finished_error',
                        f"Teste finalizado!, e {total_faillure_ports} portas com erro de implentação!")
            else:
                message_alert(
                    'finished_success', f"Teste finalizado!, e sem nenhuma porta com error, Parabéns!")

    except FileNotFoundError:
        message_alert('folder_not_found', 'Error essa pasta não contem testes hdl!')


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
    status_message_label.grid(column=0, row=3, pady=2)
    controls_container.grid(column=0, row=4)
    button_select_folder.grid(column=1, row=1, padx=5, pady=10)
    button_stop_process.grid(column=2, row=1, padx=5, pady=10)
    button_start_spector.grid(column=3, row=1, padx=5, pady=10)
    root.mainloop()
