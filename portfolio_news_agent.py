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

    #Gets the 5 most recent news stories
    news = news[0:5]

    #initialize list for restructured news
    clean_news = []

    #Loops through each news story only getting the title and summary
    for i in news:

        #Gets the title
        title = i['content']['title']

        #Gets  summary
        summary = i['content']['summary']

        #Joins them together in one string
        result = title + " - "+ summary

        #Stores sting on list
        clean_news.append(result)

    #Returns list
    return clean_news

print(get_news("AAPL"))

tools = [
    {"name": "get_news",
     "description": "A function takes a string [ticker] parameter, gets the 5 most recent news articles about that ticker, and returns the title and summary of those articles.",
     "input_schema": {
         "type": "object",
         "properties": {
             "ticker": {
                 "type": "string",
                 "description": "A string that is the name of a stock in its abbreviated form for example Apple is AAPL"
             }
            },
         "required": ["ticker"]
        }
    }
    ]