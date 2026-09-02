from portfolio_risk_engine import run_risk_analysis
from portfolio_news_agent import analyse_portfolio_news
from dotenv import load_dotenv
import anthropic

#load .env
load_dotenv()

#cerate anthropic client
client = anthropic.Anthropic()

#Function that calls portfolio_news_agent and portfolio_risk_engine then feeds that data to claude to make a risk brief
def generate_risk_brief(tickers, weights):

    #Calls run_risk_analysis and stores it 
    risk_data = run_risk_analysis(tickers, weights)

    #Calls analyse_portfolio_news and stores it
    news_data = analyse_portfolio_news(tickers)

    #Message to claude
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        temperature=0.2,
        system= "You are a senior portfolio risk analyst. Write clearly and concisely. Only use the data provided.",
        messages=[
            {"role": "user", 
             "content": 
             f"Portfolio risk metrics:\n" 
             f"Volatility:\n{risk_data['volatility'].to_string()}\n" 
             f"Correlation Matrix:\n{risk_data['correlation_matrix'].to_string()}\n" 
             f"VaR: {round(float(risk_data['portfolio_var']), 4)}\n" 
             f"Max Drawdown:\n{risk_data['max_drawdown'].to_string()}\n\n"
             f"News risk analysis:\n{news_data}\n"
             f"Write a 4-paragraph risk brief for a portfolio manager covering:\n1. Overall risk level\n2. Main risk drivers\n3. Key news events to watch\n4. One actionable recommendation"}]
    )

    #Return response from claude
    return message.content[0].text

#Test
print(generate_risk_brief(["AAPL", "JPM", "XOM"], [0.4,0.3,0.3]))