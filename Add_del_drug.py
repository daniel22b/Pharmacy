from datetime import datetime
import pandas as pd

def add_drug(drug, on_recept, no_packages):
    file_path = '/home/arus/ProjektPython/Pharmacy/drugs.xlsx'

    df_raw = pd.read_excel(file_path, header=None)
    header_row = df_raw.iloc[0, 0]
    data_rows = df_raw.iloc[1:, 0]
    df = data_rows.str.split(",", expand=True)
    df.columns = header_row.split(",")

    df["ID"] = df["ID"].astype(int)
    df["NO_PACKAGES_AVAILABLE"] = df["NO_PACKAGES_AVAILABLE"].astype(int)
    df["DATE"] = pd.to_datetime(df["DATE"])

    new_id = df["ID"].max() + 1

    # teraz data z godziną i minutą
    today = pd.Timestamp.today().strftime("%Y-%m-%d %H:%M:%S")

    new_row = [str(new_id), drug.upper(), on_recept, str(no_packages), today]

    df = pd.concat([df, pd.DataFrame([new_row], columns=df.columns)], ignore_index=True)

    # Format daty z godziną i minutą
    df["DATE"] = pd.to_datetime(df["DATE"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    new_data = df.astype(str).agg(",".join, axis=1)
    final_df = pd.DataFrame([header_row])
    final_df = pd.concat([final_df, new_data.to_frame()], ignore_index=True)

    final_df.to_excel(file_path, index=False, header=False)

# Usunęcie leku


def remove_drug(identifier):
    file_path = '/home/arus/ProjektPython/Pharmacy/drugs.xlsx'

    # 1. Wczytaj plik jako jedną kolumnę
    df_raw = pd.read_excel(file_path, header=None)
    header_row = df_raw.iloc[0, 0]
    data_rows = df_raw.iloc[1:, 0]

    # 2. Rozdziel dane na kolumny
    df = data_rows.str.split(",", expand=True)
    df.columns = header_row.split(",")

    # 3. Zamień typy
    df["ID"] = df["ID"].astype(int)
    df["NO_PACKAGES_AVAILABLE"] = df["NO_PACKAGES_AVAILABLE"].astype(int)
    df["DATE"] = pd.to_datetime(df["DATE"])

    # 4. Usuń po ID lub nazwie (case-insensitive)
    if str(identifier).isdigit():
        identifier = int(identifier)
        df = df[df["ID"] != identifier]
    else:
        df = df[df["DRUG"].str.upper() != str(identifier).upper()]

    # 5. Przywróć formatowanie daty z godziną i minutą
    df["DATE"] = df["DATE"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 6. Zapisz z powrotem w formacie z jedną kolumną (CSV w Excelu)
    new_data = df.astype(str).agg(",".join, axis=1)
    final_df = pd.DataFrame([header_row])
    final_df = pd.concat([final_df, new_data.to_frame()], ignore_index=True)
    final_df.to_excel(file_path, index=False, header=False)
