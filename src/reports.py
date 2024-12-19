import datetime
import json
import logging

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/src.reports.log", mode="w", encoding="UTF-8")
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def record_file(file_name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if file_name == None:
                filename = f'report_{result["Операция_1"]["Дата операции"]}'.replace(":", "")
            else:
                filename = file_name
            with open(f"../{filename}.json", "w", encoding="UTF-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)
            return result

        return wrapper

    return decorator


@record_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: str | None = None) -> dict:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    new_df = transactions[transactions["Категория"] == category]
    if date is None:
        date_now = datetime.datetime.now()
        date = date_now.strftime("%Y-%m-%d %H:%M:%S.%f")
        logger.info(f"переданная дата - сегодня {date}")

    date_operations = []
    end_date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    logger.info(f"Переданная дата - {end_date}")
    if end_date.month == 1:
        first_month = 10
        first_year = end_date.year - 1
        first_day_date = end_date.replace(month=first_month, year=first_year)
        logger.info(f"Дата по которую идет поиск - {first_day_date}")
        for index, operation in new_df.iterrows():
            if (
                first_day_date
                <= datetime.datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
                <= end_date
            ):
                date_operations.append(operation)
    elif end_date.month == 2:
        first_month = 11
        first_year = end_date.year - 1
        first_day_date = end_date.replace(month=first_month, year=first_year)
        logger.info(f"Дата по которую идет поиск - {first_day_date}")
        for index, operation in new_df.iterrows():
            if (
                first_day_date
                <= datetime.datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
                <= end_date
            ):
                date_operations.append(operation)
    else:
        first_month = end_date.month - 2

        first_day_date = end_date.replace(month=first_month)
        logger.info(f"Дата по которую идет поиск - {first_day_date}")
        for index, operation in new_df.iterrows():
            if (
                first_day_date
                <= datetime.datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
                <= end_date
            ):
                date_operations.append(operation)

    dict_operations = {}
    count_operations = 1
    for i in date_operations:
        dict_operations[f"Операция_{count_operations}"] = {}
        dict_operations[f"Операция_{count_operations}"]["Дата операции"] = i["Дата операции"]
        dict_operations[f"Операция_{count_operations}"]["Дата платежа"] = i["Дата платежа"]
        dict_operations[f"Операция_{count_operations}"]["Номер карты"] = i["Номер карты"]
        dict_operations[f"Операция_{count_operations}"]["Статус"] = i["Статус"]
        dict_operations[f"Операция_{count_operations}"]["Сумма операции"] = i["Сумма операции"]
        dict_operations[f"Операция_{count_operations}"]["Валюта операции"] = i["Валюта операции"]
        dict_operations[f"Операция_{count_operations}"]["Сумма платежа"] = i["Сумма платежа"]
        dict_operations[f"Операция_{count_operations}"]["Валюта платежа"] = i["Валюта платежа"]
        dict_operations[f"Операция_{count_operations}"]["Кэшбэк"] = i["Кэшбэк"]
        dict_operations[f"Операция_{count_operations}"]["Категория"] = i["Категория"]
        dict_operations[f"Операция_{count_operations}"]["MCC"] = i["MCC"]
        dict_operations[f"Операция_{count_operations}"]["Описание"] = i["Описание"]
        dict_operations[f"Операция_{count_operations}"]["Бонусы (включая кэшбэк)"] = i["Бонусы (включая кэшбэк)"]
        dict_operations[f"Операция_{count_operations}"]["Округление на инвесткопилку"] = i[
            "Округление на инвесткопилку"
        ]
        dict_operations[f"Операция_{count_operations}"]["Сумма операции с округлением"] = i[
            "Сумма операции с округлением"
        ]
        count_operations += 1
    logger.info("Создан словарь, который будет возвращать функция")
    return dict_operations
