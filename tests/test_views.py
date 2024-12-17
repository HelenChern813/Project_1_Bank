from unittest.mock import MagicMock, patch

from src.views import convert_exchange_rate, get_actual_currencies_price, get_actual_stocks_price, get_hello


def test_get_hello():
    assert get_hello("2024-12-17 00:09:54.176892") == "Доброй ночи"
    assert get_hello("31.12.2021 15:44:39") == "Добрый день"
    assert get_hello("31.12.2021 10:44:39") == "Доброе утро"
    assert get_hello("31.12.2021 18:44:39") == "Добрый вечер"
    assert get_hello("31.12.2021 23:44:39") == "Доброй ночи"


def test_actual_df_mouth(fix_actual_df_mouth):
    assert type(fix_actual_df_mouth) == type([])
    assert len(fix_actual_df_mouth) >= 1
    assert fix_actual_df_mouth[0]["Номер карты"] == "*4556"
    assert fix_actual_df_mouth[3]["Номер карты"] == "*5091"


def test_info_cards(fix_info_cards):
    assert type(fix_info_cards) == type([])
    assert len(fix_info_cards) >= 1
    assert fix_info_cards[0]["last_digits"] == "*7197"
    assert fix_info_cards[1]["last_digits"] == "*5091"
    assert fix_info_cards[2]["last_digits"] == "*4556"


def test_top_transactions(fix_top_transactions):
    assert type(fix_top_transactions) == type([])
    assert len(fix_top_transactions) >= 1
    assert fix_top_transactions == [
        {"amount": -8275.76, "category": "ЖКХ", "date": "12.11.2021 18:34:59", "description": "ЖКУ Квартира"},
        {"amount": 10000.0, "category": "Другое", "date": "03.11.2021 13:59:23", "description": "Иван С."},
        {
            "amount": -50000.0,
            "category": "Переводы",
            "date": "17.11.2021 16:38:23",
            "description": "Пополнение вклада",
        },
        {
            "amount": 50000.08,
            "category": "Переводы",
            "date": "22.11.2021 22:02:00",
            "description": "Закрытие вклада Тинькофф Банк",
        },
        {
            "amount": 126105.03,
            "category": "Переводы",
            "date": "22.11.2021 22:05:42",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
    ]


@patch("requests.get")
def test_convert_exchange_rate(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 1.0}}
    mock_get.return_value = mock_response

    assert convert_exchange_rate("USD") == 1.0


@patch("src.views.convert_exchange_rate")
def test_get_actual_currencies_price(convert_mock):
    convert_mock.return_value = 100

    assert get_actual_currencies_price()[0]["currency"] == "USD"
    assert get_actual_currencies_price()[0]["rate"] == 100
    assert get_actual_currencies_price()[1]["currency"] == "EUR"
    assert get_actual_currencies_price()[1]["rate"] == 100


def test_get_actual_stocks_price():

    assert get_actual_stocks_price()[0]["stock"] == "AAPL"
    assert type(get_actual_stocks_price()[0]["price"]) == type(0.0)
    assert get_actual_stocks_price()[1]["stock"] == "AMZN"
    assert type(get_actual_stocks_price()[1]["price"]) == type(0.0)
    assert get_actual_stocks_price()[2]["stock"] == "GOOGL"
    assert type(get_actual_stocks_price()[2]["price"]) == type(0.0)
    assert get_actual_stocks_price()[3]["stock"] == "MSFT"
    assert type(get_actual_stocks_price()[3]["price"]) == type(0.0)
    assert get_actual_stocks_price()[4]["stock"] == "TSLA"
    assert type(get_actual_stocks_price()[4]["price"]) == type(0.0)


def test_fix_home_page(fix_home_page):
    assert type(fix_home_page) == type("")
    assert len(fix_home_page) >= 1
