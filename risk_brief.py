from portfolio_risk_engine import run_risk_analysis
from portfolio_news_agent import analyse_portfolio_news
from dotenv import load_dotenv
import anthropic

#load .env
load_dotenv()

#cerate anthropic client
client = anthropic.Anthropic()
