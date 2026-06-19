from datetime import datetime
import random

# -------------------------
# Knowledge Base
# -------------------------
DOCUMENTS = [
    "Password reset: click forgot password and follow email link.",
    "API auth: use Bearer token in header.",
    "Billing: refunds take 5–7 days.",
    "Troubleshooting: restart app and clear cache.",
    "Account lock: 5 failed attempts lock account for 15 minutes."
]

# -------------------------
# Simple retrieval (NO ML)
# -------------------------
def retrieve_documents(query, top_k=3):
    q = query.lower()
    scored = []

    for doc in DOCUMENTS:
        score = sum(1 for w in q.split() if w in doc.lower())
        scored.append((score, doc))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [d for _, d in scored[:top_k]]

# -------------------------
# Build pipeline
# -------------------------
def build_pipeline():
    return DOCUMENTS

# -------------------------
# Generate answer
# -------------------------
def generate_answer(query, persona, db):

    docs = retrieve_documents(query)

    context = "\n\n".join(docs)

    escalated = any(w in query.lower() for w in ["fraud", "legal", "refund"])

    if persona == "Technical Expert":
        response = f"Technical Help:\n{context}"

    elif persona == "Business Executive":
        response = f"Business Summary:\n{context}"

    else:
        response = f"Help Info:\n{context}"

    return {
        "ticket_id": str(random.randint(100000, 999999)),
        "timestamp": str(datetime.now()),
        "persona": persona,
        "issue": query,
        "response": response,
        "documents_used": docs,
        "status": "ESCALATED" if escalated else "RESOLVED"
    }
