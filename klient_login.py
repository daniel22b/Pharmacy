import PySimpleGUI as sg
from ADMIN_drug_module import show_drug_list_window

def show_user_main_window(client_id):
    layout = [
        [sg.Text("Witaj, użytkowniku!", font=('Helvetica', 16))],
        [sg.Button("Lista leków", button_color=('white', 'green'))],
        [sg.Button("Wyloguj się", button_color=('white', 'red'))]
    ]

    window = sg.Window("Panel użytkownika", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Wyloguj się":
            break
        elif event == "Lista leków":
            window.hide()
            show_drug_list_window(user_mode=True, client_id=client_id)
            window.un_hide()

    window.close()