# documentReader.py
from fastapi import FastAPI
from langchain_community.document_loaders import TextLoader,PyPDFLoader,WebBaseLoader,ArxivLoader,WikipediaLoader,CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter,HTMLHeaderTextSplitter


import bs4

app = FastAPI()

@app.get("/read_document")
def read_document():
    loader = TextLoader('speech.txt')  # Assuming 'speech.txt' is in the same directory
    text_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20)
    final_docs = text_splitter.split_documents(text_documents)
    print(final_docs)
    return {"document_content": final_docs}

@app.get('/read_pdf')
def read_pdf():
    pdfLoader = PyPDFLoader('Prachi-Resume.pdf')
    pdf = pdfLoader.load()
    print(pdf)
    return {"pdf_content": pdf}
@app.get("/read_webpage")
def read_webpage():
    webLoader = WebBaseLoader(web_paths=('https://medium.com/@ai.blog/artificial-intelligence-ai-blogs-e1d1090599be','https://dlabs.ai/blog/top-ai-blogs-and-websites-to-follow/'),
                              bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(["p", "div", "span", "h1", "h2", "h3",])  # Include p tags and other tags
        )
        )
    webContent = webLoader.load()
    headers_to_split_on=[
        ("h1","Header 1"),
        ("h2","Header 2"),
        ("h3","Header 3")
        ]
    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on)
    final_docs_form = html_splitter.split_text(webContent[0].page_content)
    # print(webContent[0].page_content)
    
    return {"webpage_content":final_docs_form}

@app.get("/read_research_paper")
def read_research():
    paperLoader = ArxivLoader(query="1706.03762",load_max_docs=2)
    paperContent = paperLoader.load()
    print(paperContent)
    return {"Reaseach-Paper-Content":paperContent}

@app.get('/read_wikipedia')
def read_wikipedia():
    wikiLoader = WikipediaLoader(query="Generative AI",load_max_docs=3)
    wikiContent = wikiLoader.load()
    print(wikiContent)
    return {"Wikipedia_Content":wikiContent}
    
@app.get('/read_csv')
def read_csv():
    csv_loader = CSVLoader(file_path='./data_science_job.csv')
    csvContent = csv_loader.load()
    print(csvContent)
    return {"CSV Loader ": csvContent}
    
    
    