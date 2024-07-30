import json
import logging
import os
from datetime import datetime as dt
from datetime import timedelta
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

filepath_logger = "C:\\Users\\sereg\\OneDrive\\Рабочий стол\\transaction-analysis\\logs\\utils.log"
logger = logging.getLogger("utils")
file_handler = logging.FileHandler(filepath_logger, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)


def get_data(filename: str) -> Any:
    """Принимает на вход путь до файла XLSX и возвращает список вложенных словарей"""
    data_operations = []
    try:
        data_xlsx = pd.read_excel(filename)
    except FileNotFoundError as ex:
        logger.error(f"{filename} вызывает {ex}")
        return data_operations
    else:
        data_operations = data_xlsx.to_dict(orient="records")
    return data_operations


def greeting(date: Any = dt.now()) -> Any:
    """Приветствует в зависимости от текущего времени"""
    hour_now = date.strftime("%H")
    if 6 <= int(hour_now) < 12:
        return "Доброе утро"
    elif 12 <= int(hour_now) <= 18:
        return "Добрый день"
    elif 19 <= int(hour_now) <= 23:
        return "Добрый вечер"
    elif 0 <= int(hour_now) <= 5:
        return "Доброй ночи"


def filter_by_date(date: str, data_operations: list[dict]) -> list[dict]:
    """Возвращает операции за данный месяц"""
    filter_data_operations = []
    try:
        date_dt = dt.strptime(date, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        logger.error(f"Неверный формат даты - {date}")
        return filter_data_operations
    else:
        int_day = int(date_dt.strftime("%d"))
        time_del = timedelta(days=int_day - 1)
        for data_operation in data_operations:
            if (
                date_dt >= dt.strptime(str(data_operation["Дата операции"]), "%d.%m.%Y %H:%M:%S")
                and dt.strptime(str(data_operation["Дата операции"]), "%d.%m.%Y %H:%M:%S") >= date_dt - time_del
            ):
                filter_data_operations.append(data_operation)
        return filter_data_operations


def last_digit_card(data_operations: list[dict]) -> list:
    """Принимает данные об операциях и возвращает номера карт"""
    num_card = []
    for data_operation in data_operations:
        if data_operation["Номер карты"] not in num_card and str(data_operation["Номер карты"]) != "nan":
            num_card.append(data_operation["Номер карты"])
    return num_card


def payment_amount(data_operations: list[dict], num_cards: list) -> list[dict]:
    """Принимает данные об операциях и номера карт, возвращает сумму платежей по каждой карте"""
    list_sum_by_card = []
    for i in range(0, len(num_cards)):
        sum_operations = 0
        for data_operation in data_operations:
            if num_cards[i] == data_operation["Номер карты"]:
                sum_operations += data_operation["Сумма операции"]
        if sum_operations < 0:
            cashback = round(sum_operations * -1 / 100, 2)
        else:
            cashback = round(sum_operations / 100, 2)
        dict_sum_by_card = {
            "last_digits": str(num_cards[i])[1:],
            "total_spent": round(sum_operations, 2),
            "cashback": cashback,
        }
        list_sum_by_card.append(dict_sum_by_card)
    return list_sum_by_card


def top_transactions(filter_data_operations: list[dict]) -> list[dict]:
    """Принимает отфильтрованные по дате данные и возвращает топ-5 транзакций"""
    sorted_operations = sorted(filter_data_operations, key=lambda x: x["Сумма операции с округлением"], reverse=True)[
        0:5
    ]
    list_top5_operations = []
    for sorted_operation in sorted_operations:
        dict_top5_operations = {
            "date": sorted_operation["Дата операции"],
            "amount": sorted_operation["Сумма операции"],
            "category": sorted_operation["Категория"],
            "description": sorted_operation["Описание"],
        }
        list_top5_operations.append(dict_top5_operations)
    return list_top5_operations


def get_currency_stock_data(filename: str) -> Any:
    """Принимает путь к файлу user_setting.json и возвращает словарь со списком валют и ценных бумаг"""
    try:
        with open(filename, "r", encoding="utf-8") as f_obg:
            data_currency_stock = json.load(f_obg)
    except FileNotFoundError as ex:
        logger.error(f"{filename} вызывает {ex}")
        return []
    else:
        return data_currency_stock


def currency_rate(currency: Any) -> list[dict[str, Any]]:
    """Принимает словарь со списком валют и ценных бумаг, возвращает отношение рубля к иностранной валюте"""
    list_currency_rate = []
    load_dotenv()
    apikey = os.getenv("API_KEY_CURRENCY_RATE")
    try:
        for v in currency["user_currencies"]:
            url = f"https://currate.ru/api/?get=rates&pairs={v}RUB&key={apikey}"
            response = requests.get(url)
            result_convert = response.json()
            dict_currency_rate = {"currency": v, "rate": result_convert["data"][f"{v}RUB"]}
            list_currency_rate.append(dict_currency_rate)
    except TypeError as ex:
        logger.error(f"{ex}")
        return []
    else:
        return list_currency_rate


def stock_prices(stock: Any) -> Any:
    """Принимает словарь со списком валют и ценных бумаг, возвращает стоимость ценных бумаг"""
    list_stock_price = []
    load_dotenv()
    apikey = os.getenv("API_KEY_STOCK_PRICES")
    try:
        for v in stock["user_stocks"]:
            symbol = v
            api_url = "https://api.api-ninjas.com/v1/stockprice?ticker={}".format(symbol)
            response = requests.get(api_url, headers={"X-Api-Key": apikey})
            result_convert = response.json()
            dict_stock_price = {"stock": v, "price": result_convert["price"]}
            list_stock_price.append(dict_stock_price)
    except TypeError as ex:
        logger.error(f"{ex}")
        return []
    return list_stock_price
