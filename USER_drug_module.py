import PySimpleGUI as sg
import pandas as pd
import os
from Add_del_drug import DrugDatabase
from add_purchase_to_customer_file import add_purchase_to_customer_file
from Agent import agent_ai,query_gpt_and_find_medicine

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
            sg.Column([
                [sg.Text('Lista leków', font=('Helvetica', 16, 'bold'), text_color='white', background_color='#2B2B2B')],
                [
                    sg.Text('Szukaj:', background_color='#2B2B2B', text_color='white'),
                    sg.Input(key='-SEARCH-', size=(30, 1)),
                    sg.Button('Szukaj', button_color=('white', 'green')),
                    sg.Button('Pokaż wszystko', button_color=('white', 'green'))
                ],
                [sg.Table(
                    values=[],
                    headings=['ID', 'Nazwa', 'Recepta', 'Cena'],
                    key='-TABLE-',
                    auto_size_columns=False,
                    col_widths=[8, 25, 10],
                    justification='left',
                    num_rows=10,
                    enable_events=True,
                    background_color='#2B2B2B',
                    text_color='white',
                    header_background_color='darkgreen',
                    header_text_color='white',
                    alternating_row_color='#3C3C3C',
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE
                )],
                [
                    sg.Button('Dodaj do koszyka', button_color=('white', 'purple')),
                    sg.Button('Kup teraz', button_color=('white', 'green')),
                    sg.Button('Zamknij', button_color=('white', 'gray'))
                ],
                [sg.Text('Koszyk:', font=('Helvetica', 12, 'bold'), text_color='white', background_color='#2B2B2B')],
                [sg.Listbox(values=[], size=(60, 5), key='-CART-', background_color='#1E1E1E', text_color='white')]
            ], element_justification='left'),

            sg.VerticalSeparator(),

            sg.Column([
                [sg.Text("Agent AI", font=('Helvetica', 14, 'bold'), text_color='white', background_color='#2B2B2B')],
                [sg.Multiline("Dzień dobry! Jestem agentem Ai.\nOpisz mi prosze swoje objawy a postaram sie dobrac odpowiedni lek.\n", size=(50, 15), key='-CHAT-', disabled=True)],
                [sg.InputText(key='-INPUT-', size=(40, 1)), sg.Button("Wyślij do agenta")]
            ], background_color='#2B2B2B', element_justification='left')
        ]
    ]

    window = sg.Window('Użytkownik - Lista leków', layout, finalize=True, background_color='#2B2B2B')

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
