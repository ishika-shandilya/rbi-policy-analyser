# 🏦 RBI Policy Document Analyser

An AI-powered RAG (Retrieval-Augmented Generation) application that lets you upload RBI circulars, monetary policy reports, or notifications and ask questions about them in English — with instant summaries, economic implications, and key policy decisions.

🔗 **Live Demo:** [rbi-policy-analyser.streamlit.app](https://rbi-policy-analyser.streamlit.app)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?logo=googlegemini&logoColor=white)

---

## 📖 Overview

Reading dense RBI circulars and monetary policy documents can be time-consuming. This app uses a Retrieval-Augmented Generation pipeline to let you upload any RBI document and instantly:

- Ask natural-language questions and get context-grounded answers
- Generate a plain-English summary
- Extract the economic implications of a policy
- Identify key decisions and rate changes

All answers are generated using **only the content of the uploaded document**, ensuring accurate, source-grounded responses instead of generic LLM guesses.

---

## ✨ Features

- 📄 **Upload PDF or TXT** RBI documents directly in the browser
- 🔍 **Semantic search** over document content using FAISS vector store
- 💬 **Ask anything** — plain-English Q&A powered by Google Gemini
- 📊 **One-click analysis** — Summarise Policy, Economic Implications, Key Decisions
- 🧠 **Custom prompt engineering** tailored for policy analysis (interpretation + economic impact, not just extraction)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | Gemini Embedding Model |
| Orchestration | LangChain |
| Vector Store | FAISS |
| Document Parsing | PyPDF |
| Deployment | Streamlit Community Cloud |

---

## 🚀 How It Works

1. **Upload** — User uploads a PDF/TXT RBI document
2. **Chunk** — Document is split into overlapping text chunks
3. **Embed** — Each chunk is converted into vector embeddings via Gemini
4. **Store** — Embeddings are indexed in a FAISS vector store
5. **Retrieve** — On a query, the most relevant chunks are retrieved
6. **Generate** — Gemini generates a grounded answer using retrieved context + a custom RBI-analyst prompt template

---

## 💻 Run Locally

```bash
# Clone the repository
git clone https://github.com/ishika-shandilya/rbi-policy-analyser.git
cd rbi-policy-analyser

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
mkdir .streamlit
echo 'GEMINI_API_KEY = "your-key-here"' > .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

---

## 📌 Future Improvements

- [ ] Add retry/backoff handling for API rate limits
- [ ] Support multi-document comparison
- [ ] Add citation highlighting from source chunks
- [ ] Cache repeated queries to reduce API calls

---

## 👩‍💻 Author

Built by **Ishika Shandilya** as part of an ongoing portfolio of Data Science / GenAI projects.

📫 Feel free to connect or reach out for feedback!
