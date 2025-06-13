"""
Moduł GUI do zarządzania lekami z wykorzystaniem PySimpleGUI.

Zawiera funkcje do:
- wczytywania leków z pliku Excel (drugs.xlsx),
- wyświetlania okna listy leków z możliwością wyszukiwania, dodawania, edytowania, usuwania i zamawiania,
- obsługi formularzy dodawania, edycji i zamówienia leku.

Moduł korzysta z klasy DrugDatabase do operacji na bazie leków oraz funkcji add_purchase_to_customer_file do zapisywania zamówień klienta.
"""
import PySimpleGUI as sg
import os
import pandas as pd
from Add_del_drug import DrugDatabase
from add_purchase_to_customer_file import add_purchase_to_customer_file
DRUGS_FILE = "drugs.xlsx"
from layout_utils import center_layout

db = DrugDatabase()

def load_drugs(filter_query=''):
    """
    Wczytuje listę leków z pliku drugs.xlsx, opcjonalnie filtrując wyniki.

    Parametry:
    filter_query (str): opcjonalny ciąg znaków do filtrowania leków po ID lub nazwie (ignoruje wielkość liter).

    Zwraca:
    list: lista leków jako listy wartości (ID, nazwa, na receptę, ilość, data dodania, numer recepty, cena).

    W przypadku błędu wyświetla popup z informacją o błędzie i zwraca pustą listę.
    """
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
    """
    Wyświetla okno z listą leków w formie tabeli z opcjami wyszukiwania, dodawania, edycji, usuwania i zamawiania.

    Parametry:
    user_mode (bool): jeśli True, ukrywa przyciski dodawania, edycji i usuwania (tryb użytkownika).
    client_id (str): identyfikator klienta, wykorzystywany przy składaniu zamówienia.

    Funkcja blokuje dalsze wykonywanie aż do zamknięcia okna.
    """
    input_style = {
        'font': ('Segoe UI', 14),
        'size': (40, 1),
        'background_color': '#F0F0F0',
        'text_color': 'black',
        'border_width': 2,
    }

    layout = [
        [sg.Text('Lista leków', font=('Segoe UI', 24), background_color='white')],
        [sg.Text('Wyszukaj:', font=('Segoe UI', 14), background_color='white'),
         sg.Input(key='-SEARCH-', **input_style),
         sg.Button('Szukaj', button_color=('white', '#6BCB77'), font=('Segoe UI', 12)),
         sg.Button('Pokaż wszystko', button_color=('white', '#6BCB77'), font=('Segoe UI', 12))],
        [sg.Table(
            values=[],
            headings=['ID', 'Nazwa', 'Na receptę', 'Ilość', 'Data dodania', 'Numer recepty', 'Cena'],
            key='-TABLE-',
            auto_size_columns=False,
            col_widths=[6, 25, 10, 8, 15, 15, 8],
            justification='center',
            num_rows=15,
            font=('Segoe UI', 12),
            background_color='white',
            text_color='black',
            header_background_color='#6BCB77',
            header_text_color='white',
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            enable_click_events=True
        )],
        [*([
            sg.Button('Dodaj lek', button_color=('white', '#6BCB77'), size=(20, 2), font=('Segoe UI', 14)),
            sg.Button('Edytuj', button_color=('white', '#89CFF0'), size=(20, 2), font=('Segoe UI', 14)),
            sg.Button('Usuń', button_color=('white', '#FF6B6B'), size=(20, 2), font=('Segoe UI', 14)),
        ] if not user_mode else []),
         sg.Button('Zamów', button_color=('white', '#800080'), size=(20, 2), font=('Segoe UI', 14)),
         sg.Button('Zamknij', button_color=('black', '#D3D3D3'), size=(20, 2), font=('Segoe UI', 14))]
    ]

    window = sg.Window('Lista leków', center_layout(layout), background_color='white',
                     size=(1200, 900), element_justification='center', finalize=True)


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
    """
    Wyświetla okno dialogowe pozwalające dodać nowy lek do bazy danych.

    Umożliwia podanie nazwy, informacji o recepturze, liczby opakowań oraz ceny.
    Waliduje dane wejściowe i wyświetla komunikaty o błędach w razie potrzeby.

    Po poprawnym dodaniu leku okno zamyka się.
    """
    input_style = {
        'font': ('Segoe UI', 14),
        'size': (40, 1),
        'background_color': '#F0F0F0',
        'text_color': 'black',
        'border_width': 2
    }

    layout = [
        [sg.Text('Dodaj lek', font=('Segoe UI', 24), background_color='white', pad=((0, 0), (20, 20)))],

        [sg.Text('Nazwa leku:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Input(key='-DRUG-', **input_style)],

        [sg.Text('Na receptę:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Combo(['YES', 'NO'], default_value='NO', key='-RECEPT-', font=('Segoe UI', 14), size=(10, 1),
                  enable_events=True)],

        [sg.Column([
            [sg.Text('ID recepty:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
             sg.Input(key='-RECEPT-ID-', size=(20, 1), font=('Segoe UI', 14),
                      background_color='#F0F0F0', text_color='black', border_width=2)]
        ], key='-RECEPT-ROW-', visible=False, background_color='white', pad=((20, 0), (10, 20)))],

        [sg.Text('Liczba opakowań:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Input(key='-PACKAGES-', size=(20, 1), font=('Segoe UI', 14),
                  background_color='#F0F0F0', text_color='black', border_width=2, pad=((0, 0), (0, 20)))],

        [sg.Text('Cena:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Input(key='-PRICE-', size=(20, 1), font=('Segoe UI', 14),
                  background_color='#F0F0F0', text_color='black', border_width=2)],

        [sg.HorizontalSeparator(color='#6BCB77', pad=((0, 0), (20, 20)))],

        [sg.Button('Dodaj', button_color=('white', '#6BCB77'), size=(20, 2), font=('Segoe UI', 14)),
         sg.Button('Anuluj', button_color=('black', '#D3D3D3'), size=(20, 2), font=('Segoe UI', 14), pad=((20, 0), 0))]
    ]

    window = sg.Window('Dodaj lek', center_layout(layout), background_color='white', size=(1200, 900), element_justification='center', finalize=True)

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
    """
    Wyświetla okno dialogowe do edycji danych wybranego leku.

    Parametry:
    row (list): lista wartości leku w formacie [ID, nazwa, na receptę, ilość, data dodania, numer recepty, cena].

    Pozwala zmodyfikować nazwę, receptę, liczbę opakowań, numer recepty i cenę.
    Po zapisaniu zmian aktualizuje bazę danych.

    Waliduje dane i informuje o błędach.
    """
    drug_id, drug_name, recept, packages, created, recept_id, price = row

    input_style = {
        'font': ('Segoe UI', 14),
        'size': (40, 1),
        'background_color': '#F0F0F0',
        'text_color': 'black',
        'border_width': 2,
        'pad': (0, 10)
    }

    layout = [
        [sg.Text('Edytuj lek', font=('Segoe UI', 24), background_color='white', pad=((0, 0), (20, 20)))],

        [sg.Text('Nazwa leku:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Input(drug_name, key='-DRUG-', **input_style)],

        [sg.Text('Na receptę:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Combo(['YES', 'NO'], default_value=recept, key='-RECEPT-', font=('Segoe UI', 14), size=(10, 1),
                  enable_events=True, pad=(0, 10))],

        [sg.Column([
            [sg.Text('ID recepty:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
             sg.Input(recept_id if recept_id != 'None' else '', key='-RECEPT-ID-', font=('Segoe UI', 14),
                      size=(20, 1), background_color='#F0F0F0', text_color='black', border_width=2)]
        ], key='-RECEPT-ROW-', visible=(recept == 'YES'), background_color='white', pad=((0, 0), (0, 20)))],

        [sg.Text('Liczba opakowań:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Input(packages, key='-PACKAGES-', **input_style)],

        [sg.Text('Cena:', font=('Segoe UI', 14), background_color='white', size=(20, 1)),
         sg.Input(price, key='-PRICE-', **input_style)],

        [sg.HorizontalSeparator(color='#6BCB77', pad=((0, 0), (20, 20)))],

        [sg.Button('Zapisz', button_color=('white', '#6BCB77'), size=(20, 2), font=('Segoe UI', 14)),
         sg.Button('Anuluj', button_color=('black', '#D3D3D3'), size=(20, 2), font=('Segoe UI', 14), pad=((20, 0), 0))]
    ]

    window = sg.Window(f'Edycja leku ID: {drug_id}', center_layout(layout), background_color='white', size=(1200, 900), element_justification='center', finalize=True
    )

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
    """
    Wyświetla okno dialogowe umożliwiające złożenie zamówienia na wybrany lek.

    Parametry:
    row (list): lista wartości leku w formacie [ID, nazwa, na receptę, ilość, data dodania, numer recepty, cena].
    client_id (str): identyfikator klienta składającego zamówienie.

    Umożliwia podanie liczby zamawianych opakowań, waliduje dane i zapisuje zamówienie do pliku klienta.
    """
    drug_id, drug_name, recept, packages, created, recept_id, price = row

    input_style = {
        'font': ('Segoe UI', 14),
        'size': (20, 1),
        'background_color': '#F0F0F0',
        'text_color': 'black',
        'border_width': 2,
        'pad': (0, 10)
    }

    layout = [
        [sg.Text(f'Zamów lek: {drug_name}', font=('Segoe UI', 24), background_color='white', pad=((0,0),(20,20)))],

        [sg.Text('Ilość do zamówienia:', font=('Segoe UI', 14), background_color='white', size=(20,1)),
         sg.Input(key='-QTY-', **input_style)],

        [sg.HorizontalSeparator(color='#6BCB77', pad=((0,0),(20,20)))],

        [sg.Button('Zamów', button_color=('white', '#6BCB77'), size=(20, 2), font=('Segoe UI', 14)),
         sg.Button('Anuluj', button_color=('black', '#D3D3D3'), size=(20, 2), font=('Segoe UI', 14), pad=((20,0),0))]
    ]

    window = sg.Window('Zamów lek', center_layout(layout), background_color='white', size=(600, 300), element_justification='center', finalize=True)


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
