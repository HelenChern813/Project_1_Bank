from datetime import datetime
import json
from dotenv import load_dotenv
import os
import requests
from typing import Any


load_dotenv()
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
URL_RATE = "https://api.apilayer.com/exchangerates_data/latest"
URL_STOCKS = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY_STOCK}'



def get_hello(date: str | None = None) -> json:
    """
    Выдисление текущего времени и определение нужного вступительного сообщения
    """

    if not date:
        date = datetime.now()
#        date = date.strftime("%Y-%m-%d %H:%M:%S")

    if 4 <= date.hour <= 11:
        return 'Доброе утро'
    elif 12 <= date.hour <= 15:
        return 'Добрый день'
    elif 16 <= date.hour <= 22:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


def get_first_mouth_day(date: datetime | None = None) -> datetime| str:
    '''Получение первого дня месяца для поиска транзакций дата строкой в формате "YYYY-MM-DD HH:MM:SS"'''

    if not date:
        # Получение времени YYYY-MM-DD HH:MM:SS
        date = datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")

    first_day_date = date.replace(day=1)

    return first_day_date


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


def open_file_json() -> dict:
    '''Чтение JSON файла user_settings.json'''

    full_path = os.path.abspath('../user_settings.json')
    with open(full_path, "r+", encoding="utf-8") as file:
        data = json.load(file)
        return data


def get_actual_currencies_price() -> list:
    '''Возвращает список актуального курса валют'''

    data = open_file_json()
    user_currencies: list[str] = data['user_currencies']

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
    '''Возвращает список актуального курса валют'''

    data = open_file_json()
    user_stocks: list[str] = data['user_stocks']

    stocks_rates = []
    list_stocks = convert_stocks()

    for stock in user_stocks:
        for i in list_stocks:
            if i["symbol"] == stock:
                stocks_dict = {"stock": stock, "price": i['price']}
                stocks_rates.append(stocks_dict)
    return stocks_rates


def main():
    output = {
        'hello_message': get_hello(),
        'cards':
        'top_transactions': ,
        'currencies': get_actual_currencies_price(),
        'stock_prices': get_actual_stocks_price(),
    }

    print(output)


main()