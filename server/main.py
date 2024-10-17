import os
import shutil
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, WikipediaLoader, ArxivLoader, CSVLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import bs4
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
app = FastAPI(title="SmartScholar API")

# CORS settings
origins = ["http://localhost:5173"]  # Adjust to your frontend's URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define structured prompts
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that summarizes documents in {language}."),  # Dynamic language
    ("user", "Summarize the following document:\n\n{document_text}")
])

query_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions based on document content in {language}."),  # Dynamic language
    ("user", "Based on the following document:\n\n{document_text}\n\nAnswer the following question:\nQuestion: {user_question}")
])

research_query_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a knowledgeable assistant that provides detailed answers based on the content of research papers in {language}."),  # Dynamic language
    ("user", "You have the following excerpt from a research paper:\n\n{document_text}\n\nPlease answer the following question:\nQuestion: {user_question}")
])

wiki_query_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a knowledgeable assistant that provides detailed answers based on the content retrieved from Wikipedia in {language}."),  # Dynamic language
    ("user", "You have the following content from Wikipedia:\n\n{document_text}\n\nPlease answer the following question:\nQuestion: {user_question}")
])

@app.get("/")
def read_root():
    return {"message": "Welcome to the TextOracle !!"}

@app.post("/pdf/summarize")
async def summarize_pdf(file: UploadFile, language: str = Form("English")):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    temp_pdf_path = "./Attention.pdf"
    try:
        with open(temp_pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        pdfLoader = PyPDFLoader(temp_pdf_path)
        pdf_documents = pdfLoader.load()

        pdf_text = "".join(doc.page_content for doc in pdf_documents)

        # Summarization
        chain_input = {
            "document_text": pdf_text[:2000],  # Limit input size
            "language": language
        }
        summary_chain = summary_prompt | model
        summary_response = summary_chain.invoke(chain_input)
        
        # Structured response
        structured_response = {
            "language": language,
            "summary": summary_response.content
        }

        return JSONResponse(content=structured_response)

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"})
    
    finally:
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)  # Clean up the temporary file

@app.post("/pdf/query")
async def query_pdf(file: UploadFile, question: str = Form(...), language: str = Form("English")):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    temp_pdf_path = "./Attention.pdf"
    try:
        with open(temp_pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        pdfLoader = PyPDFLoader(temp_pdf_path)
        pdf_documents = pdfLoader.load()

        pdf_text = "".join(doc.page_content for doc in pdf_documents)

        # Answering the question
        chain_input = {
            "document_text": pdf_text[:2000],
            "user_question": question,
            "language": language
        }
        query_chain = query_prompt | model
        query_response = query_chain.invoke(chain_input)
        
        # Structured response
        structured_response = {
            "language": language,
            "question": question,
            "answer": query_response.content
        }

        return JSONResponse(content=structured_response)

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"})

    finally:
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)  # Clean up the temporary file

@app.post("/webpage/summarize")
async def summarize_webpage(url: str, language: str = Form("English")):
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL. Please provide a valid URL.")

    try:
        webLoader = WebBaseLoader(
            web_paths=[url],
            bs_kwargs=dict(parse_only=bs4.SoupStrainer(["p", "div", "span", "h1", "h2", "h3"]))
        )
        webContent = webLoader.load()
        web_text = webContent[0].page_content

        # Summarization
        chain_input = {
            "document_text": web_text[:2000],
            "language": language
        }
        summary_chain = summary_prompt | model
        summary_response = summary_chain.invoke(chain_input)
        
        # Structured response
        structured_response = {
            "language": language,
            "summary": summary_response.content
        }

        return JSONResponse(content=structured_response)

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"})

@app.post("/webpage/query")
async def query_webpage(url: str, question: str = Form(...), language: str = Form("English")):
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL. Please provide a valid URL.")

    try:
        webLoader = WebBaseLoader(
            web_paths=[url],
            bs_kwargs=dict(parse_only=bs4.SoupStrainer(["p", "div", "span", "h1", "h2", "h3"]))
        )
        webContent = webLoader.load()
        web_text = webContent[0].page_content

        # Answering the question
        query_chain_input = {
            "document_text": web_text[:2000],
            "user_question": question,
            "language": language
        }
        query_chain = query_prompt | model
        query_response = query_chain.invoke(query_chain_input)
        
        # Structured response
        structured_response = {
            "language": language,
            "question": question,
            "answer": query_response.content
        }

        return JSONResponse(content=structured_response)

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"})
    


@app.get("/read_research_paper/{paper_id}")
async def read_research(paper_id: str, summarize: bool = False, query: str = None, language: str = "en"):
    try:
        # Load the research paper
        paperLoader = ArxivLoader(query=paper_id, load_max_docs=1)
        paperContent = paperLoader.load()
        
        if not paperContent:
            return JSONResponse(content={"error": "No content found for the specified paper ID."})

        content = paperContent[0]
        metadata = content.metadata
        # print(metadata)
        
        # Prepare the response
        response = {
            "Title": metadata.get("Title", "Unknown Title"),
            "Authors": "".join(metadata.get("Authors", [])) if metadata.get("Authors") else "Unknown Authors",
            "Published": metadata.get("Published", "Unknown Date"),
            "Page_Content": content.page_content if content.page_content else "No Content Available",
            "Language": language,
            "Summary": None,
            "Query_Response": None
        }
        
        # Summarize if requested
        if summarize:
            # Prepare input for summarization
            chain_input = {
                "document_text": content.page_content[:2000],  # Limit input size for summarization
                "language": language
            }
            summary_chain = summary_prompt | model  # Assuming summary_prompt is defined for summarization
            summary_response = summary_chain.invoke(chain_input)
            response["Summary"] = summary_response.content
        # Respond to a query if provided
        if query:
            query_response = await handle_query(content.page_content, query, language)
            response["Query_Response"] = query_response
        
        return response

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred while loading the research paper: {str(e)}"})
MAX_TOKENS = 1500  # Adjust based on model capacity and testing
async def handle_query(document_text: str, user_question: str, language: str ="en"):
    try:
        # Limit the document text size
        if len(document_text.split()) > MAX_TOKENS:
            document_text = ' '.join(document_text.split()[:MAX_TOKENS])  # Truncate to the first MAX_TOKENS words

        # Prepare the input for the query prompt
        query_input = {
            "document_text": document_text,
            "user_question": user_question,
            "language": language
        }

        # Use the research_query_prompt to get the response
        query_chain = research_query_prompt | model  # Use research_query_prompt
        query_response = query_chain.invoke(query_input)  # Pass the query_input directly

        return query_response.content

    except Exception as e:
        return f"An error occurred while processing the query: {str(e)}"

@app.get('/read_wikipedia')
async def read_wikipedia(query: str = "Generative AI", user_question: str = None, language: str = "en", summarize: bool = False):
    try:
        # Load content from Wikipedia
        wikiLoader = WikipediaLoader(query=query, load_max_docs=3)
        wikiContent = wikiLoader.load()

        if not wikiContent:
            return JSONResponse(content={"error": "No content found for the specified query."})

        # Combine the content from loaded pages
        combined_content = " ".join(doc.page_content for doc in wikiContent)

        # Prepare the response dictionary
        response = {
            "Wikipedia_Content": combined_content,
            "Language": language,
            "Summary": None,
            "Query_Response": None  # Placeholder for query response
        }

        # Summarize if requested
        if summarize:
            # Prepare input for summarization
            chain_input = {
                "document_text": combined_content[:2000],  # Limit to the first 2000 characters
                "language": language
            }
            summary_chain = summary_prompt | model  # Assuming summary_prompt is defined for summarization
            summary_response = summary_chain.invoke(chain_input)
            response["Summary"] = summary_response.content

        # If a user question is provided, handle the query
        if user_question:
            query_response = await handle_wiki_query(combined_content, user_question, language)
            response["Query_Response"] = query_response

        return response

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred while processing the request: {str(e)}"})

# Implementing query handling for the loaded Wikipedia content
async def handle_wiki_query(document_text: str, user_question: str, language: str = "en"):
    try:
        # Ensure document_text is a single string
        if isinstance(document_text, list):
            document_text = " ".join(document_text)  # Join the list into a single string

        # Limit the document text size
        if len(document_text.split()) > MAX_TOKENS:
            document_text = ' '.join(document_text.split()[:MAX_TOKENS])  # Truncate to the first MAX_TOKENS words

        # Prepare the input for the query prompt
        query_input = {
            "document_text": document_text,
            "user_question": user_question,
            "language": language
        }

        # Use the wiki_query_prompt to get the response
        query_chain = wiki_query_prompt | model  # Use wiki_query_prompt
        query_response = query_chain.invoke(query_input)  # Pass the query_input directly

        return query_response.content

    except Exception as e:
        return f"An error occurred while processing the query: {str(e)}"
    
    

# @app.get('/read_csv')
# async def read_csv(file_path: str = './data_science_job.csv'):
#     try:
#         csv_loader = CSVLoader(file_path=file_path)
#         csvContent = csv_loader.load()
#         print(csvContent)
#         return {"CSV_Content": csvContent}
    
#     except Exception as e:
#         return JSONResponse(content={"error": f"An error occurred while loading the CSV file: {str(e)}"})