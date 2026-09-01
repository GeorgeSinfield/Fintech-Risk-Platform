import yfinance as yf
import pandas as pd
import numpy as np

#Download 1 year of price data on stocks"
prices = yf.download(["AAPL", "JPM", "XOM"], period="1y")

#Change prices to only include the Close prices
prices = prices["Close"]

#Function that takes prices and calculates the returns
def calculate_returns(prices):

    #Gets the daily percentage change in prices using
    pct_change = prices.pct_change()

    #Remives any NaN rows
    result = pct_change.dropna()

    #Returns result
    return result

#Runs calculate_returns on prices
returns = calculate_returns(prices)