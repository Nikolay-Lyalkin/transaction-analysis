import json
import logging
from datetime import datetime as dt
from datetime import timedelta
from functools import wraps
from typing import Any, Never, Union

import pandas as pd

filepath_logger = "C:\\Users\\sereg\\OneDrive\\Рабочий стол\\transaction-analysis\\logs\\reports.log"
logger = logging.getLogger("reports")
file_handler = logging.FileHandler(filepath_logger, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)


def decorators_write_file(file_path: str) -> Any:
    """Принимает путь для сохранения json файла"""

    def wrapper(func: Any) -> Any:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict("records")
            with open(file_path, "w", encoding="utf-8") as f_obj:
                json.dump(result, f_obj, ensure_ascii=False)
            return result

        return inner

    return wrapper


def data_dataframe(filename: str) -> Union[pd.DataFrame, list[Never]]:
    """Принимает путь до EXCEL файла и возвращает DataFrame"""
    try:
        excel_data = pd.read_excel(filename)
    except FileNotFoundError as ex:
        logger.error(f"{filename} вызывает {ex}")
        return []
    else:
        return excel_data


@decorators_write_file("C:/Users/sereg/OneDrive/Рабочий стол/transaction-analysis/data/reports.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Any = None) -> pd.DataFrame:
    """Принимает DataFrame с двнными, категорию и дату, возвращает сумму трат по данной категории за последние\
     три месяца"""
    sum_by_category = 0
    if not date:
        date = dt.now()
    else:
        date = dt.strptime(date, "%d.%m.%Y")
    int_day = int(date.strftime("%d"))
    time_del = timedelta(days=int_day + 60)
    for i in range(len(transactions)):
        if (
            date >= dt.strptime(str(transactions.loc[i, "Дата операции"]), "%d.%m.%Y %H:%M:%S")
            and dt.strptime(str(transactions.loc[i, "Дата операции"]), "%d.%m.%Y %H:%M:%S") >= date - time_del
        ):
            if str(transactions.loc[i, "Категория"]).lower() == category.lower():
                sum_by_category += float(transactions.loc[i, "Сумма операции с округлением"])
    return pd.DataFrame({"Категория": [category], "Cумма трат": round(sum_by_category, 2)})
