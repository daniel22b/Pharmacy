"""
Moduł odpowiedzialny za zarządzanie klientami apteki.

Zawiera funkcje do:
- wczytywania listy klientów z pliku CSV,
- wyświetlania listy klientów w oknie GUI,
- rejestracji nowego klienta,
- weryfikacji poprawności danych logowania klientów.
"""
import PySimpleGUI as sg
import os
import pandas as pd
from Add_del_customer import add_customer,remove_customer
from layout_utils import input_style, center_layout, white_push

ADRESS_FILE = "address.csv"
CUSTOMERS_FILE = "customers.csv"

def load_customers(filter_query=''):
    """
    Wczytuje listę klientów z pliku CSV i filtruje według zapytania.

    Args:
        filter_query (str): Tekst filtrowania listy klientów (opcjonalny).

    Returns:
        list: Lista klientów jako lista list (wierszy), gdzie każdy wiersz
              zawiera pola: ID, NAME, SURNAME, E-MAIL, PHONE, CREATED, AGE, GENDER.

    Raises:
        Pokazuje okno błędu, jeśli plik nie może zostać wczytany.
    """
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
    """
    Wyświetla okno GUI z listą klientów oraz opcjami:
    - wyszukiwania klientów,
    - dodawania nowego klienta,
    - usuwania zaznaczonego klienta,
    - zamknięcia okna.

    Obsługuje interakcje użytkownika oraz aktualizuje tabelę klientów na żywo.
    """
    layout = [
        [sg.Text('Lista klientów', font=('Segoe UI', 24), background_color='white')],
        [sg.Text('Wyszukaj:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-SEARCH-', **input_style),
         sg.Button('Szukaj', button_color=('white', '#6BCB77'), font=('Segoe UI', 12)),
         sg.Button('Pokaż wszystko', button_color=('white', '#6BCB77'), font=('Segoe UI', 12))],
        [sg.Table(
            values=[],
            headings=["ID", "NAME", "SURNAME", "E-MAIL", "PHONE", "CREATED", "AGE", "GENDER"],
            key='-TABLE-',
            auto_size_columns=False,
            col_widths=[5, 15, 15, 25, 15, 15, 5, 10],
            justification='center',
            num_rows=20,
            font=('Segoe UI', 12),
            background_color='white',
            text_color='black',
            header_background_color='#6BCB77',
            header_text_color='white',
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            enable_click_events=True
        )],
        [sg.Button('Dodaj klienta', button_color=('white', '#6BCB77'), size=(20, 2), font=('Segoe UI', 12)),
         sg.Button('Usuń zaznaczony', button_color=('white', '#FF6B6B'), size=(20, 2), font=('Segoe UI', 12)),
         sg.Button('Zamknij', button_color=('black', '#D3D3D3'), size=(20, 2), font=('Segoe UI', 12))]
    ]

    window = sg.Window('Lista klientów', center_layout(layout), background_color='white',
                     size=(1200, 900), element_justification='center', finalize=True)

    
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
#==========================================================================


def show_register_customers_window():
    """
    Wyświetla okno GUI do rejestracji nowego klienta.

    Zbiera dane klienta (imię, nazwisko, email, telefon, hasło, itd.),
    waliduje je (poprawność emaila, długość hasła, spójność haseł, itp.),
    a następnie zapisuje nowego klienta do pliku CSV.

    Informuje użytkownika o powodzeniu lub błędach podczas rejestracji.
    """
    input_style = {
        'font': ('Segoe UI', 14),
        'size': (40, 1),
        'background_color': '#F0F0F0',
        'text_color': 'black',
        'border_width': 2,
        'focus': False
    }

    layout = [
        [sg.Text('Dodaj klienta', font=('Segoe UI', 24), background_color='white')],
        [sg.Text('Email:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-EMAIL-', **input_style)],
        [sg.Text('Nazwa użytkownika:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-USERNAME-', **input_style)],
        [sg.Text('Hasło:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-PASSWORD-', password_char='*', **input_style)],
        [sg.Text('Potwierdź hasło:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-CONFIRM-PASSWORD-', password_char='*', **input_style)],
        [sg.Text('Imię:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-NAME-', **input_style)],
        [sg.Text('Nazwisko:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-SRNAME-', **input_style)],
        [sg.Text('Telefon:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-PHONE-', **input_style)],
        [sg.Text('Data urodzenia:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-DOB-', **input_style)],
        [sg.Text('Ulica:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-STREET-', **input_style)],
        [sg.Text('Miasto:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-CITY-', **input_style)],
        [sg.Text('Kraj:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-COUNTRY-', **input_style)],
        [sg.Text('Płeć:', font=('Segoe UI', 14), background_color='white'),
         sg.Combo(['Kobieta', 'Mężczyzna'], default_value='Kobieta', key='-GENDER-', font=('Segoe UI', 14), size=(20, 1))],
        [sg.Button('Dodaj', button_color=('white', '#6BCB77'), size=(20, 2), font=('Segoe UI', 14)),
         sg.Button('Anuluj', button_color=('black', '#D3D3D3'), size=(20, 2), font=('Segoe UI', 14))]
    ]

    window = sg.Window('Dodaj klienta', center_layout(layout), background_color='white',
                     size=(1200, 900), element_justification='center', finalize=True)



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
            city = values['-CITY-'].capitalize()
            country = values['-COUNTRY-'].capitalize()
            raw_phone = values['-PHONE-']
            street = "Ul. " + values['-STREET-'].strip()
          

            email = values['-EMAIL-']
            if '@' not in email or '.' not in email:
                sg.popup_error('Nieprawidłowy format e-mail.')
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
    """
    Weryfikuje poprawność danych logowania użytkownika na podstawie pliku CSV.

    Args:
        username (str): Nazwa użytkownika.
        password (str): Hasło użytkownika.

    Returns:
        bool: True, jeśli login i hasło są poprawne, False w przeciwnym wypadku.
    """
    import csv
    if not os.path.exists(CUSTOMERS_FILE):
        return False
    with open(CUSTOMERS_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['USER_NAME'] == username and row['PASSWORD'] == password:
                return True
    return False

