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

#List of tools
tools = [
    #get_news tool
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

#Function that checks news about ticker for risk
def check_news_for_risk(ticker):

    #Initial message to Claude with tools list
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0.2,
        system="You are a financial risk analyst. Only state facts grounded in the provided text.",
        tools=tools,
        messages=[
            {"role": "user","content": f"Check the latest news for {ticker} and identify any items that could represent a risk to an investor holding this stock."}
            ],
    )

    #Check is claude stopped because it wants to use a tool
    if message.stop_reason == "tool_use":
        #Finds where claude wants to use tool
        for i in message.content:
            if i.type == "tool_use":
                #Runs tool with the argument claude wants to use
                run_tool = get_news(i.input["ticker"])

                #Sends the results back to claude
                final_message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    temperature=0.2,
                    tools=tools,
                    system="You are a financial risk analyst. Only state facts grounded in the provided text.",
                    messages=[
                        {"role": "user", "content":  f"Check the latest news for {ticker} and identify any items that could represent a risk to an investor holding this stock."},
                        {"role": "assistant", "content": message.content},
                        {"role": "user", "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": i.id,
                                "content": str(run_tool)
                            }
                        ]}
                    ]
                )

                #return claude's response 
                return final_message.content[0].text

#Function to call check news for risk on multiple tickers at the same time  
def analyse_portfolio_news(tickers):

    #Defines result variable 
    result = {}

    #loop that calls check_news_for_risk on each ticker
    for i in tickers:
        result[i] = check_news_for_risk(i)

    #Returns analysis
    return result

#Test
print(analyse_portfolio_news(["AAPL", "JPM", "XOM"]))