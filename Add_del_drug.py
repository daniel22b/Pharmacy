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
        df["DATE"] = pd.to_datetime(df["DATE"], format='mixed')
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
        today = datetime.now().strftime("%Y-%m-%d")

        new_row = {
            "ID": int(new_id),
            "DRUG": drug.upper(),
            "DATE": today,
            "ON_RECEPT": on_recept,
            "RECEPT_ID": str(recept_id) if recept_id else "",
            "NO_PACKAGES_AVAILABLE": int(no_packages)
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
        qty_to_add = int(qty_to_add)

        self.df["ID"] = self.df["ID"].astype(int)
        self.df["NO_PACKAGES_AVAILABLE"] = self.df["NO_PACKAGES_AVAILABLE"].astype(int)

        match = self.df[self.df["ID"] == drug_id]

        if match.empty:
            raise ValueError("Nie znaleziono leku o podanym ID")

        idx = match.index[0]
        current_qty = int(self.df.at[idx, "NO_PACKAGES_AVAILABLE"])
        new_qty = current_qty + qty_to_add

        if new_qty < 0:
            raise ValueError("Nie można mieć ujemnej ilości leku w magazynie.")

        self.df.at[idx, "NO_PACKAGES_AVAILABLE"] = new_qty
        self.save_data()
