import PySimpleGUI as sg
import os
import pandas as pd
from Add_del_drug import DrugDatabase
from add_purchase_to_customer_file import add_purchase_to_customer_file
DRUGS_FILE = "drugs.xlsx"

db = DrugDatabase()

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
                
        if len(header) != df.shape[1]:
            raise ValueError(f"Niezgodność liczby kolumn: nagłówki={len(header)}, dane={df.shape[1]}")
        
        df.columns = header
        
        if filter_query:
            query = filter_query.lower()
            df = df[df.apply(
                lambda row: query in str(row["ID"]) or query in str(row["DRUG"]).lower(),
                axis=1
            )]
        
        return df.values.tolist()
    except Exception as e:
        sg.popup_error(f'Nie można wczytać danych: {e}')
        return []

def show_drug_list_window(user_mode=False, client_id=None):
    """Show drug list window with management options"""
    # Create the layout
    layout = [
        [sg.T('Lista leków', font=('Helvetica', 16))],
        [sg.T('Wyszukaj:'), 
         sg.I(key='-SEARCH-', size=(30, 1)),
         sg.B('Szukaj', button_color=('white', 'green')),
         sg.B('Pokaż wszystko', button_color=('white', 'green'))],
        [sg.Table(values=[], 
                 headings=['ID', 'Nazwa', 'Na receptę', 'Ilość', 'Data dodania','Numer recepty','Cena'],
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
        [
            *([
                  sg.B('Dodaj lek', button_color=('white', 'green')),
                  sg.B('Edytuj', button_color=('white', 'blue')),
                  sg.B('Usuń', button_color=('white', 'red')),
              ] if not user_mode else []),
         sg.B('Zamów', button_color=('white', 'purple')),
         sg.B('Zamknij', button_color=('white', 'gray'))]
         
    ]
    
    window = sg.Window('Lista leków', layout, finalize=True, background_color='#2B2B2B')
    
    # Initial load
    table_data = load_drugs()
    window['-TABLE-'].update(table_data)
    
    while True:
        event, values = window.read()
        
        if event is None or event == 'Zamknij':
            break
            
        if event == 'Szukaj':
            table_data = load_drugs(values['-SEARCH-'])
            window['-TABLE-'].update(table_data)
            
        if event == 'Pokaż wszystko':
            table_data = load_drugs()
            window['-TABLE-'].update(table_data)
            
        if event == 'Dodaj lek' and not user_mode:
            show_add_drug_window()
            table_data = load_drugs()
            window['-TABLE-'].update(table_data)

        if event == 'Edytuj' and not user_mode:
            selected = values['-TABLE-']
            if not selected:
                sg.popup_error('Wybierz rekord')
                continue
            row = table_data[selected[0]]
            show_edit_drug_window(row)
            table_data = load_drugs()
            window['-TABLE-'].update(table_data)
        
        if event == 'Zamów':
            selected = values['-TABLE-']
            if not selected:
                sg.popup_error('Wybierz rekord')
                continue
            row = table_data[selected[0]]
            order_drug_window(row, client_id)
            table_data = load_drugs()
            window['-TABLE-'].update(table_data)


        if event == 'Usuń' and not user_mode:
            selected = values['-TABLE-']
            if not selected:
                sg.popup_error('Wybierz rekord')
                continue
            row = table_data[selected[0]]
            if sg.popup_yes_no(f'Czy na pewno chcesz usunąć lek "{row[1]}" (ID: {row[0]})?') == 'Yes':
                try:
                    db.remove_drug(row[0])
                    sg.popup_ok(f'Lek "{row[1]}" (ID: {row[0]}) został usunięty')
                    table_data = load_drugs()
                    window['-TABLE-'].update(table_data)
                except Exception as e:
                        sg.popup_error(f'Nie udało się usunąć leku: {e}')
    window.close()

def show_add_drug_window():
    layout = [
        [sg.T('Dodaj lek', font=('Helvetica', 16))],
        [sg.T('Nazwa leku:'), sg.I(key='-DRUG-')],
        [sg.T('Na receptę:'), 
         sg.Combo(['YES', 'NO'], default_value='NO', key='-RECEPT-', enable_events=True)],
        [sg.Column([
            [sg.T('ID recepty:'), sg.I(key='-RECEPT-ID-', size=(10, 1))]
        ], key='-RECEPT-ROW-', visible=False)],
        [sg.T('Liczba opakowań:'), sg.I(key='-PACKAGES-', size=(10, 1))],
        [sg.T('Cena:'), sg.I(key='-PRICE-', size=(10,1))],
        [sg.B('Dodaj', button_color=('white', 'green')), 
         sg.B('Anuluj', button_color=('white', 'gray'))]
    ]
    
    window = sg.Window('Dodaj lek', layout, background_color='#2B2B2B', finalize=True)
    
    while True:
        event, values = window.read()
        
        if event is None or event == 'Anuluj':
            break
            
        if event == '-RECEPT-':
            window['-RECEPT-ROW-'].update(visible=(values['-RECEPT-'] == 'YES'))

        if event == 'Dodaj':
            drug_name = values['-DRUG-'].strip()
            recept = values['-RECEPT-']
            packages = values['-PACKAGES-'].strip()
            recept_id = values['-RECEPT-ID-'].strip() if recept == 'YES' else None
            price = values['-PRICE-'].strip()
            if not all([drug_name, recept, packages,price]):
                sg.popup_error('Uzupełnij wszystkie pola')
                continue
            
            if recept == 'YES' and not recept_id:
                sg.popup_error('Podaj ID recepty dla leku')
                continue

            try:
                packages = int(packages)
                if packages <= 0:
                    raise ValueError("Liczba opakowań musi być większa od 0")
                    
                db.add_drug(drug_name, recept, packages, recept_id,price)
                sg.popup_ok('Lek został dodany')
                break
            except ValueError as e:
                sg.popup_error(f'Nieprawidłowa liczba opakowań: {e}')
            except Exception as e:
                sg.popup_error(f'Błąd dodawania leku: {e}')
    
    window.close()

def show_edit_drug_window(row):
    drug_id, drug_name, recept, packages,created, recept_id,price = row
    
    layout = [
        [sg.T('Edytuj lek', font=('Helvetica', 16))],
        [sg.T('Nazwa leku:'), sg.I(drug_name, key='-DRUG-')],
        [sg.T('Na receptę:'), 
         sg.Combo(['YES', 'NO'], default_value=recept, key='-RECEPT-', enable_events=True)],
        [sg.Column([
            [sg.T('ID recepty:'), sg.I(recept_id if recept_id != 'None' else '', key='-RECEPT-ID-')]
        ], key='-RECEPT-ROW-', visible=(recept == 'YES'))],
        [sg.T('Liczba opakowań:'), sg.I(packages, key='-PACKAGES-')],
        [sg.T('Cena:'), sg.I(price, key='-PRICE-', size=(10,1))],
        [sg.B('Zapisz', button_color=('white', 'green')), 
         sg.B('Anuluj', button_color=('white', 'gray'))]
    ]
    
    window = sg.Window(f'Edycja leku ID: {drug_id}', layout, background_color='#2B2B2B', finalize=True)

    while True:
        event, values = window.read()
        if event is None or event == 'Anuluj':
            break

        if event == '-RECEPT-':
            window['-RECEPT-ROW-'].update(visible=(values['-RECEPT-'] == 'YES'))

        if event == 'Zapisz':
            drug_name = values['-DRUG-'].strip()
            recept = values['-RECEPT-']
            packages = values['-PACKAGES-'].strip()
            recept_id = values['-RECEPT-ID-'].strip() if recept == 'YES' else None
            price = values['-PRICE-'].strip()
            if not all([drug_name, recept, packages,price]):
                sg.popup_error('Uzupełnij wszystkie pola')
                continue

            if recept == 'YES' and not recept_id:
                sg.popup_error('Podaj ID recepty dla leku')
                continue

            try:
                packages = int(packages)
                if packages <= 0:
                    raise ValueError("Liczba opakowań musi być większa od 0")

                db.remove_drug(drug_id)
                db.add_drug(drug_name, recept, packages, recept_id,price)
                sg.popup_ok('Dane leku zostały zaktualizowane')
                break
            except Exception as e:
                sg.popup_error(f'Błąd edycji: {e}')
    window.close()

def order_drug_window(row, client_id):
    drug_id, drug_name, recept, packages, created, recept_id,price = row

    layout = [
        [sg.T(f'Zamów lek: {drug_name}', font=('Helvetica', 16))],
        [sg.T('Ilość do zamówienia:'), sg.I(key='-QTY-', size=(10, 1))],
        [sg.B('Zamów', button_color=('white', 'green')),
         sg.B('Anuluj', button_color=('white', 'gray'))]
    ]

    window = sg.Window('Zamów lek', layout, background_color='#2B2B2B', finalize=True)

    while True:
        event, values = window.read()
        if event is None or event == 'Anuluj':
            break

        if event == 'Zamów':
            qty = values['-QTY-'].strip()
            if not qty.isdigit() or int(qty) <= 0:
                sg.popup_error('Podaj prawidłową dodatnią liczbę')
                continue

            try:
                qty_int = int(qty)
                db.order_drug(drug_id, qty_int)
                add_purchase_to_customer_file(client_id, drug_name, int(qty))
                sg.popup_ok(f'Zamówiono {qty_int} sztuk leku "{drug_name}"')
                break
            except Exception as e:
                sg.popup_error(f'Błąd zamówienia: {e}')
    
    window.close()
