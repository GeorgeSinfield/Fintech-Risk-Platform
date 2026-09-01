import yfinance as yf
import pandas as pd
import numpy as np

prices = yf.download(["AAPL", "JPM", "XOM"], period="1y")
prices = prices["Close"]

def calculate_returns(prices):
    pct_change = prices.pct_change()
    result = pct_change.dropna()
    return result

returns = calculate_returns(prices)
print(returns.head())

