import json

import pytest

from src.reports import spending_by_category
from src.services import search_phone
from src.utils import file_df, open_file_json, unique_cards
from src.views import actual_df_mouth, home_page, info_cards, top_transactions

file_path = "../data/operations.xlsx"
df = file_df(file_path)
date = "30.11.2021 10:19:28"


@pytest.fixture
def df_file():
    return file_df(file_path)


@pytest.fixture()
def unique_cards_test():
    return unique_cards(file_path)


@pytest.fixture()
def open_file_json_test():
    return open_file_json()


@pytest.fixture()
def fix_actual_df_mouth():
    return actual_df_mouth(df, date)


@pytest.fixture()
def fix_info_cards():
    return info_cards(df, file_path, date)


@pytest.fixture()
def fix_top_transactions():
    return top_transactions(df, date)


@pytest.fixture()
def transaction_eur():
    return {"operationAmount": {"amount": 1.23, "currency": {"code": "EUR"}}}


@pytest.fixture()
def fix_home_page():
    return home_page(df, file_path, date)


@pytest.fixture()
def fix_search_phone():
    return search_phone(df)


@pytest.fixture()
def py_obj_search_phone():
    i = search_phone(df)
    py_obj = json.loads(i)
    return py_obj
