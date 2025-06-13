import PySimpleGUI as sg
import pandas as pd
import os
from Add_del_drug import DrugDatabase
from add_purchase_to_customer_file import add_purchase_to_customer_file
from Agent import agent_ai,query_gpt_and_find_medicine
from layout_utils import input_style, center_layout, white_push

DRUGS_FILE = "drugs.xlsx"
db = DrugDatabase()

def load_drugs(filter_query=''):
    try:
        if not os.path.exists(DRUGS_FILE):
            return []

        df_raw = pd.read_excel(DRUGS_FILE, header=None)
        if df_raw.empty:
            return []

        records = []
        header = None

        for i, row in df_raw.iterrows():
            line = str(row[0]).strip()
            parts = [p.strip() for p in line.split(',')]

            if i == 0:
                header = parts
                continue

            while len(parts) < len(header):
                parts.append("")

            if len(parts) != len(header):
                continue

            if filter_query:
                q = filter_query.lower()
                if q not in parts[0].lower() and q not in parts[1].lower():
                    continue

            records.append(parts)

        return records

    except Exception as e:
        sg.popup_error(f'Błąd wczytywania danych: {e}')
        return []

def show_user_drug_window(client_id):
    cart = []

    def update_cart_display(window):
        cart_items = [f"{item['name']} x{item['qty']} (Cena: {item.get('price', '0.00')*item['qty']} zł)" for item in cart]

        window['-CART-'].update(values=cart_items)

    layout = [
        [
            sg.VPush(),

            sg.Column([
                [sg.Text('Lista leków', font=('Segoe UI', 20, 'bold'), text_color='black', background_color='white',
                         pad=(0, 20))],

                [sg.Text('Szukaj:', background_color='white', text_color='black', font=('Segoe UI', 12)),
                 sg.Input(key='-SEARCH-', **input_style),
                 sg.Button('Szukaj', button_color=('white', '#6BCB77'), font=('Segoe UI', 12)),
                 sg.Button('Pokaż wszystko', button_color=('white', '#6BCB77'), font=('Segoe UI', 12))],

                [sg.Table(
                    values=[],
                    headings=['ID', 'Nazwa', 'Recepta', 'Cena'],
                    key='-TABLE-',
                    auto_size_columns=False,
                    col_widths=[8, 25, 10, 10],
                    justification='left',
                    num_rows=15,
                    enable_events=True,
                    font=('Segoe UI', 11),
                    background_color='white',
                    text_color='black',
                    header_background_color='#6BCB77',
                    header_text_color='white',
                    alternating_row_color='#F0F0F0',
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE
                )],

                [sg.Button('Dodaj do koszyka', button_color=('white', '#89CFF0'), font=('Segoe UI', 12)),
                 sg.Button('Kup teraz', button_color=('white', '#6BCB77'), font=('Segoe UI', 12)),
                 sg.Button('Zamknij', button_color=('white', '#FF6B6B'), font=('Segoe UI', 12))],

                [sg.Text('Koszyk:', font=('Segoe UI', 12, 'bold'), text_color='black', background_color='white',
                         pad=(0, 5))],
                [sg.Listbox(values=[], size=(50, 4), key='-CART-', font=('Segoe UI', 11),
                            background_color='lightgray', text_color='black')]
            ],
                element_justification='center',
                background_color='white',
                vertical_alignment='center'
            ),

            sg.VSeparator(),

            sg.Column([
                [sg.Text("Agent AI", font=('Segoe UI', 18, 'bold'), text_color='black', background_color='white',
                         pad=(0, 20))],

                [sg.Multiline(
                    "Dzień dobry! Jestem agentem AI.\nOpisz proszę swoje objawy, a postaram się dobrać odpowiedni lek.\n",
                    size=(50, 18), key='-CHAT-', disabled=True, font=('Segoe UI', 11),
                    background_color='lightgray', text_color='black', no_scrollbar=False)],

                [sg.Input(key='-INPUT-', **input_style)],

                [sg.Button("Wyślij do agenta", size=(50, 2), button_color=('white', '#89CFF0'), font=('Segoe UI', 12))]
            ],
                element_justification='center',
                background_color='white',
                vertical_alignment='top'
            ),

            sg.VPush()
        ]
    ]

    window = sg.Window('Użytkownik - Lista leków', layout, background_color='white', size=(1200, 900), finalize=True)

    table_data = load_drugs()
    table_display_data = [[row[0], row[1],row[2], row[6]] for row in table_data if len(row) > 6]
    window['-TABLE-'].update(table_display_data)

    conversation_history = [
        {"role": "assistant", "content": "Dzień dobry! Jestem agentem AI. Opisz proszę swoje objawy, a postaram się dobrać odpowiedni lek."}
    ]

    try:
        df = pd.read_excel("drugs.xlsx")
    except FileNotFoundError:
        sg.popup_error("Nie znaleziono pliku drugs.xlsx")
        return

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Zamknij'):
            break

        if event == 'Wyślij do agenta':
            user_msg = values['-INPUT-'].strip()
            if not user_msg:
                continue

            conversation_history.append({"role": "user", "content": user_msg})
            current_chat = window["-CHAT-"].get()
            window["-CHAT-"].update(f"{current_chat}\nTy: {user_msg}\n")
            window["-INPUT-"].update("")
            window.refresh()

            try:
                response = query_gpt_and_find_medicine(user_msg, df, conversation_history)
                conversation_history.append({"role": "assistant", "content": response.strip()})

                current_chat = window["-CHAT-"].get()
                window["-CHAT-"].update(f"{current_chat}\nAgent: {response.strip()}\n")
            except Exception as e:
                window["-CHAT-"].update(f"{window['-CHAT-'].get()}\nAgent: Wystąpił błąd: {str(e)}\n")


        if event == 'Szukaj':
            table_data = load_drugs(values['-SEARCH-'])
            table_display_data = [[row[0], row[1],row[2], row[6]] for row in table_data if len(row) > 6]
            window['-TABLE-'].update(table_display_data)

        if event == 'Pokaż wszystko':
            table_data = load_drugs()
            table_display_data = [[row[0], row[1],row[2], row[6]] for row in table_data if len(row) > 6]
            window['-TABLE-'].update(table_display_data)

        if event == 'Dodaj do koszyka':
            selected = values['-TABLE-']
            if not selected:
                sg.popup_error("Wybierz lek")
                continue

            row = table_data[selected[0]]

            try:
                drug_id = row[0]
                name = row[1]
                on_prescription = row[2].lower() == "yes"
                available_qty = int(row[3])
                price = float(row[6])
            except (IndexError, ValueError):
                sg.popup_error("Nieprawidłowy format danych leku.")
                continue

            qty_str = sg.popup_get_text(f'Ile sztuk leku \"{name}\" chcesz dodać?', default_text="")
            try:
                qty = int(qty_str)
                if qty <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                sg.popup_error("Podaj poprawną liczbę większą od zera.")
                continue

            if qty > available_qty:
                sg.popup_error("Brak w magazynie wystarczającej ilości leku.")
                continue

            prescription_number = ""
            if on_prescription:
                max_attempts = 10  

                for attempt in range(max_attempts):
                    prescription_number = sg.popup_get_text(
                        f"Lek \"{name}\" wymaga recepty.\nPodaj numer recepty :",
                        title="Numer recepty"
                    )

                    if prescription_number is None:
                        sg.popup("Anulowano dodawanie leku do koszyka.")
                        break

                    if prescription_number == str(row[5]):
                        break  
                    else:
                        sg.popup_error("Nieprawidłowy numer recepty.")

                else:
                    sg.popup("Przekroczono liczbę prób. Lek nie został dodany do koszyka.")
                    continue

                if prescription_number is None:
                    continue

            cart.append({
                'id': drug_id,
                'name': name,
                'qty': qty,
                'prescription_required': on_prescription,
                'prescription': prescription_number,
                'price': price
            })
            update_cart_display(window)

        if event == 'Kup teraz':
            if not cart:
                sg.popup_error("Koszyk jest pusty")
                continue

            for item in cart:
                if item.get('prescription_required') and not item.get('prescription', '').strip():
                    sg.popup_error(f"Lek „{item['name']}” wymaga numeru recepty.\nZamówienie przerwane.")
                    break
            else:
                errors = []
                for item in cart:
                    try:
                        db.order_drug(item['id'], -item['qty'])
                        add_purchase_to_customer_file(
                            client_id, item['name'], item['qty'], item.get('prescription', '')
                        )
                    except Exception as e:
                        errors.append(f"{item['name']}: {e}")

                if errors:
                    sg.popup_error("Błędy przy zakupie:\n" + "\n".join(errors))
                else:
                    sg.popup_ok("Zakup zakończony pomyślnie!")
                    cart.clear()
                    update_cart_display(window)
                    table_data = load_drugs()
                    window['-TABLE-'].update(table_display_data)

    window.close()
