from datetime import datetime
import random

# ==========================================================
# Knowledge Base
# ==========================================================
DOCUMENTS = [
    "Password Reset Guide: Go to login page and click forgot password.",
    "API Authentication: Use Bearer token in headers. 401 invalid key, 403 forbidden.",
    "Billing Guide: Refunds take 5–7 business days.",
    "Troubleshooting: restart app, clear cache, check internet.",
    "Account Security: 5 failed logins locks account for 15 minutes.",
    "API Errors: 400 bad request, 500 server error."
]

# ==========================================================
# Simple keyword retrieval (NO ML, NO CRASH)
# ==========================================================
def retrieve_documents(query, top_k=3):

    query = query.lower()
    scored = []

    for doc in DOCUMENTS:
        score = sum(1 for word in query.split() if word in doc.lower())
        scored.append((score, doc))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [doc for _, doc in scored[:top_k]]

# ==========================================================
# Persona detection
# ==========================================================
def detect_persona(query):

    q = query.lower()

    if any(x in q for x in ["api", "server", "error", "authentication"]):
        return "Technical Expert"

    if any(x in q for x in ["billing", "refund", "payment"]):
        return "Business Executive"

    return "General User"

# ==========================================================
# Generate Answer
# ==========================================================
def generate_answer(query, persona=None, db=None):

    if not persona:
        persona = detect_persona(query)

    docs = retrieve_documents(query)

    context = "\n\n".join(docs)

    confidence = len([d for d in docs if any(w in d.lower() for w in query.lower().split())])

    escalated = (
        confidence < 1 or
        any(w in query.lower() for w in ["fraud", "legal", "complaint", "refund"])
    )

    if persona == "General User":
        response = f"""
Help Information:

{context}

Steps:
1. Follow instructions above
2. Contact support if needed
"""

    elif persona == "Technical Expert":
        response = f"""
Technical View:

{context}

Check:
• Logs
• API keys
• Server status
"""

    else:
        response = f"""
Business View:

{context}

Review SLA and escalate if needed.
"""

    return {
        "ticket_id": str(random.randint(100000, 999999)),
        "timestamp": str(datetime.now()),
        "persona": persona,
        "issue": query,
        "response": response,
        "documents_used": docs,
        "confidence": confidence,
        "status": "ESCALATED" if escalated else "RESOLVED"
    }

# ==========================================================
# Terminal test
# ==========================================================
if __name__ == "__main__":

    print("RAG System Running (Safe Mode)")

    while True:
        q = input("User: ")
        if q == "exit":
            break

        r = generate_answer(q)

        print("\n--- RESPONSE ---")
        print(r["response"])
        print("STATUS:", r["status"])
        print("----------------\n")
