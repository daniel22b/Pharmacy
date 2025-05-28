import csv
import os
import random
from datetime import datetime
import pandas as pd

CUSTOMER_FILE = "customers.csv"
ADRESS_FILE = "address.csv"


def add_customer(user_name, name, surname, email, phone, date_of_birth, gender, street, city, country, password):

    def check_duplicates(email,phone):
        if not os.path.exists(CUSTOMER_FILE):
            return None
        with open(CUSTOMER_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['E-MAIL'].strip().lower() == email.strip().lower():
                    return "e-mail"
                if row['PHONE'].strip() == phone.strip():
                    return "numer telefonu"
        return None
    duplicate_type = check_duplicates(email, phone)
    if duplicate_type:
        raise ValueError(f"{duplicate_type} jest już używany. Podaj inny.")
    
    def generate_id():
        return ''.join(str(random.randint(0, 9)) for _ in range(4))

    def calculate_age(date_of_birth_str):
        birth_date = datetime.strptime(date_of_birth_str, "%d.%m.%Y").date()
        today = datetime.today().date()
        age = today.year - birth_date.year 

    if not os.path.exists(CUSTOMER_FILE):
        with open(CUSTOMER_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "USER_NAME", "NAME", "SURNAME", "EMAIL", "PHONE", "CREATED", "UPDATED", "AGE", "DATE_OF_BIRTH", "GENDER", "PASSWORD"])

    now = datetime.now().strftime("%d.%m.%Y")
    customer_id = generate_id()
    age = calculate_age(date_of_birth)


    def save_to_csv(filepath, row):
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    save_to_csv(CUSTOMER_FILE, [customer_id, user_name, name, surname, email, phone, now, now, date_of_birth, age,  gender, password])
    save_to_csv(ADRESS_FILE, [customer_id, street, city, country])

def remove_customer(file_path,customer_id):

    if not os.path.exists(file_path):
        raise FileNotFoundError("Plik z klientami nie istnieje.")
    df = pd.read_csv(file_path)
    df = df[df["ID"].astype(str) != str(customer_id)]
    df.to_csv(file_path, index=False)



