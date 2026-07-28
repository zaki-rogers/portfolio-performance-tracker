import yfinance as yf
import matplotlib.pyplot as plt
import csv
import os
from datetime import date


def main():
    while True:
        tickers = input("Ticker Symbol: ")
        quantity = input("Quantity of Holdings: ")
        purchase_date = input("Date of Purchase: ")
        add_holdings("holdings.csv", tickers, quantity, purchase_date)

        again = input("Add another holding? (y/n): ")
        if again.lower() != "y":
            break

    holdings = read_holdings("holdings.csv")
    tickers = [holding["ticker"] for holding in holdings]

    purchase_dates = [holding["purchase_date"] for holding in holdings]
    start = min(purchase_dates)
    end = date.today().strftime("%Y-%m-%d")

    price_history = fetch_price_history(tickers, start, end)
    daily_values = calculate_daily_values(holdings, price_history)
    total_return = calculate_total_return(daily_values)

    print(f"Total return: {total_return:.2f}%")
    plot_portfolio_value(daily_values)


def add_holdings(filepath, tickers, quantity, purchase_date):
    """Append a new holding to a CSV file, writing a header row if the file doesn't exist yet."""

    file_exists = os.path.exists(filepath)

    with open(filepath, "a") as file:
        writer = csv.DictWriter(file, fieldnames=["ticker", "quantity", "purchase_date"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"ticker": tickers, "quantity": quantity, "purchase_date": purchase_date})


def read_holdings(filepath):
    """Read all holdings from a CSV file and return them as a list of dictionaries."""
    
    holdings = []
    
    with open(filepath) as file:
        reader = csv.DictReader(file)
        for row in reader:
            holdings.append(row)
        return holdings
    

def fetch_price_history(tickers, start, end):
    """Fetch historical closing prices from Yahoo Finance and return them as a nested dictionary of {ticker: {date: price}}."""

    price_history = {}
    
    stock_price_data = yf.download(tickers, start=start, end=end)
    if stock_price_data is None:
        raise ValueError("Failed to fetch price data")
    close_prices = stock_price_data["Close"]
    
    for ticker in close_prices:
        ticker_prices = close_prices[ticker]
        prices_by_date = {}
        
        for date, price in ticker_prices.items():
            prices_by_date[date.strftime("%Y-%m-%d")] = price
        price_history[ticker] = prices_by_date

    return price_history


def calculate_daily_values(holdings, price_history):
    """Calculate total portfolio value for each date, counting only holdings already purchased by that date."""

    daily_values = {}
    last_known_price = {}

    first_ticker = holdings[0]["ticker"]
    dates = price_history[first_ticker].keys()

    for date in dates:
        total = 0
        for holding in holdings:
            if holding["purchase_date"] <= date:
                ticker = holding["ticker"]
                price_at_date = price_history[ticker][date]

                if price_at_date == price_at_date:
                    last_known_price[ticker] = price_at_date
                elif ticker in last_known_price:
                    price_at_date = last_known_price[ticker]
                else:
                    continue

                quantity = float(holding["quantity"])
                value = price_at_date * quantity
                total += value
        daily_values[date] = total

    return daily_values


def calculate_total_return(daily_values):
    """Calculate the percentage return between the earliest and most recent portfolio values."""

    dates_list = list(daily_values.keys())
    earliest_date = dates_list[0]
    latest_date = dates_list[-1]
    earliest_value = daily_values[earliest_date]
    latest_value = daily_values[latest_date]

    total_return = (latest_value - earliest_value) / earliest_value * 100
    return total_return


def plot_portfolio_value(daily_values):
    """Plot total portfolio value over time and save the chart as an image."""

    dates = list(daily_values.keys())
    values = list(daily_values.values())

    plt.plot(dates, values)
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.title("Portfolio Value Over Time")
    plt.xticks([dates[0], dates[-1]])
    plt.tight_layout()
    plt.savefig("portfolio_value.png")


if __name__ == "__main__":
    main()