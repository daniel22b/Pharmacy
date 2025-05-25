import PySimpleGUI as sg
import pandas as pd
from Add_del_drug import add_drug, remove_drug
from customer import add_customer
import os

# Constants
CORRECT_PIN = "1"
DRUGS_FILE = "drugs.xlsx"

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
            [sg.B('Zarejestruj klienta', size=(20, 2), button_color=('white', 'green'))],
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
            
        if event == 'Zarejestruj klienta':
            window.hide()
            show_registration_window()
            window.un_hide()
            
        if event == 'Lista leków':
            window.hide()
            show_drug_list_window()
            window.un_hide()
    
    window.close()

def show_registration_window():
    """Show customer registration window"""
    layout = [
        [sg.T('Rejestracja klienta', font=('Helvetica', 16))],
        [sg.T('Imię i nazwisko:'), sg.I(key='-NAME-')],
        [sg.T('Email:'), sg.I(key='-EMAIL-')],
        [sg.T('Telefon:'), sg.I(key='-PHONE-')],
        [sg.T('Gender:'), 
         sg.Combo(['MALE', 'FEMALE'], default_value='MALE', key='-GENDER-')],
        [sg.T('Date of birth:'), sg.I(key='-DATE_OF_BIRTH-')],
        [sg.T('Street:'), sg.I(key='-STREET-')],
        [sg.T('City:'), sg.I(key='-CITY-')],
        [sg.T('Country:'), sg.I(key='-COUNTRY-')],
        [sg.B('Zarejestruj', button_color=('white', 'green')), 
         sg.B('Anuluj', button_color=('white', 'gray'))]
    ]
    
    window = sg.Window('Rejestracja', layout, background_color='#2B2B2B')
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Anuluj'):
            break
            
        if event == 'Zarejestruj':
            name = values['-NAME-'].strip()
            email = values['-EMAIL-'].strip()
            phone = values['-PHONE-'].strip()
            gender = values['-GENDER-'].strip()
            date_of_birth = values['-DATE_OF_BIRTH-'].strip()
            street = values['-STREET-'].strip()
            city = values['-CITY-'].strip()
            country = values['-COUNTRY-'].strip()

            
            if not all([name, email, phone,date_of_birth,gender]):
                sg.popup_error('Uzupełnij wszystkie pola')
                continue
                
            try:
                customer_id = add_customer(name, email, phone, date_of_birth,gender,street,city,country)
                print(f'Klient został dodany z ID: {customer_id}')
                sg.popup_ok(f'Klient został dodany z ID: {customer_id}')
                break
            except Exception as e:
                sg.popup_error(f'Nie udało się dodać klienta: {e}')
    
    window.close()

def load_drugs(filter_query=''):
    """Load drugs from Excel file with optional filtering"""
    try:
        if not os.path.exists(DRUGS_FILE):
            return []
            
        df_raw = pd.read_excel(DRUGS_FILE, header=None)
        if df_raw.empty:
            return []
            
        header = df_raw.iloc[0, 0].split(",")
        df = df_raw.iloc[1:, 0].str.split(",", expand=True)
        df.columns = header
        
        if filter_query:
            query = filter_query.lower()
            df = df[df.apply(
                lambda row: query in str(row["ID"]).lower() or query in str(row["DRUG"]).lower(),
                axis=1
            )]
        
        return df.values.tolist()
    except Exception as e:
        sg.popup_error(f'Nie można wczytać danych: {e}')
        return []

def show_drug_list_window():
    """Show drug list window with management options"""
    # Create the layout
    layout = [
        [sg.T('Lista leków', font=('Helvetica', 16))],
        [sg.T('Wyszukaj:'), 
         sg.I(key='-SEARCH-', size=(30, 1)),
         sg.B('Szukaj', button_color=('white', 'green')),
         sg.B('Pokaż wszystko', button_color=('white', 'green'))],
        [sg.Table(values=[], 
                 headings=['ID', 'Nazwa', 'Na receptę', 'Ilość', 'Data'],
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
        [sg.B('Dodaj lek', button_color=('white', 'green')), 
         sg.B('Usuń zaznaczony', button_color=('white', 'red')),
         sg.B('Zamknij', button_color=('white', 'gray'))]
    ]
    
    window = sg.Window('Lista leków', layout, finalize=True, background_color='#2B2B2B')
    
    # Initial load
    table_data = load_drugs()
    window['-TABLE-'].update(table_data)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Zamknij'):
            break
            
        if event == 'Szukaj':
            table_data = load_drugs(values['-SEARCH-'])
            window['-TABLE-'].update(table_data)
            
        if event == 'Pokaż wszystko':
            table_data = load_drugs()
            window['-TABLE-'].update(table_data)
            
        if event == 'Dodaj lek':
            show_add_drug_window()
            table_data = load_drugs()
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
                if sg.popup_yes_no(f'Czy na pewno chcesz usunąć lek "{row[1]}" (ID: {row[0]})?') == 'Yes':
                    remove_drug(row[0])
                    sg.popup_ok(f'Lek "{row[1]}" (ID: {row[0]}) został usunięty')
                    table_data = load_drugs()
                    window['-TABLE-'].update(table_data)
            except Exception as e:
                sg.popup_error(f'Nie udało się usunąć leku: {e}')
    
    window.close()

def show_add_drug_window():
    """Show window for adding new drugs"""
    layout = [
        [sg.T('Dodaj lek', font=('Helvetica', 16))],
        [sg.T('Nazwa leku:'), sg.I(key='-DRUG-')],
        [sg.T('Na receptę:'), 
         sg.Combo(['YES', 'NO'], default_value='YES', key='-RECEPT-')],
        [sg.T('Liczba opakowań:'), 
         sg.I(key='-PACKAGES-', size=(10, 1))],
        [sg.B('Dodaj', button_color=('white', 'green')), 
         sg.B('Anuluj', button_color=('white', 'gray'))]
    ]
    
    window = sg.Window('Dodaj lek', layout, background_color='#2B2B2B')
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Anuluj'):
            break
            
        if event == 'Dodaj':
            drug_name = values['-DRUG-'].strip()
            recept = values['-RECEPT-']
            packages = values['-PACKAGES-'].strip()
            
            if not all([drug_name, recept, packages]):
                sg.popup_error('Uzupełnij wszystkie pola')
                continue
                
            try:
                packages = int(packages)
                if packages <= 0:
                    raise ValueError("Liczba opakowań musi być większa od 0")
                    
                add_drug(drug_name, recept, packages)
                sg.popup_ok('Lek został dodany')
                break
            except ValueError as e:
                sg.popup_error(f'Nieprawidłowa liczba opakowań: {e}')
            except Exception as e:
                sg.popup_error(f'Błąd dodawania leku: {e}')
    
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