

📘 PolicyPulse – Intelligent HR Policy Assistant using LangChain, Qdrant & RAG
PolicyPulse is an enterprise-grade Retrieval-Augmented Generation (RAG) powered HR Policy Assistant designed to help employees instantly understand company policies with accuracy, clarity, and real-time guidance. A complete **Retrieval-Augmented Generation (RAG)** system designed to help employees query HR policies with high accuracy, using:

* **LangChain** for end-to-end orchestration
* **Qdrant** for semantic vector storage and retrieval
* **MiniLM-L6-v2 (HuggingFace)** embeddings
* **Groq Llama-3.1-8B** for ultra-fast, deterministic LLM responses
* **FastAPI** backend with context retrieval, memory tracking & custom reasoning
* **Streamlit** chatbot UI with typing animation, expandable context view & memory controls



# 🚀 **Features**

### 🔍 Intelligent HR Query Handling

* Answers employee questions using real company policy PDFs.
* Extracts, embeds, and retrieves policy chunks using semantic search.

### 🧠 Multi-Stage Reasoning

* Topic detection
* Smart fallback logic
* Dynamic prompt engineering
* “Answer in short” / “Explain more” adaptive responses
* Memory-aware conversation flow

### ⚡ Groq-Powered LLM

* Uses **Llama-3.1-8B** (Groq) for near-instant responses
* Temperature 0 for deterministic, accurate policy answers

### 📚 LangChain Integration

* PDF loaders
* Recursive text splitting
* Embeddings
* VectorStore retrievers
* Custom LLM chains

### 🗄 Qdrant Vector Database

* Dockered instance
* Persistent vector storage
* Fast, scalable semantic retrieval

### 💬 Modern Chat UI

* Built with Streamlit
* Real-time typing animation
* Expandable conversation history
* View/Clear memory buttons
* Clean professional layout

---

# 📁 **Project Structure**

```
POLICYPULSE – INTELLIGENT HR POLICY ASSISTANT/
│
├── app/
│   ├── ingest_pdfs.py          # Extracts text from PDFs & loads into Qdrant
│   ├── rag_chain.py            # RAG pipeline, retrieval, Groq LLM logic
│   ├── server.py               # FastAPI backend (routes, memory, inference)
│   ├── __init__.py
│   └── __pycache__/
│
├── ui/
│   └── app.py                  # Streamlit chatbot UI
│
├── policies/
│   └── README.md               # Policy document instructions
│
├── document/
│   ├── policy_pulse_flowchart.pdf
│   └── PolicyPulse_Full_Technical_Documentation.pdf
│
├── docker-compose.yml          # Qdrant database setup
├── requirements.txt            # Python dependencies
├── README.md                   # Main GitHub documentation (THIS FILE)
└── .gitignore
```

---

# 🛠 **Tech Stack**

### **Backend**

* Python
* FastAPI
* LangChain
* Qdrant (Dockerized)
* HuggingFace SentenceTransformers (MiniLM-L6-v2)
* Groq Llama-3.1-8B

### **Frontend**

* Streamlit

### **Infra / Tools**

* Docker
* Git
* VS Code

---

# ⚙️ **Setup Instructions**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/PolicyPulse.git
cd PolicyPulse
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start Qdrant (Docker)

```bash
docker-compose up -d
```

### 5️⃣ Add your Groq API key

Create **.env**:

```
GROQ_API_KEY=your_key_here
```

### 6️⃣ Run PDF ingestion

```bash
python app/ingest_pdfs.py
```

### 7️⃣ Run backend

```bash
uvicorn app.server:app --reload
```

### 8️⃣ Run Streamlit UI

```bash
streamlit run ui/app.py
```

---

# 🧪 **How It Works (Short Overview)**

1. PDFs → processed & split into chunks
2. MiniLM-L6-v2 embeddings generated
3. Stored in Qdrant vector DB
4. On user query → embeddings computed
5. Qdrant returns top-k relevant policy chunks
6. LangChain builds optimized prompt
7. Groq Llama-3.1-8B generates final answer
8. Streamlit displays response with typing animation

---

# 📦 **Documents Included**

Inside **/document**:

* **policy_pulse_flowchart.pdf** → architecture flowchart
* **PolicyPulse_Full_Technical_Documentation.pdf** → technical documentation

---

# 🧑‍💻 **Author**

**Kavinvelavan Manivasakan**
GitHub: [https://github.com/mkavinvelavan](https://github.com/mkavinvelavan)
LinkedIn: [https://www.linkedin.com/in/m-kavinvelavan/](https://www.linkedin.com/in/m-kavinvelavan/)

---

# ⭐ **Support the Project**

If you found this useful, please ⭐ star the repository!
Your support helps the project reach more developers.

---




