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
root.iconphoto(False, PhotoImage(file="./icons/icon.png"))
root.geometry(config['size'])
root.title(config['title'])
root.config(background=config["background_color"])
root.resizable(width=False, height=False)

frame = ttk.Frame(root, padding=12)
frame.pack()

controls_container = ttk.Frame(frame)

file_path = CTkLabel(frame,
                     width=56,
                     font=('arial', 19),
                     bg_color=config['background_color'],
                     text="Nenuma pasta selecionada")


status_message = CTkLabel(frame,
                          font=('arial', 17),
                          width=56,
                          text="",
                          bg_color=config['background_color'])

logs_list_box = Listbox(
    frame,
    font="arial",
    activestyle="none",
    width=50,
    borderwidth=2,
    height=12,
    border=0,
    background=config["background_color"])


def select_folder():
    global folder_path
    folder_path = fd.askdirectory()
    file_path.configure(text=folder_path)


def is_port_success(port):
    command = ["java", "-jar", "./lib/hdl.jar", port]
    results = subprocess.run(command, capture_output=True, text=True)
    return results.stdout


def start_spector():
    position = 0
    logs_list_box.delete(0, END)

    try:
        status_message.configure(text_color="#3700b3", text="Verificando...")
        for file in os.listdir(folder_path):
            if file.endswith(".tst"):
                logs_list_box.update()
                full_path = f"{folder_path}/{file}"
                file_name = file.split(".")[0]

                if is_port_success(full_path):
                    logs_list_box.insert(
                        position, f"[PASSOU]: {file_name}")
                    logs_list_box.itemconfig(position, {'fg': 'green'})

                else:
                    logs_list_box.insert(
                        position, f"[NÃO PASSOU]: {file_name}")
                    logs_list_box.itemconfig(position, {'fg': '#B00020'})

                time.sleep(0.7)
                position += 1
                logs_list_box.see(position)

        status_message.configure(text="Teste finalizado!")
        logs_list_box.see(position)

    except:
        status_message.configure(
            text_color='#B00020',
            text='Error essa pasta não contem testes hdl!')


style = ttk.Style()
style.configure("TFrame", background=config["background_color"])


button_select_folder = CTkButton(
    controls_container,
    command=select_folder,
    text="Selecionar pasta",
    text_color="#000000",
    hover_color="#B49C00",
    fg_color="#FFDE03")

button_start_spector = CTkButton(
    controls_container,
    command=start_spector,
    text="Iniciar Teste",
    fg_color="#3303FF",
    hover_color="#1D0085",)

if __name__ == "__main__":
    controls_container.grid(column=0, row=3)
    file_path.grid(column=0, row=0)
    status_message.grid(column=0, row=1, pady=12)
    button_select_folder.grid(column=0, row=0, padx=12, pady=12)
    logs_list_box.grid(column=0, row=2)
    button_start_spector.grid(column=1, row=0, padx=12, pady=12)
    root.mainloop()
