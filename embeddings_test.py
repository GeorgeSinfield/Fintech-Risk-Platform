from sentence_transformers import SentenceTransformer , util
import chromadb

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

#Create sentences to embed
sentences = ["The company faces significant liquidity risk due to short-term debt obligations.", "The firm may struggle to meet its short-term financial commitments.", "The CEO purchased a private yacht last summer."] 

#embed the sentences
embeddings = model.encode(sentences)

#print the cosine similarity between sentence 1 and sentence 2, and between sentence 1 and sentence 3
print(util.cos_sim(embeddings[0], embeddings[1]))
print(util.cos_sim(embeddings[0], embeddings[2]))

# Create a ChromaDB client
client = chromadb.Client()

# Create a collection in ChromaDB
collection = client.create_collection("risk_test")

# Add the sentences, ids and embeddings to the collection
collection.add(
    documents = sentences,
    ids = ["id1", "id2", "id3"],
    embeddings = embeddings.tolist()  
)

#Query
query = "What financial risks does the company have?" 

#embed the Query
query_embeddings = model.encode(query)

#Query the collection using embedding
results = collection.query(
    query_embeddings = query_embeddings,
    n_results = 2
)

#print results
print(results)