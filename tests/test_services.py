def test_search_phone(fix_search_phone):
    assert type(fix_search_phone) == type("")


def test_py_obj_search_phone(py_obj_search_phone):
    assert py_obj_search_phone["Операция_1"]["index"] == "259"
    assert py_obj_search_phone["Операция_24"]["index"] == "5002"
    assert py_obj_search_phone["Операция_30"]["index"] == "6309"
    assert py_obj_search_phone["Операция_16"]["index"] == "2138"
