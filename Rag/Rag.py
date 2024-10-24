import os 
import streamlit as st 
import google.generativeai as genai
import tempfile 
import numpy as np 
from dotenv import load_dotenv 
from langchain.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer 
import faiss
load_dotenv()

api=os.getenv("Google_api_key")

if api:
    genai.configure(api_key=api)
else:
    st.error("API not found")
    
def generate_text(text):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(text)
    return response.text

st.title("Rag With Vector Database and Gemini API")

if "message" not in st.session_state:
    st.session_state.message=[]

for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

upload=st.file_uploader("choose file",type=["pdf"]) 
# its not a valid path

if upload is not None:
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tfile:
        tfile.write(upload.read())
        tfpath=tfile.name
        
    
    loader=PyPDFLoader(tfpath)
    documents=loader.load()
    
    #Embedding model 
    e_model=SentenceTransformer("all-MiniLM-L6-v2")
    text=[doc.page_content for doc in documents] #incase multiple pages
    embeddings=e_model.encode(text,show_progress_bar=True)
    em_matrix=np.array(embeddings)
    index=faiss.IndexFlatL2(em_matrix.shape[1])  #create index 
    index.add(em_matrix)
    st.success("PDF content Processed into the Index")
    user_input=st.chat_input("Please enter Question")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        
        st.session_state.message.append({"role":"user","content":user_input})
        embd_question=e_model.encode([user_input])
        k=1
        distances,indecies=index.search(embd_question,k)
        similar_doc=[documents[i] for i in indecies[0]]
        context=""
        for i,doc in enumerate(similar_doc):
            context+=doc.page_content+"\n"
        # st.write(context)
        #Understanding LLM large language model (Gemini APi)
        prompt=f"You are an assistant who retrieves answers based on the following content:{context}\n\nQuestion:{user_input}"
        with st.chat_message("assistant"):
            message_placeholder=st.empty()
            with st.spinner("generating answer"):
                response=generate_text(prompt)
                message_placeholder.markdown(f"{response}")
        st.session_state.message.append({"role":"assistant","content":response})
else:
    st.info("Please Upload File to chat with")
