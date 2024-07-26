import pandas as pd


def get_data(filename: str) -> list[dict]:
    """Принимает на вход путь до файла XLSX и возвращает список вложенных словарей"""
    data_xlsx = pd.read_excel(filename)
    data_operations = data_xlsx.to_dict(orient="records")
    return data_operations
