import yfinance as yf
import anthropic
from dotenv import load_dotenv

#load .env
load_dotenv()

#cerate anthropic client
client = anthropic.Anthropic()


#Function that gets news about a ticker
def get_news(ticker):

    #Creates a yf ticker object
    ticker = yf.Ticker(ticker)

    #Gets the news of the ticker 
    news = ticker.news

    news = news[0:5]
    clean_news = []

    for i in news:
        title = i['content']['title']
        summary = i['content']['summary']
        result = title + " - "+ summary
        clean_news.append(result)
    
    return clean_news

print(get_news("AAPL"))