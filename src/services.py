import logging
from datetime import datetime as dt

filepath_logger = "C:\\Users\\sereg\\OneDrive\\Рабочий стол\\transaction-analysis\\logs\\utils.log"
logger = logging.getLogger("utils")
file_handler = logging.FileHandler(filepath_logger, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)


def categories_in_data(data_operations: list[dict]) -> list:
    """Принимает данные об операциях и возвращает категории"""
    categories = []
    for data_operation in data_operations:
        if data_operation["Категория"] not in categories and str(data_operation["Категория"]) != "nan":
            categories.append(data_operation["Категория"])
    return categories


def filter_by_date(data_operations: list[dict]) -> list[dict]:
    """Принимает на вход с данными об операциях, обрабатывает пользовотельский ввод даты и возвращает сортированные\
    данные по дате за указанный месяц"""

    data_filter_by_date = []
    year = input("Введите год. Пример '2024'\n")
    month = input("Введите месяц. Пример '02'\n")
    if year.isdigit() and len(year) == 4 and month.isdigit() and len(month) == 2 and 1 <= int(month) <= 12:
        date = f"{year}.{month}"
        data_filter_by_date = [
            i
            for i in data_operations
            if dt.strptime(str(i["Дата операции"]), "%d.%m.%Y %H:%M:%S").strftime("%Y.%m") == date
        ]
    return data_filter_by_date


def analysis_categories_of_csshback(data: list[dict], categories: list) -> dict[str, float]:
    """Принимает на вход данные об операциях и категории, возвращает словарь с наиболее выгодными категориями\
     для кэшбэка"""
    top_categories_csshback = {}
    for i in range(0, len(categories)):
        amount = 0
        for d in data:
            if categories[i] == d["Категория"]:
                amount += d["Сумма операции с округлением"]
                top_categories_csshback[f"{categories[i]}"] = round(amount / 100, 2)
    top_categories_csshback = dict(sorted(top_categories_csshback.items(), key=lambda x: x[1], reverse=True))
    return top_categories_csshback
