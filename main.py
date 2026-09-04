from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from risk_brief import generate_risk_brief
import shutil
from rag_pipeline import process_pdf, extract_risk_categories

#Create a FastAPI instance
app = FastAPI()

#Class to define request model 
class PortfolioRequest(BaseModel):
    tickers: list[str]
    weights: list[float]

#POST endpoint at /risk-brief
@app.post("/risk-brief")

#Function that runs generate_risk_brief with parameters from PortfolioRequest
def run_risk_brief(request: PortfolioRequest):

    #Runs and stores generate_risk_brief
    result = generate_risk_brief(request.tickers, request.weights)

    #Returns risk brief
    return result

#POST endpoint at /upload-10k
@app.post("/upload-10k")

#Function that takes a file saves it then process it then runs extract_risk_categories on it and returns the risk_categories
async def upload_10k(company_name: str, file: UploadFile = File(...)):

    # save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #Runs and Stores process_pdf
    collection = process_pdf(temp_path, company_name)

    #Runs and stores extract_risk_categories
    risk_categories = extract_risk_categories(collection)

    #Returns risk_categories
    return risk_categories

