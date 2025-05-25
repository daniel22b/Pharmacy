import PySimpleGUI as sg
import os
import pandas as pd


CUSTOMERS_FILE = "DATABASE/customers.csv"

def load_customers(filter_query=''):
    try:
        if not os.path.exists(CUSTOMERS_FILE):
            return []
            
        df = pd.read_csv(CUSTOMERS_FILE)
        if df.empty:
            return []
            
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
    """Show customers list window with management options"""
    # Create the layout
    layout = [
        [sg.T('Lista klientów', font=('Helvetica', 16))],
        [sg.T('Wyszukaj:'), 
         sg.I(key='-SEARCH-', size=(30, 1)),
         sg.B('Szukaj', button_color=('white', 'green')),
         sg.B('Pokaż wszystko', button_color=('white', 'green'))],
        [sg.Table(values=[], 
                 headings=['ID','NAME','E-MAIL','PHONE','CREATED','UPDATED','DATE_OF_BIRTH','GENDER'],
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
    
    # Initial load
    table_data = load_customers()
    window['-TABLE-'].update(table_data)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Zamknij'):
            break
            
        if event == 'Szukaj':
            table_data = load_customers(values['-SEARCH-'])
            window['-TABLE-'].update(table_data)
            
        if event == 'Pokaż wszystko':
            table_data = load_customers()
            window['-TABLE-'].update(table_data)
            
        if event == 'Dodaj klienta':
            # show_add_customers_window()
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
                if sg.popup_yes_no(f'Czy na pewno chcesz usunąć lek "{row[1]}" (ID: {row[0]})?') == 'Yes':
                    remove_customer(row[0])
                    sg.popup_ok(f'Klient "{row[1]}" (ID: {row[0]}) został usunięty')
                    # table_data = load_drugs()
                    window['-TABLE-'].update(table_data)
            except Exception as e:
                sg.popup_error(f'Nie udało się usunąć leku: {e}')
    
    window.close()

def remove_customer(customer_id):
    if not os.path.exists(CUSTOMERS_FILE):
        raise FileNotFoundError("Plik z klientami nie istnieje.")
    
    df = pd.read_csv(CUSTOMERS_FILE)
    df = df[df["ID"].astype(str) != str(customer_id)]
    df.to_csv(CUSTOMERS_FILE, index=False)
    
# def show_add_customers_window():
#     """Show window for adding new drugs"""
#     layout = [
#         [sg.T('Dodaj lek', font=('Helvetica', 16))],
#         [sg.T('Nazwa leku:'), sg.I(key='-DRUG-')],
#         [sg.T('Na receptę:'), 
#          sg.Combo(['YES', 'NO'], default_value='YES', key='-RECEPT-')],
#         [sg.T('Liczba opakowań:'), 
#          sg.I(key='-PACKAGES-', size=(10, 1))],
#         [sg.B('Dodaj', button_color=('white', 'green')), 
#          sg.B('Anuluj', button_color=('white', 'gray'))]
#     ]
    
#     window = sg.Window('Dodaj lek', layout, background_color='#2B2B2B')
    
#     while True:
#         event, values = window.read()
        
#         if event in (sg.WIN_CLOSED, 'Anuluj'):
#             break
            
#         if event == 'Dodaj':
#             drug_name = values['-DRUG-'].strip()
#             recept = values['-RECEPT-']
#             packages = values['-PACKAGES-'].strip()
            
#             if not all([drug_name, recept, packages]):
#                 sg.popup_error('Uzupełnij wszystkie pola')
#                 continue
                
#             try:
#                 packages = int(packages)
#                 if packages <= 0:
#                     raise ValueError("Liczba opakowań musi być większa od 0")
                    
#                 add_drug(drug_name, recept, packages)
#                 sg.popup_ok('Lek został dodany')
#                 break
#             except ValueError as e:
#                 sg.popup_error(f'Nieprawidłowa liczba opakowań: {e}')
#             except Exception as e:
#                 sg.popup_error(f'Błąd dodawania leku: {e}')
    
#     window.close()

