import PySimpleGUI as sg
from USER_drug_module import show_user_drug_window
from layout_utils import center_layout
def show_user_main_window(client_id):
    layout = [
        [sg.Text("Witaj, użytkowniku!", font=('Segoe UI', 24), justification='center', background_color='white')],
        [sg.Button('Lista leków', size=(30, 3), button_color=('white', '#89CFF0'), font=('Segoe UI', 14))],
        [sg.Button('Wyloguj się', size=(30, 3), button_color=('white', '#FF6B6B'), font=('Segoe UI', 14))]
    ]

    window = sg.Window(
        "Panel użytkownika",
        center_layout(layout),
        background_color='white',
        size=(1200, 900),
        element_justification='center',
        finalize=True
    )

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Wyloguj się":
            break
        elif event == "Lista leków":
            window.hide()
            show_user_drug_window(client_id)  # Nowe wywołanie z koszykiem
            window.un_hide()

    window.close()
