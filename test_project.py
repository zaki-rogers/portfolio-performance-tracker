import os
from project import add_holdings
from project import read_holdings
from project import fetch_price_history
from project import calculate_daily_values
from project import calculate_total_return

def test_add_holdings():
    if os.path.exists("test_holdings.csv"):
        os.remove("test_holdings.csv")

    add_holdings("test_holdings.csv", "VUAG.L", "10", "2025-01-01")
    add_holdings("test_holdings.csv", "VWRP.L", "5", "2025-02-01")

    holdings = read_holdings("test_holdings.csv")
    assert holdings == [
        {"ticker": "VUAG.L", "quantity": "10", "purchase_date": "2025-01-01"},
        {"ticker": "VWRP.L", "quantity": "5", "purchase_date": "2025-02-01"},
    ]


def test_read_holdings():
    with open("test_read.csv", "w") as file:
        file.write("ticker,quantity,purchase_date\n")
        file.write("VUAG.L,10,2025-01-01\n")
        file.write("VWRP.L,5,2025-02-01\n")

    holdings = read_holdings("test_read.csv")
    assert holdings == [
        {"ticker": "VUAG.L", "quantity": "10", "purchase_date": "2025-01-01"},
        {"ticker": "VWRP.L", "quantity": "5", "purchase_date": "2025-02-01"},
    ]


def test_fetch_price_history():
    result = fetch_price_history(["VUAG.L"], "2025-01-01", "2025-01-10")
    assert "VUAG.L" in result
    assert isinstance(result["VUAG.L"], dict)
    assert len(result["VUAG.L"]) > 0


def test_calculate_daily_values():
    holdings = [
        {"ticker": "VUAG.L", "quantity": "10", "purchase_date": "2025-01-01"},
        {"ticker": "VWRP.L", "quantity": "5", "purchase_date": "2025-01-02"},
    ]

    price_history = {
        "VUAG.L": {"2025-01-01": 100, "2025-01-02": 101},
        "VWRP.L": {"2025-01-01": 200, "2025-01-02": 202},
    }

    assert calculate_daily_values(holdings, price_history) == {"2025-01-01": 1000, "2025-01-02": 2020}


def test_calculate_total_return():
    daily_values = {"2025-01-01": 1000, "2025-01-02": 2020}
    assert calculate_total_return(daily_values) == 102.0