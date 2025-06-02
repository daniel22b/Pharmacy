import os
from datetime import datetime


def add_purchase_to_customer_file(client_id, drug_name, quantity, expiry_date=None):
    folder = "DATABASE"
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, f"{client_id}.txt")

    # Jeśli plik nie istnieje, utwórz go z nagłówkiem
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Klient ID: {client_id}\nZakupy:\n")

    # Dopisz zakup do pliku
    with open(filepath, "a", encoding="utf-8") as f:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{now_str} - {drug_name}, ilość: {quantity}"
        if expiry_date:
            line += f", data ważności: {expiry_date}"
        line += "\n"
        f.write(line)
