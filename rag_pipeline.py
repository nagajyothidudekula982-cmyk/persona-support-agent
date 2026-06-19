import os
from sentence_transformers import SentenceTransformer
from datetime import datetime
import random
import numpy as np

# ==========================================================
# Cloud-safe mode toggle
# ==========================================================
USE_SIMPLE_MODE = True
# ==========================================================
# Load Embedding Model
# ==========================================================
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ==========================================================
# Knowledge Base
# (UNCHANGED - your original content preserved)
# ==========================================================
DOCUMENTS = [
    """Password Reset Guide
Issue:
User unable to login or forgot password.
Steps:
1. Go to Login page.
2. Click Forgot Password.
3. Enter registered email.
4. Check email inbox.
5. Click password reset link.
6. Reset link expires in 10 minutes.
If email not received:
• Check Spam folder.
• Verify email address.
• Wait 2–3 minutes.""",

    """Authentication Guide
Every API request requires:
Authorization: Bearer <API_KEY>
401 Unauthorized → invalid key
403 Forbidden → permission denied
Best practices:
• Store keys securely
• Rotate keys regularly""",

    """Billing Guide
• Duplicate charge
• Refund delay
Refunds processed in 5–7 business days.
Invoices available in dashboard.""",

    """Troubleshooting Guide
1. Restart app
2. Clear cache
3. Check internet
4. Retry after 5 minutes""",

    """Cookie Guide
Clear cookies from browser settings → Privacy → Clear Data""",

    """Database Integration Guide
• DB unavailable
• Wrong credentials
• Timeout issues
Check logs first.""",

    """Business SLA Guide
Billing disputes → 5–7 days
Critical outages → immediate escalation""",

    """Account Security Guide
5 failed login attempts → account locked for 15 minutes""",

    """API Error Guide
400 Bad Request
401 Unauthorized
403 Forbidden
500 Internal Server Error"""
]

# ==========================================================
# Build Pipeline (Cloud + Local Safe)
# ==========================================================
def build_pipeline():

    print("Building pipeline...")

    # -----------------------------
    # STREAMLIT CLOUD MODE (NO CHROMADB)
    # -----------------------------
    if USE_SIMPLE_MODE:
        print("Running in Cloud Safe Mode (no ChromaDB)")

        embeddings = embedding_model.encode(DOCUMENTS)

        return {
            "docs": DOCUMENTS,
            "embeddings": embeddings
        }

    # -----------------------------
    # LOCAL MODE (ChromaDB)
    # -----------------------------
    import chromadb

    client = chromadb.PersistentClient(path="./chroma_db")

    try:
        client.delete_collection("support_docs")
    except:
        pass

    collection = client.create_collection("support_docs")

    print(f"Documents Loaded: {len(DOCUMENTS)}")

    for i, doc in enumerate(DOCUMENTS):

        embedding = embedding_model.encode(doc).tolist()

        collection.add(
            ids=[str(i)],
            documents=[doc],
            embeddings=[embedding]
        )

    print("Vector DB Created")

    return collection

# ==========================================================
# Retrieve Documents (Hybrid Mode)
# ==========================================================
def retrieve_documents(query, db, top_k=3):

    query_embedding = embedding_model.encode(query)

    # -----------------------------
    # CLOUD MODE (NumPy similarity search)
    # -----------------------------
    if USE_SIMPLE_MODE:

        scores = np.dot(db["embeddings"], query_embedding)

        top_k_idx = np.argsort(scores)[::-1][:top_k]

        return [db["docs"][i] for i in top_k_idx]

    # -----------------------------
    # LOCAL MODE (ChromaDB)
    # -----------------------------
    results = db.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results["documents"][0]

# ==========================================================
# Persona Detection
# ==========================================================
def detect_persona(query):

    q = query.lower()

    if any(word in q for word in ["api", "database", "authentication", "401", "403", "500", "server"]):
        return "Technical Expert"

    elif any(word in q for word in ["business", "sla", "impact", "downtime"]):
        return "Business Executive"

    else:
        return "General User"

# ==========================================================
# Confidence Score
# ==========================================================
def calculate_confidence(docs, query):

    score = 0
    query_words = query.lower().split()

    for doc in docs:
        doc = doc.lower()
        for word in query_words:
            if word in doc:
                score += 1

    return min(score, 10)

# ==========================================================
# Generate Answer
# ==========================================================
def generate_answer(query, persona=None, db=None):

    if db is None:
        db = build_pipeline()

    if not persona:
        persona = detect_persona(query)

    docs = retrieve_documents(query, db)

    context = "\n\n".join(docs)

    confidence = calculate_confidence(docs, query)

    escalation_keywords = [
        "refund", "fraud", "legal", "complaint",
        "escalate", "payment failed"
    ]

    escalated = (
        confidence < 2 or
        any(word in query.lower() for word in escalation_keywords)
    )

    # -----------------------------
    # Persona-based response
    # -----------------------------
    if persona == "General User":
        response = f"""
I found helpful information:

{context}

Steps:
1. Follow the instructions above
2. Contact support if needed
"""

    elif persona == "Technical Expert":
        response = f"""
Technical Details:

{context}

Actions:
• Check logs
• Validate configuration
• Verify API/authentication
"""

    elif persona == "Business Executive":
        response = f"""
Business Summary:

{context}

Impact:
• Review SLA
• Monitor service health
• Escalate if required
"""

    else:
        response = context

    status = "ESCALATED" if escalated else "RESOLVED"

    return {
        "ticket_id": str(random.randint(100000, 999999)),
        "timestamp": str(datetime.now()),
        "persona": persona,
        "issue": query,
        "response": response,
        "documents_used": docs,
        "confidence": confidence,
        "status": status
    }

# ==========================================================
# Terminal Mode (UNCHANGED)
# ==========================================================
if __name__ == "__main__":

    db = build_pipeline()

    print("\nPersona Support Agent Ready\n")

    while True:

        query = input("User: ")

        if query.lower() == "exit":
            break

        persona = detect_persona(query)

        result = generate_answer(query, persona, db)

        print("\n--------------------------------")
        print("Persona:", result["persona"])
        print("Status:", result["status"])
        print("Confidence:", result["confidence"])
        print("--------------------------------\n")

        print(result["response"])
        print("\nTicket ID:", result["ticket_id"])
        print("--------------------------------\n")
