
import streamlit as st
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


st.set_page_config(page_title="RBI Policy Document Review App", layout="wide")
st.title("🏦 RBI Policy Document Analyser")
st.write("Upload any RBI circular, monetary policy report, or notification and ask questions in English Language.")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload RBI Document (PDF or TXT)", type=["pdf", "txt"])

# -------------------------------
# LOAD DOCUMENT
# -------------------------------
def load_document(file):
    if file.name.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(file.read())
        loader = PyPDFLoader("temp.pdf")
    else:
        with open("temp.txt", "wb") as f:
            f.write(file.read())
        loader = TextLoader("temp.txt")

    documents = loader.load()
    return documents


# -------------------------------
# TEXT SPLITTING - Chunking
# -------------------------------
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)

# -------------------------------
# VECTOR STORE - 
# -------------------------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def create_vectorstore(docs):
    # embeddings = OpenAIEmbeddings()
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",
                                              api_key = GEMINI_API_KEY)
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


POLICY_PROMPT = PromptTemplate(
    input_variables = ["context","question"],
    template = """
You are an expert RBI policy analyst and economist.
Analyze the following RBI document and answer the question.

Provide:
1. Clear answer
2. Policy interpretation
3. Economic implications
4. Impact on India's economy

Context:
{context}

Question:
{question}

Answer:
"""
)


def create_qa_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash',temperature=0.37,
                                 api_key = GEMINI_API_KEY) 
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | POLICY_PROMPT
        | llm
    )

    return chain


# -------------------------------
# PROCESS DOCUMENT
# -------------------------------
if uploaded_file:
    st.spinner("Processing document...")

    documents = load_document(uploaded_file)     # Loads the file
    split_docs = split_documents(documents)      # Chunks the docs
    vectorstore = create_vectorstore(split_docs) # Gen Docs Embeddings + Add Index - Store into VectorDB
    qa_chain = create_qa_chain(vectorstore)      # Generate QA Chain
    st.success("Document processed successfully!")

    # USER QUERY
    query = st.text_input("Ask a question from the document:")

    if query:
        with st.spinner("Analyzing..."):
            response = qa_chain.invoke(query)
            st.subheader("Answer")
            st.write(response.content)

    # -------------------------------
    # EXTRA ANALYSIS BUTTONS
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Summarise Policy"):
            response = qa_chain.invoke("Summarise this RBI document in simple terms in under 300 words")
            st.write(response.content)

    with col2:
        if st.button("📈 Economic Implications"):
            response = qa_chain.invoke("What are the key economic implications of this policy in under 300 words")
            st.write(response.content)

    with col3:
        if st.button("🎯 Key Decisions"):
            response = qa_chain.invoke("What are the key policy decisions and rate changes mentioned in under 300 words")
            st.write(response.content)

else:
    st.warning("Please upload a RBI Policy Document to begin.")

