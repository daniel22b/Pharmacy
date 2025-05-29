# import pandas as pd
# from datetime import datetime

# FILE_PATH = 'drugs.xlsx'

# def load_drug_data(file_path=FILE_PATH):
#     df_raw = pd.read_excel(file_path, header=None)
#     header_row = df_raw.iloc[0, 0]
#     data_rows = df_raw.iloc[1:, 0]

#     df = data_rows.str.split(",", expand=True)
#     header_cols = header_row.split(",")

#     df.columns = header_cols
#     df["ID"] = df["ID"].astype(int)
#     df["NO_PACKAGES_AVAILABLE"] = df["NO_PACKAGES_AVAILABLE"].astype(int)
#     df["DATE"] = pd.to_datetime(df["DATE"])
#     df["RECEPT_ID"] = df["RECEPT_ID"].fillna("").astype(str)


#     return df, header_row

# def save_drug_data(df, header_row, file_path=FILE_PATH):
#     if header_row is None:
#         header_row = ",".join(df.columns)
#     # df["DATE"] = df["DATE"].dt.strftime("%Y-%m-%d %H:%M:%S")
#     new_data = df.astype(str).agg(",".join, axis=1)
#     final_df = pd.DataFrame([header_row])
#     final_df = pd.concat([final_df, new_data.to_frame()], ignore_index=True)
#     final_df.to_excel(file_path, index=False, header=False)

# def add_drug(drug, on_recept, no_packages,recept_id=None):
    
#     df, header_row = load_drug_data()
#     if recept_id is not None and str(recept_id).strip() != "":
#         if recept_id in df["RECEPT_ID"].astype(str).values:
#             raise ValueError(f"RECEPT_ID '{recept_id}' jest już w bazie. Podaj inny.")
         
#     new_id = df["ID"].max() + 1 if not df.empty else 1
#     today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     new_row = [str(new_id), drug.upper(), on_recept, str(no_packages), today, str(recept_id) if recept_id else ""]
#     df = pd.concat([df, pd.DataFrame([new_row], columns=df.columns)], ignore_index=True)

#     save_drug_data(df, header_row)

# def remove_drug(identifier):
#     df, header_row = load_drug_data()

#     if str(identifier).isdigit():
#         identifier = int(identifier)
#         df = df[df["ID"] != identifier]
#     else:
#         df = df[df["DRUG"].str.upper() != str(identifier).upper()]

#     save_drug_data(df, header_row)

# def order_drug(drug_id, qty_to_add):
#     """Zwiększ liczbę opakowań dla danego leku i zapisz"""
#     # Wczytaj dane
#     df_raw = pd.read_excel(FILE_PATH, header=None)
#     header_line = df_raw.iloc[0, 0]
#     header = header_line.split(",")
#     df = df_raw.iloc[1:, 0].str.split(",", expand=True)
#     df.columns = header

#     # Upewnij się, że ilości są liczbami
#     df["NO_PACKAGES_AVAILABLE"] = df["NO_PACKAGES_AVAILABLE"].astype(int)

#     # Zwiększ liczbę opakowań
#     if drug_id not in df["ID"].values:
#         raise ValueError("Nie znaleziono leku o podanym ID")
#     df.loc[df["ID"] == drug_id, "NO_PACKAGES_AVAILABLE"] += qty_to_add

#     # Konwersja z powrotem do formatu pliku: jedna kolumna tekstowa z przecinkami
#     lines = [header_line] + df.apply(lambda row: ",".join(row.astype(str)), axis=1).tolist()
#     df_final = pd.DataFrame(lines)

#     # Zapis
#     df_final.to_excel(FILE_PATH, index=False, header=False)
import pandas as pd
from datetime import datetime

class DrugDatabase:
    def __init__(self, file_path='drugs.xlsx'):
        self.file_path = file_path
        self.header_row = None
        self.df = None
        self.load_data()

    def load_data(self):
        df_raw = pd.read_excel(self.file_path, header=None)
        self.header_row = df_raw.iloc[0, 0]
        data_rows = df_raw.iloc[1:, 0]

        df = data_rows.str.split(",", expand=True)
        header_cols = self.header_row.split(",")

        df.columns = header_cols
        df["ID"] = df["ID"].astype(int)
        df["NO_PACKAGES_AVAILABLE"] = df["NO_PACKAGES_AVAILABLE"].astype(int)
        df["DATE"] = pd.to_datetime(df["DATE"])
        df["RECEPT_ID"] = df["RECEPT_ID"].fillna("").astype(str)

        self.df = df

    def save_data(self):
        if self.header_row is None:
            self.header_row = ",".join(self.df.columns)
        new_data = self.df.astype(str).agg(",".join, axis=1)
        final_df = pd.DataFrame([self.header_row])
        final_df = pd.concat([final_df, new_data.to_frame()], ignore_index=True)
        final_df.to_excel(self.file_path, index=False, header=False)

    def add_drug(self, drug, on_recept, no_packages, recept_id=None):
        if recept_id is not None and str(recept_id).strip() != "":
            if recept_id in self.df["RECEPT_ID"].astype(str).values:
                raise ValueError(f"RECEPT_ID '{recept_id}' jest już w bazie. Podaj inny.")
        
        new_id = self.df["ID"].max() + 1 if not self.df.empty else 1
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_row = {
        "ID": int(new_id),
        "DRUG": drug.upper(),
        "ON_RECEPT": on_recept,
        "NO_PACKAGES_AVAILABLE": int(no_packages),
        "DATE": pd.to_datetime(today),
        "RECEPT_ID": str(recept_id) if recept_id else ""
}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_data()

    def remove_drug(self, identifier):
        if str(identifier).isdigit():
            identifier = int(identifier)
            self.df = self.df[self.df["ID"] != identifier]
        else:
            self.df = self.df[self.df["DRUG"].str.upper() != str(identifier).upper()]
        self.save_data()

    def order_drug(self, drug_id, qty_to_add):
        drug_id = int(drug_id)
        if drug_id not in self.df["ID"].values:
            raise ValueError("Nie znaleziono leku o podanym ID")
        self.df.loc[self.df["ID"] == drug_id, "NO_PACKAGES_AVAILABLE"] += int(qty_to_add)
        self.save_data()
