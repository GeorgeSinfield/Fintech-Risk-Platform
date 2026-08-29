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

#Print function's first 500 words
print(text[:500])