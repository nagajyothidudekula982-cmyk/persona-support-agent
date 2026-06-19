import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime
import random

# ==========================================================
# Load Embedding Model
# ==========================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================================
# Knowledge Base
# ==========================================================

DOCUMENTS = [

"""
Password Reset Guide

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
• Wait 2–3 minutes.
""",

"""
Authentication Guide

Every API request requires:

Authorization: Bearer <API_KEY>

Common Errors

401 Unauthorized
• Invalid API key
• Expired API key
• Missing Authorization header

403 Forbidden
• Permission denied

Best Practices

• Store API keys in environment variables.
• Never expose API keys.
• Rotate keys regularly.
""",

"""
Billing Guide

Common Issues

• Duplicate charge
• Refund delay
• Failed payment

Refund Policy

Refunds are processed within
5–7 business days.

Invoices can be downloaded
from Dashboard.
""",

"""
Troubleshooting Guide

If application is not working

1. Restart application.
2. Clear browser cache.
3. Clear browser cookies.
4. Check internet.
5. Verify API service status.
6. Try again after five minutes.

Timeout errors
usually indicate network issues.
""",

"""
Cookie Guide

To clear cookies

Google Chrome

Settings

↓

Privacy and Security

↓

Clear Browsing Data

↓

Cookies and Cached Files

↓

Clear Data
""",

"""
Database Integration Guide

Internal server errors may happen because

• Database unavailable
• Wrong credentials
• Firewall blocking access
• Invalid connection string
• Database timeout

Always verify logs first.
""",

"""
Business SLA Guide

Billing disputes

Resolved within

5–7 business days

Critical outages

Escalate immediately.
""",

"""
Account Security Guide

Account lock occurs after

5 failed login attempts.

Lock duration

15 minutes.

Users may wait
or contact support.
""",

"""
API Error Guide

400 Bad Request

Invalid request format.

401 Unauthorized

Authentication failure.

403 Forbidden

Permission denied.

500 Internal Server Error

Unexpected backend failure.
"""

]


# ==========================================================
# Build Vector Database
# ==========================================================

def build_pipeline():

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    try:

        client.delete_collection("support_docs")

    except:

        pass

    collection = client.create_collection(
        "support_docs"
    )

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
# Retrieve Documents
# ==========================================================

def retrieve_documents(

        query,

        db,

        top_k=3

):

    query_embedding = embedding_model.encode(query).tolist()

    results = db.query(

        query_embeddings=[query_embedding],

        n_results=top_k

    )

    return results["documents"][0]


# ==========================================================
# Persona Detection
# ==========================================================

def detect_persona(query):

    q = query.lower()

    if any(word in q for word in [

        "api",

        "database",

        "authentication",

        "401",

        "403",

        "500",

        "token",

        "server",

        "integration"

    ]):

        return "Technical Expert"

    elif any(word in q for word in [

        "business",

        "sla",

        "timeline",

        "executive",

        "downtime",

        "impact"

    ]):

        return "Business Executive"

    else:

        return "General User"


# ==========================================================
# Confidence Score
# ==========================================================

def calculate_confidence(

        docs,

        query

):

    query = query.lower()

    score = 0

    for doc in docs:

        doc = doc.lower()

        for word in query.split():

            if word in doc:

                score += 1

    return min(score, 10)
# ==========================================================
# Generate Answer
# ==========================================================

def generate_answer(query, persona=None, db=None):

    # Build DB if not passed
    if db is None:
        db = build_pipeline()

    # Auto-detect persona if none selected
    if persona is None or persona == "":
        persona = detect_persona(query)

    # Retrieve documents
    docs = retrieve_documents(query, db)

    # Join context
    context = "\n\n".join(docs)

    # Confidence score
    confidence = calculate_confidence(docs, query)

    # Escalation keywords
    escalation_keywords = [
        "refund",
        "duplicate charge",
        "fraud",
        "lawsuit",
        "legal",
        "manager",
        "complaint",
        "escalate",
        "payment failed"
    ]

    query_lower = query.lower()

    escalated = (
        confidence < 2
        or any(word in query_lower for word in escalation_keywords)
    )

    # Persona-specific responses
    if persona == "General User":

        response = f"""
I found the following information that may help.

{context}

Recommended Steps

1. Follow the instructions above.
2. If the problem continues, contact customer support.
"""

    elif persona == "Technical Expert":

        response = f"""
Technical Response

Relevant Documentation

{context}

Recommended Technical Actions

• Verify logs.
• Validate configuration.
• Confirm authentication.
• Check server connectivity.
"""

    elif persona == "Business Executive":

        response = f"""
Executive Summary

{context}

Business Impact

• Review service status.
• Follow documented SLA.
• Escalate if operations are affected.
"""

    else:

        response = context

    # Status
    if escalated:
        status = "ESCALATED"
        reason = "Low confidence or sensitive issue"
    else:
        status = "RESOLVED"
        reason = "Knowledge base response"

    return {

        "ticket_id": str(random.randint(100000, 999999)),

        "timestamp": str(datetime.now()),

        "persona": persona,

        "issue": query,

        "response": response,

        "documents_used": docs,

        "confidence": confidence,

        "status": status,

        "reason": reason
    }


# ==========================================================
# Terminal Chatbot
# ==========================================================

if __name__ == "__main__":

    db = build_pipeline()

    print("\n======================================")
    print(" Persona Adaptive Support Agent ")
    print("======================================")

    print("Type 'exit' to quit.\n")

    while True:

        query = input("User: ")

        if query.lower() == "exit":
            print("\nGoodbye 👋")
            break

        persona = detect_persona(query)

        result = generate_answer(
            query=query,
            persona=persona,
            db=db
        )

        print("\n--------------------------------------")
        print("Persona :", result["persona"])
        print("Status  :", result["status"])
        print("Confidence :", result["confidence"])
        print("--------------------------------------\n")

        print(result["response"])

        print("\nTicket ID :", result["ticket_id"])
        print("--------------------------------------\n")
