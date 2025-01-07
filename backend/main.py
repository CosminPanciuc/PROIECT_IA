from datetime import datetime, timedelta

import numpy as np
import yfinance as yf
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.pso import PSO


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
    daily_returns = stock_prices.pct_change().dropna() * 10

    covariance_matrix = daily_returns.cov()

    return np.array(covariance_matrix)


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PortfolioInput(BaseModel):
    symbols: list = ("NVDA", "AMD", "MSFT")
    risk: float | None = 1000
    num_particles: int | None = 50
    iter: int | None = 100


@app.post("/optimize")
def optimize_portfolio(data: PortfolioInput):
    start_date = (datetime.now() - timedelta(days=365 * 5)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")

    stock_prices = fetch_stock_data(data.symbols, start_date, end_date)
    print(stock_prices)

    returns = np.array([calculate_return(stock_prices[symbol]) for symbol in stock_prices])

    covariance = calculate_covariance(stock_prices)

    pso = PSO(
        num_particles=data.num_particles,
        num_assets=len(data.symbols),
        returns=returns,
        covariance=covariance,
        risk=data.risk,
        iter=data.iter,
    )

    optimal_allocation = pso.optimize()
    # pso.plot_positions()
    # pso.plot_positions_3d()

    return {
        "symbols": data.symbols,
        "allocation": optimal_allocation.tolist(),
    }
