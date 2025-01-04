from datetime import datetime, timedelta

import yfinance as yf


def fetch_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)

    prices = stock_data["Close"]

    return prices


def calculate_return(prices):
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]

    stock_return = (end_price - start_price) / start_price

    return stock_return


def calculate_covariance(stock_prices):
    daily_returns = stock_prices.pct_change().dropna()

    covariance_matrix = daily_returns.cov()

    return covariance_matrix


if __name__ == "__main__":
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    prices = fetch_stock_data(["AAPL", "MSFT"], start_date, end_date)
    print(prices)
    print(calculate_return(prices))
    print(calculate_covariance(prices))
