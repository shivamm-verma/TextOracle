import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Get the Groq API Key from .env
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq Model
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Define the structured prompt for Groq
summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that summarizes documents.",
        ),
        (
            "user",
            "Summarize the following document:\n\n{document_text}"
        )
    ]
)

query_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that answers questions based on document content.",
        ),
        (
            "user",
            "Based on the following document:\n\n{document_text}\n\nAnswer the following question:\nQuestion: {user_question}"
        )
    ]
)
st.title("PDF Query with Groq API")

# Step 1: Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with open("temp_uploaded_pdf.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Step 2: Use PyPDFLoader to load the PDF content
    pdfLoader = PyPDFLoader("temp_uploaded_pdf.pdf")
    pdf_documents = pdfLoader.load()
    
    # Extract text content from all the documents
    pdf_text = ""
    for doc in pdf_documents:
        pdf_text += doc.page_content

    st.write("Extracted text from PDF:")
    st.text_area("PDF Text", pdf_text[100:2000], height=300)  # Display a part of the text for better UX

    # Step 3: Summarize the PDF text using Groq API
    if st.button("Summarize PDF"):
        # Prepare input for summarization
        chain_input = {
            "document_text": pdf_text[:2000]  # Use only the first 2000 characters for summarization
        }

        # Call Groq API for summarization using the defined prompt
        try:
            summary_chain = summary_prompt | model
            summary_response = summary_chain.invoke(chain_input)
            st.write("Summarized Result:")
            st.write(summary_response.content)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while summarizing: {e}")

    # Step 4: User query interaction with Groq API
    user_query = st.text_input("Ask a question about the PDF content:")

    if user_query and st.button("Get Answer from Groq"):
        # Prepare input for query answering
        query_chain_input = {
            "document_text": pdf_text[:2000],  # Again, limit the content to 2000 characters
            "user_question": user_query
        }

        # Call Groq API for question answering using the defined prompt
        try:
            query_chain = query_prompt | model
            query_response = query_chain.invoke(query_chain_input)
            st.write("Groq API Response:")
            st.write(query_response.content)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")



# import os
# import streamlit as st
# from langchain_groq import ChatGroq
# # from langchain_community.embeddings import OllamaEmbeddings
# from langchain_ollama import OllamaEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_core.prompts import ChatPromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# groq_api_key = os.getenv("GROQ_API_KEY")
# print(groq_api_key)

# model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# # Ensure you import or define this properly
# # from langchain_core.prompts import ChatPromptTemplate
# # Define the prompt template if it's missing
# prompt = ChatPromptTemplate(
#     input_variables=["context", "input"],
#     template="""
#         Answer questions based on the provided text, summarizing the concept to the best of your ability.
#         Please provide the most accurate response based on:
#         <context> 
#         {context}
#         <context> 
#         Question: {input}
#     """
# )
# print(prompt)

# embeddings = OllamaEmbeddings(
#     model="llama3",
# )
# def create_vector_embedding():
#     if "vectors" not in st.session_state:
#         st.session_state.embeddings = embeddings
#         st.session_state.loader = PyPDFDirectoryLoader("Attention.pdf")
#         st.session_state.docs = st.session_state.loader.load()
#         st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:10])
#         print(st.session_state.final_documents)
#         st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# user_prompt = st.text_input("Enter your query:")

# if st.button("Document Embeddings"):
#     create_vector_embedding()
#     st.write("Vector Database is ready")

# import time

# if user_prompt:
#     document_chain = create_stuff_documents_chain(model, prompt)
#     retriever = st.session_state.vectors.as_retriever()
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)
#     start = time.process_time()
#     response = retrieval_chain.invoke({'input': user_prompt})
#     st.write(f"Response time: {time.process_time() - start} seconds")
#     st.write(response['answer'])

#     with st.expander("Document similarity Search"):
#         for i, doc in enumerate(response['context']):
#             st.write(doc.page_content)
#             st.write('-----------------------')

# import os
# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain_ollama import OllamaEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_core.messages import SystemMessage, HumanMessage
# from langchain_core.prompts import ChatPromptTemplate
# from dotenv import load_dotenv

# load_dotenv()

# # Load the API key for the Groq model
# groq_api_key = os.getenv("GROQ_API_KEY")
# print(groq_api_key)

# # Initialize the ChatGroq model
# model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# # Define the conversation as a list of messages
# messages = [
#     SystemMessage(content="You are a helpful assistant."),
#     HumanMessage(content="Question: {input}")
# ]

# # Initialize the ChatPromptTemplate with the messages
# prompt = ChatPromptTemplate(messages=messages)
# print(prompt)

# # Initialize the embeddings for Ollama model
# embeddings = OllamaEmbeddings(model="llama3")

# def create_vector_embedding():
#     if "vectors" not in st.session_state:
#         st.session_state.embeddings = embeddings
#         st.session_state.loader = PyPDFDirectoryLoader("Attention.pdf")
#         st.session_state.docs = st.session_state.loader.load()
#         st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:10])
#         print(st.session_state.final_documents)
#         st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# # Streamlit UI for user input
# user_prompt = st.text_input("Enter your query:")

# # Button to trigger vector embedding creation
# if st.button("Document Embeddings"):
#     create_vector_embedding()
#     st.write("Vector Database is ready")

# import time

# # Processing user input and using the retrieval chain
# if user_prompt:
#     document_chain = create_stuff_documents_chain(model, prompt)
#     retriever = st.session_state.vectors.as_retriever()
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
#     start = time.process_time()
#     response = retrieval_chain.invoke({'input': user_prompt})
#     st.write(f"Response time: {time.process_time() - start} seconds")
#     st.write(response['answer'])

#     # Display document similarity search results
#     with st.expander("Document similarity Search"):
#         for i, doc in enumerate(response['context']):
#             st.write(doc.page_content)
#             st.write('-----------------------')






















# # for chat convenience to teachers and students in multilanguage
# from langchain_community.chat_message_histories import ChatMessageHistory 
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.messages import HumanMessage, AIMessage


























# # to distinguish chatSession with other chatSessions
# chat_store = {}

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in chat_store:
#         chat_store[session_id] = ChatMessageHistory()
#     return chat_store[session_id]

# with_msg_history = RunnableWithMessageHistory(model, get_session_history)

# config = {"configurable":{"session_id": "chat1"}}

# response = with_msg_history.invoke(
#     [HumanMessage(content="Hi, I am Prachi and I am an AI Engineer, I am doing DSA in Java")],
#     config=config
# )
# # print(response)
# # prompt Templating
# from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceHolder
# prompt = ChatPromptTemplate(
#     [
#         ("system","You are a helpful assitant for school students and teachers, you always recommend good tips and Answer them to the best of your ability")    
#     ],
#     MessagesPlaceHolder(variable_name="messages")
# )
