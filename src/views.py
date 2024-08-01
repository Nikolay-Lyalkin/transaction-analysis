import json
from datetime import datetime as dt
from typing import Any

from src.utils import (
    currency_rate,
    filter_by_date,
    get_currency_stock_data,
    get_data,
    greeting,
    last_digit_card,
    payment_amount,
    stock_prices,
    top_transactions,
)


def main_page(date: str) -> Any:
    """Главная страница"""
    # Приветствие в зависимости от времени суток
    greeting_main_page = greeting(date=dt.now())

    # Получение данных о транзациях в формате list[dict]
    data = get_data("C:/Users/sereg/OneDrive/Рабочий стол/transaction-analysis/data/operations.xlsx")

    # Возвращает отфильрованный список за данный месяц
    filter_data_by_date = filter_by_date(date, data)

    # Возвращает номера карт используемых в данном месяце
    num_cards = last_digit_card(filter_data_by_date)

    # Возвращает сумму платежей по каждой карте
    payment_amount_by_cards = payment_amount(filter_data_by_date, num_cards)

    # Возвращает топ-5 транзакций этого месяца
    top5_transactions_this_month = top_transactions(filter_data_by_date)

    # Принимает путь к файлу user_setting.json и возвращает словарь со списком валют и ценных бумаг
    currency_stock_data = get_currency_stock_data(
        "C:/Users/sereg/OneDrive/Рабочий стол/transaction-analysis/user_settings.json"
    )

    # Принимает словарь со списком валют и ценных бумаг, возвращает отношение рубля к иностранной валюте
    currency_rate_rub = currency_rate(currency_stock_data)

    # Принимает словарь со списком валют и ценных бумаг, возвращает стоимость ценных бумаг
    stock_prices_ = stock_prices(currency_stock_data)

    result = {
        "greeting": greeting_main_page,
        "cards": payment_amount_by_cards,
        "top_transactions": top5_transactions_this_month,
        "currency_rates": currency_rate_rub,
        "stock_prices": stock_prices_,
    }
    with open(
        "C:/Users/sereg/OneDrive/Рабочий стол/transaction-analysis/data/main_page.json", "w", encoding="utf-8"
    ) as f_obj:
        json.dump(result, f_obj, ensure_ascii=False)
    return result
