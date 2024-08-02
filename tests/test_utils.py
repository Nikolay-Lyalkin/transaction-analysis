from unittest.mock import mock_open, patch
import pytest
from datetime import datetime as dt

from src.utils import (
    currency_rate,
    filter_by_date,
    get_currency_stock_data,
    get_data,
    greeting,
    last_digit_card,
    payment_amount,
    stock_prices,
)


@patch("pandas.read_excel")
def test_get_data(mock_xlsx):
    """Функуия-тест для проверки. что xlsx-файл читается корректно"""
    mock_xlsx.return_value.to_dict.return_value = {
        "Дата операции": "31.12.2021 16:44:00",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -160.89,
        "Валюта операции": "RUB",
        "Сумма платежа": -160.89,
        "Валюта платежа": "RUB",
        "Кэшбэк": "nan",
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 3,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 160.89,
    }
    assert get_data("filename.xlsx") == {
        "Дата операции": "31.12.2021 16:44:00",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -160.89,
        "Валюта операции": "RUB",
        "Сумма платежа": -160.89,
        "Валюта платежа": "RUB",
        "Кэшбэк": "nan",
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 3,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 160.89,
    }


@pytest.mark.parametrize(
    "date, test_greeting",
    [
        (dt.strptime("2018-07-11T02:26:18.671407", "%Y-%m-%dT%H:%M:%S.%f"), "Доброй ночи"),
        (dt.strptime("2018-07-11T07:26:18.671407", "%Y-%m-%dT%H:%M:%S.%f"), "Доброе утро"),
        (dt.strptime("2018-07-11T14:26:18.671407", "%Y-%m-%dT%H:%M:%S.%f"), "Добрый день"),
        (dt.strptime("2018-07-11T20:26:18.671407", "%Y-%m-%dT%H:%M:%S.%f"), "Добрый вечер"),
    ],
)
def test_greeting(date, test_greeting):
    """Тестирует приветсвие в зависимости от времени дня"""
    assert greeting(date=date) == test_greeting


def test_filter_by_date(data):
    """Тестирует фильтр по дате"""
    assert filter_by_date("17.07.2019 23:59:59", data) == [
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


def test_last_digit_card(data):
    """Тестирует возврат номеров карт"""
    assert last_digit_card(data) == ["*7197", "*4556"]


def test_payment_amount(data, num_cards):
    """Тестирует возврат суммы платежей по каждой карте"""
    assert payment_amount(data, num_cards) == [
        {"last_digits": "7197", "total_spent": -25.0, "cashback": 0.25},
        {"last_digits": "4556", "total_spent": -305.0, "cashback": 3.05},
    ]


@patch("requests.get")
def test_currency_rate(mock_get):
    """Тестирование возвращает ли функция курс иностранной валюты по отношению к рублю"""
    mock_get.return_value.json.return_value = {"status": 200, "message": "rates", "data": {"USDRUB": "64.1824"}}
    assert currency_rate({"user_currencies": ["USD"]}) == [{"currency": "USD", "rate": "64.1824"}]


@patch("requests.get")
def test_stock_prices(mock_get):
    """Тестрование возвращает ли функция стоимость ценных бумаг"""
    mock_get.return_value.json.return_value = {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "price": 218.24,
        "exchange": "NASDAQ",
        "updated": 1722283201,
    }
    assert stock_prices({"user_stocks": ["AAPL"]}) == [{"stock": "AAPL", "price": 218.24}]


def test_get_currency_stock_data():
    """Функуия-тест для проверки. что json-файл читается корректно"""
    mock_data = '[{"user_currencies": ["USD", "EUR"],' '"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        data = get_currency_stock_data("path_to_file.json")
        assert data == [{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}]
