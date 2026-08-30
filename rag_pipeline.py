from pypdf import PdfReader

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

#Run function on pdf
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

#Run chunk_text on goldman pdf text and print total chunks and the first chunk
chunks = chunk_text(text)
print(len(chunks))
print(chunks[0])