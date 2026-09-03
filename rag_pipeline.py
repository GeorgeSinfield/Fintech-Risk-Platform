from pypdf import PdfReader
from sentence_transformers import SentenceTransformer , util
import chromadb
import anthropic
from dotenv import load_dotenv
import json

#load dotenv
load_dotenv()

#Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

#Create a chromadb client
chromadb_client = chromadb.PersistentClient(path="./chroma_db")

#Create a client for anthropic
anthropic_client = anthropic.Anthropic()

#Function to extract all text from pdf
def load_pdf (filepath):

    #Opens pdf
    reader = PdfReader(filepath)

    #Get's num of pages in pdf
    num_pages = len(reader.pages)

    #Define text string
    text = ""

    #Loops through every page and extracts the text
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text

#Function to chunk the text
def chunk_text(text, chunk_size=200, overlap=20):

    #Split text into words
    words = text.split()

    #Total number of words
    total_words = len(words)

    #Create list where chunks can be stored
    chunks = []

    #Create step variable
    step = chunk_size - overlap

    #Create start variable
    start = 0

    #Loop though words adding them to a chunk which will then be stored in chunks
    while start < total_words:
        chunks.append(" ".join(words[start:start + chunk_size]))
        start += step

    #Return chunks
    return chunks

#Function that process pdf by using load_pdf and chunk_text
def process_pdf(filepath, collection_name):

    #Runs load_pdf on file
    text = load_pdf(filepath)

    #Chunks the text
    chunks = chunk_text(text, chunk_size=200, overlap=20)

    #Embeds the chunks
    embeddings = model.encode(chunks)

    #Creates collection
    collection = chromadb_client.get_or_create_collection(collection_name)

    #Adds chunks and embeddings to collection 
    collection.add(
            documents = chunks,
            ids = [f"id{i}" for i in range(len(chunks))],
            embeddings = embeddings.tolist()  
        )

    #Returns collection 
    return collection

#Function to ask a question though anthropic api
def ask(question, collection):

    #embed question
    query_embeddings = model.encode(question)

    #query collection with question
    results = collection.query(query_embeddings = query_embeddings, n_results = 3)

    #turn query results into text
    relevant_info = "\n\n".join(results['documents'][0])

    #ask question and feed relevant info
    message = anthropic_client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    temperature=0.2,
    system="You are a financial risk analyst. Only state facts grounded in the provided text.",
    messages=[{"role": "user", "content": question + " use only this information: \n" + relevant_info}])

    #Return answer
    return message.content[0].text

#Function that queries for each risk type and runs ask using the queried chunks
def extract_risk_categories(collection):

    #Define risk_categories 
    risk_categories = {"market_risk": "", "credit_risk": "", "regulatory_risk": "", "operational_risk": "", "liquidity_risk": ""}

    #For each risk category run ask and save result then return all results
    for key in risk_categories:
        result = ask(f"what does this company say about {key}?", collection)
        risk_categories[key] = result

    return(risk_categories)

#Test
if __name__ == "__main__": 

    #Runs and stores process_pdf
    collection = process_pdf("goldman_bdc_10k.pdf", "goldman_bdc")

    #Runs and stores extract_risk_categories
    risk_data = extract_risk_categories(collection)

    #Formats extract_risk_categories creates a json file for output 
    with open("goldman_bdc_risk.json", "w") as f:
        f.write(json.dumps(risk_data, indent=2))

    #Print test
    print("Risk categories saved to goldman_bdc_risk.json")