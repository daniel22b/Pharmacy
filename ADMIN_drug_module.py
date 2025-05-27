import PySimpleGUI as sg
import os
import pandas as pd
from Add_del_drug import add_drug, remove_drug
DRUGS_FILE = "drugs.xlsx"

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
                 headings=['ID', 'Nazwa', 'Na receptę', 'Ilość', 'Data dodania','Numer recepty'],
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
        
        if event is None or event == 'Zamknij':
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
    layout = [
        [sg.T('Dodaj lek', font=('Helvetica', 16))],
        [sg.T('Nazwa leku:'), sg.I(key='-DRUG-')],
        [sg.T('Na receptę:'), 
         sg.Combo(['YES', 'NO'], default_value='NO', key='-RECEPT-', enable_events=True)],
        [sg.Column([
            [sg.T('ID recepty:'), sg.I(key='-RECEPT-ID-', size=(10, 1))]
        ], key='-RECEPT-ROW-', visible=False)],
        [sg.T('Liczba opakowań:'), sg.I(key='-PACKAGES-', size=(10, 1))],
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
            
            if not all([drug_name, recept, packages]):
                sg.popup_error('Uzupełnij wszystkie pola')
                continue
            
            if recept == 'YES' and not recept_id:
                sg.popup_error('Podaj ID recepty dla leku')
                continue

            try:
                packages = int(packages)
                if packages <= 0:
                    raise ValueError("Liczba opakowań musi być większa od 0")
                    
                add_drug(drug_name, recept, packages, recept_id)
                sg.popup_ok('Lek został dodany')
                break
            except ValueError as e:
                sg.popup_error(f'Nieprawidłowa liczba opakowań: {e}')
            except Exception as e:
                sg.popup_error(f'Błąd dodawania leku: {e}')
    
    window.close()
