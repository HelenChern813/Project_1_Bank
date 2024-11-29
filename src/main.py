from datetime import datetime

from src.reports import spending_by_category
from src.services import search_phone
from src.utils import file_df
from src.views import home_page


def main():
    """Основная функция для запуска реализованных функций"""

    print(
        """Для получения JSON-ответа "Главной" страницы введите 1;
    Для получения JSON-ответа с информацией по поиску транзакций по номеру телефона введите 2
    Для формирования файла с JSON-ответом по транзакциям за последние 3 месяца от нужной даты введите 3
    Чтобы выполнить все функции введиде 4"""
    )
    client = int(input("Введите нужную цифру: "))
    if client == 1:
        # Передайте в переменную путь до файла клиента
        file_path = "../data/operations.xlsx"
        df = file_df(file_path)
        # Для передачи другой даты - введите нужную дату
        date = str(datetime.now())
        date = str(datetime.strptime(date, "%d.%m.%Y %H:%M:%S"))
        home_page_client = home_page(df, file_path, date)
        return home_page_client
    elif client == 2:
        # Передайте в переменную путь до файла клиента
        file_path = "../data/operations.xlsx"
        df = file_df(file_path)
        search_phone_client = search_phone(df)
        return search_phone_client
    elif client == 3:
        # Передайте в переменную путь до файла клиента
        file_path = "../data/operations.xlsx"
        df = file_df(file_path)
        list_category = df["Категория"].unique()
        print(
            f"""Выберите иодну из категорий и введите ее название с большой буквы
{list_category}"""
        )
        category_client = input("Введите категорию: ")
        # Если нужно определенную дату, то передайте эту дату в парамерты функции
        # Если нужно взять текущую дату, то прсото не передавате этот параметр
        date = "31.12.2021 16:44:00"
        # Генерация файла. Если нужно задать имя файла, то передайте имя файла строкой в вызов декоратора функции
        spending_by_category(df, category_client, date)
    else:
        file_path = "../data/operations.xlsx"
        df = file_df(file_path)
        # Для передачи другой даты - введите нужную дату
        date = str(datetime.now())
        date = str(datetime.strptime(date, "%d.%m.%Y %H:%M:%S"))
        home_page_client = home_page(df, file_path, date)
        search_phone_client = search_phone(df)
        list_category = df["Категория"].unique()
        print(
            f"""Выберите иодну из категорий и введите ее название с большой буквы
        {list_category}"""
        )
        category_client = input("Введите категорию: ")
        # Если нужно определенную дату, то передайте эту дату в парамерты функции
        # Если нужно взять текущую дату, то прсото не передавате этот параметр
        date = "31.12.2021 16:44:00"
        # Генерация файла. Если нужно задать имя файла, то передайте имя файла строкой в вызов декоратора функции
        spending_by_category(df, category_client, date)
        return home_page_client, search_phone_client
