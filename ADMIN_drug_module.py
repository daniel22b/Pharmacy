import PySimpleGUI as sg
import os
import pandas as pd
from Add_del_drug import DrugDatabase
from add_purchase_to_customer_file import add_purchase_to_customer_file

DRUGS_FILE = "drugs.xlsx"

db = DrugDatabase()

def load_drugs(filter_query=''):
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
    table_data = load_drugs()
    headings = ['ID', 'Nazwa', 'Na receptę', 'Ilość', 'Data dodania', 'Numer recepty']

    layout = [
        [sg.Text('Lista leków', font=('Helvetica', 20), text_color='white', background_color='#2B2B2B')],
        [sg.Text('Wyszukaj:', background_color='#2B2B2B', text_color='white'),
         sg.Input(key='-SEARCH-', size=(30, 1)),
         sg.Button('Szukaj', button_color=('white', 'green')),
         sg.Button('Pokaż wszystko', button_color=('white', 'green'))],
        [sg.Table(values=table_data,
                  headings=headings,
                  key='-TABLE-',
                  auto_size_columns=False,
                  col_widths=[5, 20, 10, 6, 12, 15],
                  justification='center',
                  num_rows=15,
                  row_height=25,
                  background_color='#1E1E1E',
                  text_color='white',
                  header_background_color='#00A86B',
                  header_text_color='white',
                  alternating_row_color='#2E2E2E',
                  font=('Helvetica', 11),
                  expand_x=True,
                  expand_y=True,
                  enable_click_events=True,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Column([
            [
                *([sg.Button('Dodaj lek', button_color=('white', 'green')),
                   sg.Button('Edytuj', button_color=('white', 'blue')),
                   sg.Button('Usuń', button_color=('white', 'red'))] if not user_mode else []),
                sg.Button('Zamów', button_color=('white', 'purple')),
                sg.Button('Zamknij', button_color=('white', 'gray'))
            ]
        ], element_justification='center', expand_x=True)]
    ]

    window = sg.Window('Lista leków (Administrator)', layout, finalize=True, background_color='#2B2B2B', resizable=True)

    while True:
        event, values = window.read()

        if event in (None, 'Zamknij'):
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

def order_drug_window(drug, client_id):
    layout = [
        [sg.Text(f"Zamawianie leku: {drug[1]}", font=("Helvetica", 14))],
        [sg.Text("Podaj ilość do zamówienia:"), sg.Input(key='-QTY-', size=(10, 1))],
        [sg.Button("Zamów"), sg.Button("Anuluj")]
    ]

    window = sg.Window("Zamów lek", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Anuluj"):
            break
        elif event == "Zamów":
            try:
                qty_int = int(values['-QTY-'])
                if qty_int <= 0:
                    sg.popup_error("Podaj dodatnią liczbę.")
                    continue
                db.order_drug(drug[0], qty_int)  # Zwiększ ilość w magazynie
                sg.popup("Zamówienie zrealizowane. Ilość leku w magazynie została zwiększona.")
                break
            except ValueError:
                sg.popup_error("Wprowadź poprawną liczbę.")
    window.close()
