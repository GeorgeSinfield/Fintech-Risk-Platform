from pypdf import PdfReader
from sentence_transformers import SentenceTransformer , util
import chromadb
import anthropic
from dotenv import load_dotenv

#Function to extract all text from pdf
def load_pdf (filepath):

    #Opens pdf
    reader = PdfReader(filepath)

    #Get's num of pages in pdf
    num_pages = len(reader.pages)

    #Define text string
    text = ""

    #Loops through every page and extracs the text
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text

#Run load pdf function on pdf
text = load_pdf("goldman_bdc_10k.pdf")

#Function to chunk the text
def chunk_text(text, chunk_size=200, overlap=20):

    #Split text into words
    words = text.split()

    #Total number of words
    total_words = len(words)

    #Create list where chunks can be stored
    chunks = []

    #Create step varible
    step = chunk_size - overlap

    #Create start varible
    start = 0

    #Loop though words adding them to a chunk which will then be stoerd in chiunks
    while start < total_words:
        chunks.append(" ".join(words[start:start + chunk_size]))
        start += step

    #Retun chunks
    return chunks

#Run chunk function on pdf text
chunks = chunk_text(text)

#Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

#embed chunks
embeddings = model.encode(chunks)

#Create a chromadb client
chromadb_client = chromadb.Client()

#Create a collection in chromadb to hold the goldman embeddings
collection = chromadb_client.create_collection("goldman_bdc")

#Add embedings to collection
collection.add(
    documents = chunks,
    ids = [f"id{i}" for i in range(len(chunks))],
    embeddings = embeddings.tolist()  
)

#Conformantion
print("All chunks embedded and stored")

#load dotenv
load_dotenv()

#Create a client for anthropic
anthropic_client = anthropic.Anthropic()

#Function to ask a question though anthropic api
def ask(question):

    #embed question
    query_embeddings = model.encode(question)

    #query collection with question
    results = collection.query(query_embeddings = query_embeddings, n_results = 3)

    #turn query results into text
    relevent_info = "\n\n".join(results['documents'][0])

    #ask question and feed relevent info
    message = anthropic_client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    temperature=0.2,
    system="You are a financial risk analyst. Only state facts grounded in the provided text.",
    messages=[{"role": "user", "content": question + " use only this infomastion: \n" + relevent_info}])

    #Print answer
    print(message.content[0].text)

#Run ask function with a question
ask("What are the main risks this company faces?")