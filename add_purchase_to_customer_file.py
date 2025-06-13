import os
from datetime import datetime


def add_purchase_to_customer_file(client_id, drug_name, quantity, expiry_date=None):
    """
    Dodaje wpis o zakupie leku do pliku klienta w katalogu "DATABASE".

    Jeśli katalog "DATABASE" lub plik klienta jeszcze nie istnieją, są tworzone automatycznie.
    W pliku zapisywana jest data i czas zakupu, nazwa leku, ilość oraz opcjonalnie data ważności leku.

    Args:
        client_id (str | int): Unikalny identyfikator klienta, używany jako nazwa pliku.
        drug_name (str): Nazwa zakupionego leku.
        quantity (int): Ilość zakupionego leku.
        expiry_date (str, optional): Data ważności leku w formacie tekstowym (np. "YYYY-MM-DD").
            Domyślnie None, wtedy data ważności nie jest zapisywana.

    Plik zapisu:
        - Katalog: "DATABASE"
        - Nazwa pliku: "{client_id}.txt"
        - Format wpisu: "YYYY-MM-DD HH:MM:SS - nazwa leku, ilość: X, data ważności: YYYY-MM-DD" (opcjonalnie data ważności)

    Przykład wpisu w pliku:
        2025-06-13 15:30:45 - Paracetamol, ilość: 2, data ważności: 2026-01-01
    """
    folder = "DATABASE"
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, f"{client_id}.txt")

    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Klient ID: {client_id}\nZakupy:\n")

    with open(filepath, "a", encoding="utf-8") as f:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{now_str} - {drug_name}, ilość: {quantity}"
        if expiry_date:
            line += f", data ważności: {expiry_date}"
        line += "\n"
        f.write(line)
