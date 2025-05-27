import PySimpleGUI as sg
from ADMIN_drug_module import show_drug_list_window
from ADMIN_customer_module import show_customers_list_window,show_register_customers_window


CORRECT_PIN = "123"

#==================================================================
#=====================LOGIN WINDOW=========================


def create_login_window():
    layout = [
        [sg.T('System Apteki', font=('Helvetica', 20))],
        [sg.T('Wybierz typ logowania:', font=('Helvetica', 12))],
        [sg.B('User', size=(20, 2), button_color=('white', 'green'))],
        [sg.B('Admin', size=(20, 2), button_color=('white', 'green'))]
    ]
    
    window = sg.Window('Logowanie', layout, element_justification='center', background_color='#2B2B2B')
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            return None
            
        if event == 'User':
            if 1==True:
            # if show_register_customers_window():

                window.close()
                return 'User'
            
        if event == 'Admin':
            if show_pin_window():
                window.close()
                return 'Admin'
    

#==================================================================
#=====================PIN WINDOW=========================

def show_pin_window():
    """Show PIN input window for admin login"""
    layout = [
        [sg.T('Wprowadź PIN:')],
        [sg.I(password_char='*', key='-PIN-')],
        [sg.B('Potwierdź', button_color=('white', 'green'))]
    ]
    
    window = sg.Window('PIN', layout, element_justification='center', background_color='#2B2B2B')
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            window.close()
            return False
            
        if event == 'Potwierdź':
            if values['-PIN-'] == CORRECT_PIN:
                window.close()
                return True
            else:
                sg.popup_error('Nieprawidłowy PIN')
    
#==================================================================
#=====================MAIN WINDOW=========================


def create_main_window(user_type):
    """Create and show the main window"""
    layout = [
        [sg.T(f'Witaj, {"Administratorze" if user_type == "Admin" else "użytkowniku"}!', 
              font=('Helvetica', 16))],
    ]
    
    if user_type == 'Admin':
        layout.extend([
            [sg.B('Lista klientów', size=(20, 2), button_color=('white', 'green'))],
            [sg.B('Lista leków', size=(20, 2), button_color=('white', 'green'))]
        ])
    elif user_type == 'User':
        layout.extend([
            [sg.B('Zaloguj się', size=(20, 2), button_color=('white', 'green'))],
            [sg.B('Zarejestruj się', size=(20, 2), button_color=('white', 'green'))]
        ])
    
    layout.append([sg.B('Wyloguj się', size=(20, 2), button_color=('white', 'red'))])
    
    window = sg.Window('System Apteki', layout, element_justification='center', background_color='#2B2B2B')
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
            
        if event == 'Wyloguj się':
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

        if event == 'Zaloguj się':
            sg.popup_ok("Zalogowano (funkcja do uzupełnienia)")
        
        if event == 'Zarejestruj się':
            show_register_customers_window()
    
    window.close()

def main():
    while True:
        user_type = create_login_window()
        if user_type is None:
            break
            
        if not create_main_window(user_type):
            break

if __name__ == '__main__':
    main()