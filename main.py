import PySimpleGUI as sg
from ADMIN_drug_module import show_drug_list_window
from ADMIN_customer_module import show_customers_list_window, show_register_customers_window, validate_user_login
from klient_login import show_user_main_window
from Agent import agent_ai

CORRECT_UN = ""
CORRECT_PIN = ""


def create_admin_window():
    layout = [
        [sg.T("Witaj,Administratorze", 
              font=('Helvetica', 16))],
        [sg.Button('Lista klientów', size=(20, 2), button_color=('white', 'green'))],
        [sg.B('Lista leków', size=(20, 2), button_color=('white', 'green'))],

    ]
    
    layout.append([sg.B('Wyloguj się', size=(20, 2), button_color=('white', 'red'))])
    
    window = sg.Window('System Apteki', layout, element_justification='center', background_color='#2B2B2B')
    
    while True:
        event, values = window.read()
        
        if event is None or event == 'Wyloguj się':
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

        [sg.B('Zaloguj się', size=(20, 2), button_color=('white', 'green'))],
        [sg.B('Zarejestruj się', size=(20, 2), button_color=('white', 'blue'))],
        [sg.B('Wyjdź', size=(20, 2), button_color=('white', 'red'))],
        [sg.Button("Skontaktuj sie z asystenetem AI")]
    ]
    window = sg.Window('Witamy w systemie apteki', layout, background_color='#2B2B2B')
    return window
def login_window():
    layout = [
        [sg.Text('Nazwa użytkownika:'), sg.Input(key='-UNAME-')],
        [sg.Text('Hasło:'), sg.Input(key='-PASS-', password_char='*')],
        [sg.B('Zaloguj', button_color=('white', 'green')), sg.B('Anuluj')]
    ]
    return sg.Window('Logowanie', layout, background_color='#2B2B2B')


def main():
    while True:
        window = start_window()
        while True:
            event, _ = window.read()
            if event is None or event == 'Wyjdź':
                window.close()
                return

            if event == 'Zarejestruj się':
                show_register_customers_window()
                window.close()
                break
            if event == 'Skontaktuj sie z asystenetem AI':
                agent_ai()


            if event == 'Zaloguj się':
                login = login_window()
                while True:
                    event, values = login.read()
                    if event is None or event == 'Anuluj':
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
