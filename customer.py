import csv
import os
import random
from datetime import datetime

CUSTOMER_FILE = "DATABASE/customers.csv"
ADRESS_FILE = "address.csv"


def generate_id():
    return ''.join(str(random.randint(0, 9)) for _ in range(4))

def add_customer(name, email, phone,date_of_birth,gender,street,city,country):
    # if not os.path.exists(CUSTOMER_FILE):
    #     with open(CUSTOMER_FILE, 'w', newline='', encoding='utf-8') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(["ID", "NAME", "EMAIL", "PHONE", "CREATED", "UPDATED","DATE_OF_BIRTH","GENDER"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    customer_id = generate_id()

    with open(CUSTOMER_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([customer_id, name, email, phone, now, now,date_of_birth,gender])

    with open(ADRESS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([customer_id,street,city,country])

    return customer_id
