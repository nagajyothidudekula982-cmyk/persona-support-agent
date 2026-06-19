import os
import random
from datetime import datetime

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


DATA_PATH = "data"


# ---------------- SIMPLE SPLITTER ----------------
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


# ---------------- PERSONA CLASSIFIER ----------------
def classify_persona(query: str):
    query = query.lower()

    if any(k in query for k in ["api", "code", "error", "header", "request"]):
        return "Technical Expert"
    elif any(k in query for k in ["urgent", "not working", "issue", "help", "stuck"]):
        return "Frustrated User"
    elif any(k in query for k in ["revenue", "impact", "business", "cost", "downtime"]):
        return "Business Executive"
    else:
        return "General User"


# ---------------- ESCALATION CHECK ----------------
def should_escalate(confidence, query):
    sensitive_keywords = ["refund", "billing", "locked", "fraud", "charge"]

    if confidence < 0.5:
        return True

    if any(k in query.lower() for k in sensitive_keywords):
        return True

    return False


# ---------------- MAIN PIPELINE ----------------
class RAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = None

    # LOAD FILES
    def load_documents(self):
        docs = []

        for file in os.listdir(DATA_PATH):
            path = os.path.join(DATA_PATH, file)

            if file.endswith(".txt") or file.endswith(".md"):
                loader = TextLoader(path, encoding="utf-8")
                docs.extend(loader.load())

        print(f"Documents Loaded: {len(docs)}")
        return docs

    # SPLIT
    def split_documents(self, documents):
        chunks = []

        for doc in documents:
            chunks.extend(split_text(doc.page_content))

        print(f"Chunks Created: {len(chunks)}")
        return chunks

    # VECTOR STORE
    def build_vectorstore(self, chunks):
        self.vectorstore = FAISS.from_texts(chunks, self.embeddings)
        print("Vector DB Created")

    # RETRIEVE WITH SCORE
    def retrieve(self, query, k=3):
        results = self.vectorstore.similarity_search_with_score(query, k=k)

        docs = []
        scores = []

        for doc, score in results:
            docs.append(doc.page_content)
            scores.append(score)

        confidence = 1 - (sum(scores) / len(scores)) if scores else 0

        return docs, confidence

    # MAIN RUN
    def run(self, query):
        persona = classify_persona(query)

        documents = self.load_documents()
        chunks = self.split_documents(documents)
        self.build_vectorstore(chunks)

        context, confidence = self.retrieve(query)

        escalate = should_escalate(confidence, query)

        response = self.generate_response(persona, query, context)

        if escalate:
            return {
                "ticket_id": str(random.randint(100000, 999999)),
                "timestamp": str(datetime.now()),
                "persona": persona,
                "issue": query,
                "status": "ESCALATED",
                "reason": "Low confidence / sensitive issue",
                "documents_used": context
            }

        return {
            "persona": persona,
            "query": query,
            "confidence": confidence,
            "response": response,
            "escalated": False
        }

    # RESPONSE ENGINE
    def generate_response(self, persona, query, context):
        context_text = "\n".join(context)

        if persona == "Technical Expert":
            style = "Explain step-by-step with technical depth"
        elif persona == "Frustrated User":
            style = "Be empathetic and simple"
        elif persona == "Business Executive":
            style = "Be concise and impact-focused"
        else:
            style = "Be simple and clear"

        return f"""
Persona: {persona}
Style: {style}

Context:
{context_text}

Answer:
Based on the above knowledge base, here is the best resolution for your issue:
{query}
"""
