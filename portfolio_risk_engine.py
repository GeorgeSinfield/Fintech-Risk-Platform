import yfinance as yf
import pandas as pd
import numpy as np

#Function that takes prices and calculates the returns
def calculate_returns(prices):

    #Gets the daily percentage change in prices using
    pct_change = prices.pct_change()

    #Removes  any NaN rows
    result = pct_change.dropna()

    #Returns the returns
    return result

#Function that calculates the volatility of returns 
def calculate_volatility(returns):

    #Calculate standard deviation for each column
    returns_std = returns.std()

    #Multiply the standard deviation by square root of 252 to br the volatility
    result = returns_std * np.sqrt(252)

    #Returns the volatility
    return result

#Function to calculate correlation matrix
def calculate_correlation_matrix(returns):

    #Calculate correlation matrix using pandas .corr()
    result = returns.corr()

    #Return correlation matrix
    return result

#Function that calculates the historical VaR
def calculate_portfolio_var(returns, weights, confidence=0.95):

    #weighted portfolio returns for each day
    weighted_returns = returns.dot(weights)

    #Reverse the confidence value
    percentile  = (1 - confidence) * 100

    #Finds var based of the weighted returns and confidence
    result = np.percentile(weighted_returns, percentile)

    #Returns the var
    return result

#Function that calculates the max drawdown
def calculate_max_drawdown(prices):

    #Finds the maximum price
    max_price = prices.cummax()

    #Calculates difference of current price with max price
    current_dif = (prices - max_price) / max_price

    #Finds the minimum value across all days
    worst_drawdown = current_dif.min()

    #Returns worst drawdown
    return worst_drawdown

#Function that takes tickers and weights and runs a full risk analysis on the portfolio
def run_risk_analysis(tickers: list[str], weights: list[float]):

    #Download 1 year of price data on stocks
    prices = yf.download(tickers, period="1y")

    #Change prices to only include the Close prices
    prices = prices["Close"]   

    #Calculates the returns
    returns = calculate_returns(prices)

    #Returns the risk analysis
    return {
    "volatility": calculate_volatility(returns),
    "correlation_matrix": calculate_correlation_matrix(returns),
    "portfolio_var": calculate_portfolio_var(returns, weights),
    "max_drawdown": calculate_max_drawdown(prices)
    }

#Test
#result = run_risk_analysis(["AAPL", "JPM", "XOM"], [0.4, 0.3, 0.3])
#print("Volatility:\n", result["volatility"])
#print("\nCorrelation:\n", result["correlation_matrix"])
#print("\nVaR:\n", result["portfolio_var"])
#print("\nMax Drawdown:\n", result["max_drawdown"])