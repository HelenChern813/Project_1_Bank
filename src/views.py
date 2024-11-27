import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import file_df, open_file_json, unique_cards

load_dotenv()
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
URL_RATE = "https://api.apilayer.com/exchangerates_data/latest"
URL_STOCKS = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY_STOCK}"


def get_hello(date: str | None) -> json:
    """Вычисление текущего времени и определение нужного вступительного сообщения"""

    if not date:
        date = datetime.now()
    date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    if 4 <= date.hour <= 11:
        return "Доброе утро"
    elif 12 <= date.hour <= 15:
        return "Добрый день"
    elif 16 <= date.hour <= 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def actual_df_mouth(data: pd.DataFrame, date: str) -> list:
    """Формирование нового итерируемого объекта с транзакциями от начала месяца"""

    date_operations = []
    end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    first_day_date = end_date.replace(day=1)
    for index, operation in data.iterrows():
        if first_day_date <= datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S") <= end_date:
            date_operations.append(operation)
    return date_operations


def info_cards(data: pd.DataFrame, path: str, date: str) -> list:
    """Для сбора данных о транзакциях по картам, кроме стандартного ДФ и даты, принимает путь к самому файлу"""

    data_list = actual_df_mouth(data, date)
    info_cards_list = []

    cards = unique_cards(path)
    for i in cards:

        total_spent = 0
        cashback = 0

        for transactions in data_list:
            if transactions["Номер карты"] == i:
                total_spent += float(transactions["Сумма платежа"])
                cashback += float(transactions["Кэшбэк"])
        dict_card = {"last_digits": i, "total_spent": round(total_spent, 2), "cashback": cashback}
        info_cards_list.append(dict_card)
    return info_cards_list


def top_transactions(data: pd.DataFrame, date: str | None = None) -> list:
    """Для сбора данных о 5 самых больших транзакции"""

    data_list = actual_df_mouth(data, date)
    top_transactions_list = []
    sorted_transactions = sorted(data_list, key=lambda x: x["Сумма операции с округлением"])
    for i in sorted_transactions[-6:-1]:
        top_transactions_dict = {
            "date": i["Дата операции"],
            "amount": i["Сумма платежа"],
            "category": i["Категория"],
            "description": i["Описание"],
        }
        top_transactions_list.append(top_transactions_dict)
    return top_transactions_list


def convert_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Any:
    """Функция возращает актуальный курс"""

    headers = {"apikey": API_KEY_CURRENCY}
    params = {"base": base_currency, "symbols": target_currency}
    response = requests.get(URL_RATE, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["rates"][target_currency]
    else:
        raise Exception(f"Ошибка запроса {response.status_code}")


def get_actual_currencies_price() -> list:
    """Возвращает список актуального курса валют"""

    data = open_file_json()
    user_currencies: list[str] = data["user_currencies"]

    currency_rates = []

    for currency in user_currencies:
        currency_dict = {"currency": currency, "rate": convert_exchange_rate(currency)}
        currency_rates.append(currency_dict)
    return currency_rates


def convert_stocks() -> Any:
    """Функция возращает JSON-объект с данными по акциям"""

    response = requests.get(URL_STOCKS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Ошибка запроса {response.status_code}")


def get_actual_stocks_price() -> list:
    """Возвращает список актуального курса валют"""

    data = open_file_json()
    user_stocks: list[str] = data["user_stocks"]

    stocks_rates = []
    list_stocks = convert_stocks()

    for stock in user_stocks:
        for i in list_stocks:
            if i["symbol"] == stock:
                stocks_dict = {"stock": stock, "price": i["price"]}
                stocks_rates.append(stocks_dict)
    return stocks_rates


def home_page(data: pd.DataFrame, path: str, date: str | None = None) -> json:
    """Основная функция, которая формирует JSON-ответ"""

    output = {
        "hello_message": get_hello(date),
        "cards": info_cards(data, path, date),
        "top_transactions": top_transactions(data, date),
        "currencies": get_actual_currencies_price(),
        "stock_prices": get_actual_stocks_price(),
    }
    return json.dumps(output, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    file_path = "../data/operations.xlsx"

    df = file_df(file_path)
    date = "30.11.2021 18:19:28"
    print(home_page(df, file_path, date))
