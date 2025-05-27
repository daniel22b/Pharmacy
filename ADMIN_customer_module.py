import PySimpleGUI as sg
import os
import pandas as pd
from Add_del_customer import add_customer,remove_customer

ADRESS_FILE = "address.csv"
CUSTOMERS_FILE = "customers.csv"

def load_customers(filter_query=''):
    try:
        if not os.path.exists(CUSTOMERS_FILE):
            return []
            
        df = pd.read_csv(CUSTOMERS_FILE)
        if df.empty:
            return []
        display_columns = ["ID","NAME","SURNAME","E-MAIL","PHONE","CREATED","AGE","GENDER"]
        df = df[display_columns]
            
        if filter_query:
            query = filter_query.lower()
            df = df[
                df["ID"].astype(str).str.lower().str.contains(query) |
                df["NAME"].astype(str).str.lower().str.contains(query)
            ]

        
        return df.values.tolist()
    except Exception as e:
        sg.popup_error(f'Nie można wczytać danych: {e}')
        return []

def show_customers_list_window():
    layout = [
        [sg.T('Lista klientów', font=('Helvetica', 16))],
        [sg.T('Wyszukaj:'), 
         sg.I(key='-SEARCH-', size=(30, 1)),
         sg.B('Szukaj', button_color=('white', 'green')),
         sg.B('Pokaż wszystko', button_color=('white', 'green'))],
        [sg.Table(values=[], 
                 headings=["ID","NAME","SURNAME","E-MAIL","PHONE","CREATED","AGE","GENDER"],
                 key='-TABLE-',
                 auto_size_columns=True,
                 justification='center',
                 num_rows=10,
                 background_color='#2B2B2B',
                 text_color='white',
                 header_background_color='green',
                 header_text_color='white',
                 select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                 enable_click_events=True)],
        [sg.B('Dodaj klienta', button_color=('white', 'green')), 
         sg.B('Usuń zaznaczony', button_color=('white', 'red')),
         sg.B('Zamknij', button_color=('white', 'gray'))]
    ]
    
    window = sg.Window('Lista klientow', layout, finalize=True, background_color='#2B2B2B')
    
    table_data = load_customers()
    window['-TABLE-'].update(table_data)
    
    while True:
        event, values = window.read()
        
        if event is None or event == 'Zamknij':
            break
            
        if event == 'Szukaj':
            table_data = load_customers(values['-SEARCH-'])
            window['-TABLE-'].update(table_data)
            
        if event == 'Pokaż wszystko':
            table_data = load_customers()
            window['-TABLE-'].update(table_data)
            
        if event == 'Dodaj klienta':
            show_register_customers_window()
            table_data = load_customers()
            window['-TABLE-'].update(table_data)
            
        if event == 'Usuń zaznaczony':
            selected = values['-TABLE-']
            if not selected or len(selected) == 0:
                sg.popup_warning('Zaznacz rekord do usunięcia')
                continue
                
            try:
                selected_row = selected[0]
                if selected_row >= len(table_data):
                    sg.popup_error('Nieprawidłowy wybór')
                    continue
                    
                row = table_data[selected_row]
                if sg.popup_yes_no(f'Czy na pewno chcesz usunąć klienta "{row[1]}" (ID: {row[0]})?') == 'Yes':
                    remove_customer(CUSTOMERS_FILE,row[0])
                    remove_customer(ADRESS_FILE,row[0])

                    sg.popup_ok(f'Klient "{row[1]}" (ID: {row[0]}) został usunięty')
                    table_data = load_customers()
                    window['-TABLE-'].update(table_data)
            except Exception as e:
                sg.popup_error(f'Nie udało się usunąć klienta: {e}')
    
    window.close()


#==========================================================================
 #===================================================================================


def show_register_customers_window():
    """Show window for adding new drugs"""
    layout = [
        [sg.T('Dodaj klienta', font=('Helvetica', 16))],
        [sg.T('Email:'), sg.I(key='-EMAIL-')],
        [sg.T('Nazwa użytkownika:'), sg.I(key='-USERNAME-')],
        [sg.T('Hasło:'), sg.I(password_char='*',key='-PASSWORD-')],
        [sg.T('Potwiedź hasło:'), sg.I(password_char='*',key='-CONFIRM-PASSWORD-')],
        [sg.T('Imie:'), sg.I(key='-NAME-')],
        [sg.T('Nazwisko:'), sg.I(key='-SRNAME-')],
        [sg.T('Telefon:'), sg.I(key='-PHONE-')],
        [sg.T('Data urodzenia:'), sg.I(key='-DOB-')],
        [sg.T('Ulica:'), sg.I(key='-STREET-')],
        [sg.T('Miasto:'), sg.I(key='-CITY-')],
        [sg.T('Kraj:'), sg.I(key='-COUNTRY-')],
        [sg.T('Płeć:'), 
         sg.Combo(['Kobieta', 'Mężczyzna'], default_value='Kobieta', key='-GENDER-')],
        [sg.B('Dodaj', button_color=('white', 'green')), 
         sg.B('Anuluj', button_color=('white', 'gray'))]
    ]
    
    window = sg.Window('Dodaj klienta', layout, background_color='#2B2B2B')
    
    while True:
        event, values = window.read()
        
        if event is None or event == 'Anuluj':
            break
            
        if event == 'Dodaj':
            name = values['-NAME-'].capitalize()
            surname = values['-SRNAME-'].capitalize()
            user_name = values['-USERNAME-']
            date_of_birth = values['-DOB-']
            gender = values['-GENDER-']
            street = values['-STREET-'].capitalize()
            city = values['-CITY-'].capitalize()
            country = values['-COUNTRY-'].capitalize()
            raw_phone = values['-PHONE-']

            email = values['-EMAIL-']
            if '@' not in email or '.' not in email:
                sg.popup_error('Nieprawidłowy adres e-mail. Musi zawierać "@" oraz "."')
                continue

            if not raw_phone.isdigit() or len(raw_phone) != 9:
               sg.popup_error('Numer telefonu musi mieć dokładnie 9 cyfr')
               continue

            phone = f"{raw_phone[:3]}-{raw_phone[3:6]}-{raw_phone[6:]}"
            password = values['-PASSWORD-']
            if not 5 <= len(password) <= 10:
                sg.popup_error('Hasło musi mieć od 5 do 10 znaków')
                continue

            conf_passowrd = values['-CONFIRM-PASSWORD-']
            if password != conf_passowrd:
               sg.popup_error('Hasła nie są takie same')
               continue
            
            if not all([user_name,name,surname, email, phone,date_of_birth,gender,street,city,country, password]):
                sg.popup_error('Uzupełnij wszystkie pola')
                continue
                
            try:
                add_customer(user_name,name,surname, email, phone,date_of_birth,gender,street,city,country, password)
                sg.popup_ok('Klient został dodany')
                break
            except Exception as e:
                sg.popup_error(f'Błąd dodawania klienta: {e}')
    
    window.close()

def validate_user_login(username, password):
    import csv
    if not os.path.exists(CUSTOMERS_FILE):
        return False
    with open(CUSTOMERS_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['USER_NAME'] == username and row['PASSWORD'] == password:
                return True
    return False