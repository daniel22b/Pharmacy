import csv
import os
from datetime import datetime
import random

CUSTOMER_FILE = "DATABASE/customers.csv"

# Tworzy plik z nagłówkiem jeśli nie istnieje
def init_customer_file():
    if not os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "NAME", "EMAIL", "PHONE", "CREATED", "UPDATED"])

def generate_unique_id():
    existing_ids = set()
    if os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_ids = {row["ID"] for row in reader}
    
    while True:
        new_id = ''.join(str(random.randint(0, 9)) for _ in range(4))
        if new_id not in existing_ids:
            return new_id

def add_customer(name, email, phone):
    init_customer_file()
    customer_id = generate_unique_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CUSTOMER_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([customer_id, name, email, phone, now, now])
    
    return customer_id
