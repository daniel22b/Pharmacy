import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from Add_del_drug import add_drug, remove_drug
import pandas as pd
from customer import add_customer

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")
    app = ctk.CTk()
    app.geometry("400x300")
    app.title("System Apteki")

    CORRECT_PIN = "1"

    def open_main_window(user_type):
        login_window.withdraw()
        main_window = ctk.CTkToplevel()
        main_window.geometry("400x400")
        main_window.title(f"System Apteki - {user_type}")


        def on_register_click():
            register_window = ctk.CTkToplevel()
            register_window.title("Rejestracja klienta")
            register_window.geometry("400x350")

            ctk.CTkLabel(register_window, text="Imię i nazwisko:").pack(pady=5)
            name_entry = ctk.CTkEntry(register_window)
            name_entry.pack()

            ctk.CTkLabel(register_window, text="Email:").pack(pady=5)
            email_entry = ctk.CTkEntry(register_window)
            email_entry.pack()

            ctk.CTkLabel(register_window, text="Telefon:").pack(pady=5)
            phone_entry = ctk.CTkEntry(register_window)
            phone_entry.pack()

            def submit_customer():
                name = name_entry.get()
                email = email_entry.get()
                phone = phone_entry.get()

                if not name or not email or not phone:
                    messagebox.showwarning("Brak danych", "Uzupełnij wszystkie pola.")
                    return

                try:
                    customer_id = add_customer(name, email, phone)
                    messagebox.showinfo("Sukces", f"Klient został dodany z ID: {customer_id}")
                    register_window.destroy()
                except Exception as e:
                    messagebox.showerror("Błąd", f"Nie udało się dodać klienta: {e}")

            ctk.CTkButton(register_window, text="Zarejestruj", command=submit_customer).pack(pady=20)


        def open_drug_list():
            list_window = ctk.CTkToplevel()
            list_window.title("Lista leków")
            list_window.geometry("1000x700")

            search_frame = ctk.CTkFrame(list_window)
            search_frame.pack(pady=10)

            ctk.CTkLabel(search_frame, text="Wyszukaj po nazwie lub ID:").pack(side="left", padx=5)
            search_entry = ctk.CTkEntry(search_frame)
            search_entry.pack(side="left", padx=5)

            def load_data(filter_query=""):
                try:
                    df_raw = pd.read_excel("drugs.xlsx", header=None)
                    header = df_raw.iloc[0, 0].split(",")
                    df = df_raw.iloc[1:, 0].str.split(",", expand=True)
                    df.columns = header

                    if filter_query:
                        query = filter_query.lower()
                        df = df[df.apply(lambda row: query in str(row["ID"]).lower() or query in str(row["DRUG"]).lower(), axis=1)]

                    tree.delete(*tree.get_children())
                    for _, row in df.iterrows():
                        tree.insert("", "end", values=tuple(row))
                except Exception as e:
                    messagebox.showerror("Błąd", f"Nie można wczytać danych: {e}")

            ctk.CTkButton(search_frame, text="Szukaj", command=lambda: load_data(search_entry.get())).pack(side="left", padx=5)
            ctk.CTkButton(search_frame, text="Pokaż wszystko", command=lambda: load_data()).pack(side="left", padx=5)

            tree = ttk.Treeview(list_window, columns=("ID", "DRUG", "ON_RECEPT", "NO_PACKAGES_AVAILABLE", "DATE"), show='headings')
            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            tree.pack(expand=True, fill="both", pady=10)

            def add_drug_window():
                drug_window = ctk.CTkToplevel()
                drug_window.title("Dodaj lek")
                drug_window.geometry("300x300")

                ctk.CTkLabel(drug_window, text="Nazwa leku:").pack(pady=5)
                drug_entry = ctk.CTkEntry(drug_window)
                drug_entry.pack()

                ctk.CTkLabel(drug_window, text="Na receptę:").pack(pady=5)
                on_recept_option = ctk.StringVar(value="YES")
                ctk.CTkOptionMenu(drug_window, variable=on_recept_option, values=["YES", "NO"]).pack()

                ctk.CTkLabel(drug_window, text="Liczba opakowań:").pack(pady=5)
                package_entry = ctk.CTkEntry(drug_window)
                package_entry.pack()

                def submit_drug():
                    try:
                        add_drug(
                            drug_entry.get(),
                            on_recept_option.get().strip().upper(),
                            int(package_entry.get())
                        )
                        messagebox.showinfo("Sukces", "Lek został dodany.")
                        drug_window.destroy()
                        load_data()
                    except Exception as e:
                        messagebox.showerror("Błąd", f"Błąd dodawania leku: {e}")

                ctk.CTkButton(drug_window, text="Dodaj", command=submit_drug).pack(pady=10)

            def delete_selected_drug():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Brak wyboru", "Zaznacz rekord do usunięcia.")
                    return

                record = tree.item(selected[0])["values"]
                identifier = record[0]
                name = record[1]

                try:
                    remove_drug(identifier)
                    messagebox.showinfo("Sukces", f"Lek '{name}' (ID: {identifier}) został usunięty.")
                    tree.delete(selected[0])
                except Exception as e:
                    messagebox.showerror("Błąd", f"Nie udało się usunąć leku: {e}")

            button_frame = ctk.CTkFrame(list_window)
            button_frame.pack(pady=10)

            ctk.CTkButton(button_frame, text="Dodaj lek", command=add_drug_window).pack(side="left", padx=10)
            ctk.CTkButton(button_frame, text="Usuń zaznaczony lek", command=delete_selected_drug).pack(side="left", padx=10)

            load_data()

        if user_type == "Admin":
            ctk.CTkButton(main_window, text="Zarejestruj klienta", command=on_register_click).pack(pady=10)
            ctk.CTkButton(main_window, text="Lista leków", command=open_drug_list).pack(pady=10)
        else:
            ctk.CTkLabel(main_window, text="Witaj, użytkowniku!").pack(pady=20)

        ctk.CTkButton(
            main_window,
            text="Wyloguj się",
            command=lambda: (main_window.destroy(), login_window.deiconify())
        ).pack(pady=20)

    def ask_for_pin():
        def check_pin():
            entered_pin = pin_entry.get()
            if entered_pin == CORRECT_PIN:
                pin_window.destroy()
                open_main_window("Admin")
            else:
                messagebox.showerror("Błąd", "PIN error")

        pin_window = ctk.CTkToplevel()
        pin_window.geometry("300x150")
        pin_window.title("Podaj PIN")

        ctk.CTkLabel(pin_window, text="Wprowadź PIN:").pack(pady=10)
        pin_entry = ctk.CTkEntry(pin_window, show="*")
        pin_entry.pack(pady=5)
        ctk.CTkButton(pin_window, text="Potwierdź", command=check_pin).pack(pady=10)

    login_window = app
    ctk.CTkLabel(login_window, text="Wybierz typ logowania:").pack(pady=20)
    ctk.CTkButton(login_window, text="User", command=lambda: open_main_window("User")).pack(pady=10)
    ctk.CTkButton(login_window, text="Admin", command=ask_for_pin).pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()