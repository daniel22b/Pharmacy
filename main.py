import PySimpleGUI as sg

# Ustaw ciemny motyw
sg.theme('DarkGrey13')

from ADMIN_drug_module import show_drug_list_window
from ADMIN_customer_module import show_customers_list_window, show_register_customers_window, validate_user_login
from klient_login import show_user_main_window

CORRECT_UN = ""
CORRECT_PIN = ""


def create_admin_window():
    layout = [
        [sg.Text('Panel Administratora', font=('Helvetica', 18, 'bold'), justification='center', expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('Wybierz akcję:', font=('Helvetica', 14))],
        [sg.Button('Lista klientów', size=(25, 2), button_color=('white', '#2E8B57'), font=('Helvetica', 12))],
        [sg.Button('Lista leków', size=(25, 2), button_color=('white', '#2E8B57'), font=('Helvetica', 12))],
        [sg.Button('Wyloguj się', size=(25, 2), button_color=('white', '#8B0000'), font=('Helvetica', 12))]
    ]

    column = [[sg.Column(layout, element_justification='center', pad=(20, 20))]]

    window = sg.Window('System Apteki - Administrator', column, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Wyloguj się'):
            window.close()
            return True

        if event == 'Lista klientów':
            window.hide()
            show_customers_list_window()
            window.un_hide()

        if event == 'Lista leków':
            window.hide()
            show_drug_list_window()
            window.un_hide()


def start_window():
    layout = [
        [sg.Text('Witamy w systemie apteki', font=('Helvetica', 18, 'bold'), justification='center', expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Button('Zaloguj się', size=(25, 2), button_color=('white', '#2E8B57'), font=('Helvetica', 12))],
        [sg.Button('Zarejestruj się', size=(25, 2), button_color=('white', '#1E90FF'), font=('Helvetica', 12))],
        [sg.Button('Wyjdź', size=(25, 2), button_color=('white', '#8B0000'), font=('Helvetica', 12))]
    ]
    column = [[sg.Column(layout, element_justification='center', pad=(20, 20))]]
    return sg.Window('Witamy w systemie apteki', column, finalize=True)


def login_window():
    layout = [
        [sg.Text('Nazwa użytkownika:', font=('Helvetica', 12)), sg.Input(key='-UNAME-')],
        [sg.Text('Hasło:', font=('Helvetica', 12)), sg.Input(key='-PASS-', password_char='*')],
        [sg.Button('Zaloguj', size=(12, 1), button_color=('white', '#2E8B57')),
         sg.Button('Anuluj', size=(12, 1), button_color=('white', '#8B0000'))]
    ]
    return sg.Window('Logowanie', layout, element_justification='center', finalize=True)


def main():
    while True:
        window = start_window()
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, 'Wyjdź'):
                window.close()
                return

            if event == 'Zarejestruj się':
                show_register_customers_window()
                window.close()
                break

            if event == 'Zaloguj się':
                login = login_window()
                while True:
                    event, values = login.read()
                    if event in (sg.WIN_CLOSED, 'Anuluj'):
                        login.close()
                        break

                    if event == 'Zaloguj':
                        uname = values['-UNAME-']
                        passwd = values['-PASS-']
                        if uname == CORRECT_UN and passwd == CORRECT_PIN:
                            login.close()
                            window.close()
                            create_admin_window()
                            break
                        elif validate_user_login(uname, passwd):
                            login.close()
                            window.close()
                            show_user_main_window(uname)
                            break
                        else:
                            sg.popup_error('Nieprawidłowa nazwa użytkownika lub hasło')
                break


if __name__ == '__main__':
    main()
