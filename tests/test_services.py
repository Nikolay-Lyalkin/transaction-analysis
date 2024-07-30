from unittest.mock import patch

from src.services import analysis_categories_of_csshback, categories_in_data, filter_by_date


def test_categories_in_data(data):
    """Тестирует возвращает ли функция категории транзакций"""
    assert categories_in_data(data) == ["Дом и ремонт", "Переводы"]


def test_analysis_categories_of_csshback(data):
    """"""
    assert analysis_categories_of_csshback(data, ["Дом и ремонт", "Переводы"]) == {
        "Дом и ремонт": 0.25,
        "Переводы": 3.05,
    }


@patch("builtins.input")
def test_filter_by_date(m_input, data):
    m_input.side_effect = ["2019", "07"]
    assert filter_by_date(data) == [
        {
            "Дата операции": "17.07.2019 15:05:27",
            "Дата платежа": "19.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -25.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -25.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Дом и ремонт",
            "MCC": 5200.0,
            "Описание": "OOO Nadezhda",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 25.0,
        }
    ]
