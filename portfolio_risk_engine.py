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

    #Returns the returns
    return result

#Runs calculate_returns on prices and stores it
returns = calculate_returns(prices)

#Function that calculates the volatility of returns 
def calculate_volatility(returns):

    #Calculate standard deviation for each column
    returns_std = returns.std()

    #Muultplys the standard deviation by square root of 252 to br the volatility
    result = returns_std * np.sqrt(252)

    #Retuns the volatility
    return result

#Runs calculate_volatility on returns and stores it
volatility = calculate_volatility(returns)
print(volatility)