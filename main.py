from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from risk_brief import generate_risk_brief
import shutil
from rag_pipeline import process_pdf, extract_risk_categories, ask, chromadb_client
import yfinance as yf
from fastapi.middleware.cors import CORSMiddleware

#Create a FastAPI instance
app = FastAPI()

#Enable CORS to access frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def upload_10k(company_name: str = Form(...), file: UploadFile = File(...)):

    # save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #Removes spaces from company name
    clean_name = company_name.lower().replace(" ", "_")

    #Runs and Stores process_pdf
    collection = process_pdf(temp_path, clean_name)

    #Runs and stores extract_risk_categories
    risk_categories = extract_risk_categories(collection)

    #Returns risk_categories
    return risk_categories

#GET endpoint at /search-ticker
@app.get("/search-ticker")

#Function that takes search string and returns ticker matching with matching company names
def search_ticker(query: str):

    #Runs search of query and stores it 
    result = yf.Search(query)

    #Returns result in a list companies and their tickers
    return result.quotes

#Class to define AskRequest model
class AskRequest(BaseModel):
    question: str
    collection_name: str

#POST Endpoint at /ask
@app.post("/ask")

#Function that that takes request and runs ask on request as a question 
def ask_question(request: AskRequest):

    #Gets existing ChromaDB collection for company if it exists instead of making a new one
    collection = chromadb_client.get_or_create_collection(request.collection_name)

    #Runs and stores ask
    answer = ask(request.question, collection)

    #Returns answer form Claude API
    return {"answer": answer}
