import PySimpleGUI as sg
from ADMIN_drug_module import show_drug_list_window
from ADMIN_customer_module import show_customers_list_window, show_register_customers_window, validate_user_login
from klient_login import show_user_main_window
from Agent import agent_ai
from layout_utils import input_style, center_layout, white_push

CORRECT_UN = ""
CORRECT_PIN = ""

sg.theme('DefaultNoMoreNagging')

def create_admin_window():
    """
    Tworzy i wyświetla okno panelu administratora.

    Okno zawiera przyciski:
    - Lista klientów: wyświetla listę zarejestrowanych klientów,
    - Lista leków: wyświetla listę leków w aptece,
    - Wyloguj się: zamyka panel i zwraca sterowanie.

    Funkcja działa w pętli, reagując na zdarzenia GUI.

    Returns:
        bool: Zwraca True po wylogowaniu administratora.
    """
    layout = [
        [sg.Text("Witaj, Administratorze", font=('Segoe UI', 24), justification='center', background_color='white')],
        [sg.Button('Lista klientów', size=(30, 3), button_color=('white', '#89CFF0'))],
        [sg.Button('Lista leków', size=(30, 3), button_color=('white', '#89CFF0'))],
        [sg.Button('Wyloguj się', size=(30, 3), button_color=('white', '#FF6B6B'))]
    ]
    window = sg.Window('Panel Administratora', center_layout(layout), background_color='white', size=(1200, 900), element_justification='center', finalize=True)

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
    """
    Tworzy i zwraca okno startowe aplikacji.

    Okno zawiera przyciski:
    - Zaloguj się,
    - Zarejestruj się,
    - Wyjdź,
    - Skontaktuj się z asystentem AI.

    Returns:
        sg.Window: Obiekt okna PySimpleGUI.
    """
    layout = [
        [sg.Text("Witamy w systemie apteki", font=('Segoe UI', 28), justification='center', background_color='white')],
        [sg.Button('Zaloguj się', size=(30, 3), button_color=('white', '#89CFF0'))],
        [sg.Button('Zarejestruj się', size=(30, 3), button_color=('white', '#89CFF0'))],
        [sg.Button('Wyjdź', size=(30, 3), button_color=('white', '#FF6B6B'))],
        [sg.Button('Skontaktuj sie z asystenetem AI', size=(35, 3), button_color=('black', '#D3D3D3'))]
    ]
    return sg.Window('Witamy w systemie apteki', center_layout(layout), background_color='white', size=(1200, 900), element_justification='center', finalize=True)

def login_window():
    """
    Tworzy i zwraca okno logowania użytkownika.

    Okno umożliwia podanie nazwy użytkownika i hasła, oraz przyciski:
    - Zaloguj,
    - Anuluj.

    Returns:
        sg.Window: Obiekt okna PySimpleGUI do logowania.
    """
    layout = [
        [sg.Text('Nazwa użytkownika:', font=('Segoe UI', 16), background_color='white')],
        [sg.Input(key='-UNAME-', **input_style)],
        [sg.Text('Hasło:', font=('Segoe UI', 16), background_color='white')],
        [sg.Input(key='-PASS-', password_char='*', **input_style)],
        [sg.Button('Zaloguj', size=(20, 2), button_color=('white', '#89CFF0')),
         sg.Button('Anuluj', size=(20, 2), button_color=('black', '#E0E0E0'))]
    ]
    return sg.Window('Logowanie', center_layout(layout), background_color='white', size=(1200, 900), element_justification='center', finalize=True)

def main():
    """
    Główna pętla programu uruchamiająca GUI apteki.

    Funkcja wyświetla okno startowe i obsługuje:
    - logowanie (admin lub klient),
    - rejestrację nowego użytkownika,
    - wyjście z aplikacji,
    - kontakt z asystentem AI.

    W przypadku poprawnego logowania:
    - dla administratora wywołuje create_admin_window(),
    - dla klienta wywołuje show_user_main_window(uname).

    Po wylogowaniu lub zamknięciu aplikacji funkcja kończy działanie.
    """
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
                        window.close()
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
