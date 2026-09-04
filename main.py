from fastapi import FastAPI
from pydantic import BaseModel
from risk_brief import generate_risk_brief

#Create a FastAPI instance
app = FastAPI()

#Class to define request model 
class PortfolioRequest(BaseModel):
    tickers: list[str]
    weights: list[float]


@app.post("/risk-brief")

#Function that runs generate_risk_brief with parameters from PortfolioRequest
def run_risk_brief(request: PortfolioRequest):

    #Runs and stores generate_risk_brief
    result = generate_risk_brief(request.tickers, request.weights)

    #Returns risk brief
    return result