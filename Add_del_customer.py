import csv
import os
import random
from datetime import datetime
import pandas as pd

CUSTOMER_FILE = "customers.csv"
ADRESS_FILE = "address.csv"



def add_customer(name, email, phone,date_of_birth,gender,street,city,country):
    def generate_id():
        return ''.join(str(random.randint(0, 9)) for _ in range(4))
    
    if not os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "NAME", "EMAIL", "PHONE", "CREATED", "UPDATED","DATE_OF_BIRTH","GENDER"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    customer_id = generate_id()
    
    def save_to_csv(filepath, row):
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    save_to_csv(CUSTOMER_FILE, [customer_id, name, email, phone, now, now, date_of_birth, gender])
    save_to_csv(ADRESS_FILE, [customer_id, street, city, country])

def remove_customer(file_path,customer_id):

    # if not os.path.exists(CUSTOMERS_FILE):
    #         raise FileNotFoundError("Plik z klientami nie istnieje.")
    # df = pd.read_csv(CUSTOMERS_FILE)
    # df = df[df["ID"].astype(str) != str(customer_id)]
    # df.to_csv(CUSTOMERS_FILE, index=False)

    # if not os.path.exists(ADRESS_FILE):
    #         raise FileNotFoundError("Plik z klientami nie istnieje.")
    # df = pd.read_csv(ADRESS_FILE)
    # df = df[df["ID"].astype(str) != str(customer_id)]
    # df.to_csv(ADRESS_FILE, index=False)

    if not os.path.exists(file_path):
        raise FileNotFoundError("Plik z klientami nie istnieje.")
    df = pd.read_csv(file_path)
    df = df[df["ID"].astype(str) != str(customer_id)]
    df.to_csv(file_path, index=False)

