import json
import os

import pandas as pd


def file_df(path: str) -> pd.DataFrame:
    """Читает файл с транзакциями и не учитывает транзакции по статусу 'FAILED"""

    file_path = os.path.abspath(path)
    df = pd.read_excel(file_path)
    df = df[df["Статус"] == "OK"]
    df = df.replace("NaN", "0")
    return df


def unique_cards(path: str) -> list:

    df = file_df(path)
    df = df["Номер карты"].dropna()
    cards = df.unique()
    return cards


def open_file_json() -> dict:
    """Чтение JSON файла user_settings.json"""

    full_path = os.path.abspath("../user_settings.json")
    with open(full_path, "r+", encoding="utf-8") as file:
        data = json.load(file)
        return data
