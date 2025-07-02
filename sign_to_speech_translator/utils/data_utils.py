# utils/data_utils.py

import pandas as pd
import os

def load_data(path="data/sign_data.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found.")
    df = pd.read_csv(path)
    X = df.drop("label", axis=1)
    y = df["label"]
    return X, y

def save_row_to_csv(row, label, path="data/sign_data.csv"):
    df = pd.read_csv(path)
    df.loc[len(df)] = [label] + row
    df.to_csv(path, index=False)
