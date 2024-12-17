def test_unique_cards_test(unique_cards_test):

    assert str(unique_cards_test) == "['*7197' '*5091' 0.0 '*4556']"


def test_open_file_json(open_file_json_test):

    assert open_file_json_test == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }
