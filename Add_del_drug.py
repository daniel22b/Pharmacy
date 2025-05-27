import pandas as pd
from datetime import datetime

FILE_PATH = 'drugs.xlsx'

def load_drug_data(file_path=FILE_PATH):
    df_raw = pd.read_excel(file_path, header=None)
    header_row = df_raw.iloc[0, 0]
    data_rows = df_raw.iloc[1:, 0]

    df = data_rows.str.split(",", expand=True)
    header_cols = header_row.split(",")

    df.columns = header_cols
    df["ID"] = df["ID"].astype(int)
    df["NO_PACKAGES_AVAILABLE"] = df["NO_PACKAGES_AVAILABLE"].astype(int)
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["RECEPT_ID"] = df["RECEPT_ID"].apply(lambda x: int(x) if str(x).isdigit() else None)

    

    return df, header_row

def save_drug_data(df, header_row, file_path=FILE_PATH):
    if header_row is None:
        header_row = ",".join(df.columns)
    # df["DATE"] = df["DATE"].dt.strftime("%Y-%m-%d %H:%M:%S")
    new_data = df.astype(str).agg(",".join, axis=1)
    final_df = pd.DataFrame([header_row])
    final_df = pd.concat([final_df, new_data.to_frame()], ignore_index=True)
    final_df.to_excel(file_path, index=False, header=False)

def add_drug(drug, on_recept, no_packages,recept_id=None):
    df, header_row = load_drug_data()

    new_id = df["ID"].max() + 1
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_row = [str(new_id), drug.upper(), on_recept, str(no_packages), today,str(recept_id) if recept_id else ""]
    df = pd.concat([df, pd.DataFrame([new_row], columns=df.columns)], ignore_index=True)

    save_drug_data(df, header_row)

def remove_drug(identifier):
    df, header_row = load_drug_data()

    if str(identifier).isdigit():
        identifier = int(identifier)
        df = df[df["ID"] != identifier]
    else:
        df = df[df["DRUG"].str.upper() != str(identifier).upper()]

    save_drug_data(df, header_row)
