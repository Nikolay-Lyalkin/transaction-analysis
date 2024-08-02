from unittest.mock import patch

from src.reports import data_dataframe


@patch("pandas.read_excel")
def test_get_dataframe(mock_xlsx):
    """Функуия-тест для проверки. что xlsx-файл читается корректно"""
    mock_xlsx.return_value = {"Yes": [50, 21], "No": [131, 2]}
    assert data_dataframe("operations.xlsx") == {"Yes": [50, 21], "No": [131, 2]}
