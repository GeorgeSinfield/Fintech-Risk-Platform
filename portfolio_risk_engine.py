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

    #Multiply the standard deviation by square root of 252 to br the volatility
    result = returns_std * np.sqrt(252)

    #Retuns the volatility
    return result

#Runs calculate_volatility on returns and stores it
volatility = calculate_volatility(returns)

#Function to calculate correlation matrix
def calculate_correlation_matrix(returns):

    #Calculate correlation matrix using pandas .corr()
    result = returns.corr()

    #Return correlation matrix
    return result

#Run and store correlation matrix
correlation_matrix = calculate_correlation_matrix(returns)

#Function that calculates the historical VaR
def calculate_portfolio_var(returns, weights, confidence=0.95):

    #weighted portfolio returns for each day
    weighted_returns = returns.dot(weights)

    #Reverse the confidence valule
    percentile  = (1 - confidence) * 100

    #Finds var bassed of the weighted returns and confidence
    result = np.percentile(weighted_returns, percentile)

    #returns the var
    return result

#Run and store calculate_portfolio_var
portfolio_var = calculate_portfolio_var(returns, [0.4, 0.3, 0.3],)

#Function that calculates the max drawdown
def calculate_max_drawdown(prices):

    #Finds the maximum price
    max_price = prices.cummax()

    #Calculates diffrence of current price with max price
    current_dif = (prices - max_price) / max_price

    #Finds the minimun value across all days
    worst_drawdown = current_dif.min()

    #Returns worst drawdown
    return worst_drawdown

#Run and store calculate_max_drawdown
worst_drawdown = calculate_max_drawdown(prices)

#Print all fuunctions
print(" RETURNS ")
print(returns.head())
print("\n VOLATILITY ")
print(volatility)
print("\n CORRELATION MATRIX ")
print(correlation_matrix)
print("\n VAR ")
print(portfolio_var)
print("\n WORST DRAWDOWN ")
print(worst_drawdown)