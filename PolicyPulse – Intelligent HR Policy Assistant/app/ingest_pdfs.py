import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceEmbeddings

# Path to your policies folder
POLICY_PATH = "policies"

# Qdrant config
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "policypulse_policies"

def load_pdfs():
    docs = []
    for file in os.listdir(POLICY_PATH):
        if file.endswith(".pdf"):
            path = os.path.join(POLICY_PATH, file)
            loader = PyPDFLoader(path)
            pages = loader.load_and_split()

            for p in pages:
                p.metadata["source"] = file

            docs.extend(pages)
    return docs

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)

def ingest():
    print("📄 Loading PDFs...")
    docs = load_pdfs()

    print(f"🔍 Loaded {len(docs)} pages. Splitting...")
    chunks = split_docs(docs)

    print(f"✂️ Total chunks: {len(chunks)}")

    print("🧠 Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("🗄 Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_URL)

    print("📥 Uploading to Qdrant collection...")
    Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )

    print("✅ Ingestion completed successfully!")

if __name__ == "__main__":
    ingest()
