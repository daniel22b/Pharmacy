import PySimpleGUI as sg
from customer import add_customer
from drug_module import show_drug_list_window
from customer_module import show_customers_list_window


CORRECT_PIN = "123"

def create_login_window():
    """Create and show the login window"""
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
            window.close()
            return 'User'
            
        if event == 'Admin':
            window.close()
            if show_pin_window():
                return 'Admin'
    
    window.close()

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
    
    window.close()

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
    
    window.close()

# def show_registration_window():
#     """Show customer registration window"""
#     layout = [
#         [sg.T('Rejestracja klienta', font=('Helvetica', 16))],
#         [sg.T('Imię i nazwisko:'), sg.I(key='-NAME-')],
#         [sg.T('Email:'), sg.I(key='-EMAIL-')],
#         [sg.T('Telefon:'), sg.I(key='-PHONE-')],
#         [sg.T('Gender:'), 
#          sg.Combo(['MALE', 'FEMALE'], default_value='MALE', key='-GENDER-')],
#         [sg.T('Date of birth:'), sg.I(key='-DATE_OF_BIRTH-')],
#         [sg.T('Street:'), sg.I(key='-STREET-')],
#         [sg.T('City:'), sg.I(key='-CITY-')],
#         [sg.T('Country:'), sg.I(key='-COUNTRY-')],
#         [sg.B('Zarejestruj', button_color=('white', 'green')), 
#          sg.B('Anuluj', button_color=('white', 'gray'))]
#     ]
    
#     window = sg.Window('Rejestracja', layout, background_color='#2B2B2B')
    
#     while True:
#         event, values = window.read()
        
#         if event in (sg.WIN_CLOSED, 'Anuluj'):
#             break
            
#         if event == 'Zarejestruj':
#             name = values['-NAME-'].strip()
#             email = values['-EMAIL-'].strip()
#             phone = values['-PHONE-'].strip()
#             gender = values['-GENDER-'].strip()
#             date_of_birth = values['-DATE_OF_BIRTH-'].strip()
#             street = values['-STREET-'].strip()
#             city = values['-CITY-'].strip()
#             country = values['-COUNTRY-'].strip()

            
#             if not all([name, email, phone,date_of_birth,gender]):
#                 sg.popup_error('Uzupełnij wszystkie pola')
#                 continue
                
#             try:
#                 customer_id = add_customer(name, email, phone, date_of_birth,gender,street,city,country)
#                 print(f'Klient został dodany z ID: {customer_id}')
#                 sg.popup_ok(f'Klient został dodany z ID: {customer_id}')
#                 break
#             except Exception as e:
#                 sg.popup_error(f'Nie udało się dodać klienta: {e}')
    
#     window.close()

def main():
    while True:
        user_type = create_login_window()
        if user_type is None:
            break
            
        if not create_main_window(user_type):
            break

if __name__ == '__main__':
    main()