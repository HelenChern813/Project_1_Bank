import json
import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/src.services.log", mode="w", encoding="UTF-8")
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def search_phone(data: pd.DataFrame) -> json:
    """
    Принимает на вход DataFrame, осуществляет поиск операций на номер телефона и возвращает json-ответ
    """

    pattern = re.compile(r"(\s\+7\s|\s\+\s7\s)")

    list_phone_transaction = []
    list_index = []
    info_phone_transaction = {}

    for index, row in data.iterrows():
        if re.search(pattern=pattern, string=row["Описание"]):

            info_phone_transaction["Дата операции"] = row["Дата операции"]
            info_phone_transaction["Дата платежа"] = row["Дата платежа"]
            info_phone_transaction["Номер карты"] = row["Номер карты"]
            info_phone_transaction["Сумма платежа"] = row["Сумма платежа"]
            info_phone_transaction["Валюта платежа"] = row["Валюта платежа"]
            info_phone_transaction["Кэшбэк"] = row["Кэшбэк"]
            info_phone_transaction["Категория"] = row["Категория"]
            info_phone_transaction["Описание"] = row["Описание"]

            list_phone_transaction.append(info_phone_transaction)

            list_index.append(index)
    if len(list_index) == 0 or len(list_phone_transaction) == 0:
        logger.warning("Не правильно передан DataFrame")

    phone_transaction = {}
    for i in range(len(list_index)):
        phone_transaction[f"Операция_{i + 1}"] = {
            "index": f"{list_index[i]}",
            "краткая информация": f"{list_phone_transaction[i]}",
        }

    logger.info("Функция вернула json-ответ")
    return json.dumps(phone_transaction, indent=4, ensure_ascii=False)
