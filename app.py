import streamlit as st
from rag_pipeline import build_pipeline, generate_answer

# ==========================================================
# Page Config
# ==========================================================
st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    page_icon="🧠",
    layout="centered"
)

# ==========================================================
# Load DB once (important for Streamlit Cloud)
# ==========================================================
@st.cache_resource
def load_db():
    return build_pipeline()

db = load_db()

# ==========================================================
# UI
# ==========================================================
st.title("🧠 Persona Adaptive Support Agent")

st.write("RAG-based AI system with persona-aware responses and escalation logic")

query = st.text_input("Enter your question")

persona = st.selectbox(
    "Choose Persona",
    ["General User", "Technical Expert", "Business Executive"]
)

# ==========================================================
# Run
# ==========================================================
if st.button("Generate Response"):

    if not query:
        st.warning("Please enter a question")
    else:

        result = generate_answer(query, persona, db)

        st.subheader("🤖 Response")
        st.write(result["response"])

        st.subheader("📊 Confidence")
        st.progress(min(result["confidence"], 10) / 10)
        st.write(result["confidence"])

        st.subheader("📄 Documents Used")
        for i, doc in enumerate(result["documents_used"], 1):
            st.write(f"**Doc {i}:**")
            st.write(doc)

        st.subheader("🎫 Ticket Info")
        st.json({
            "Ticket ID": result["ticket_id"],
            "Persona": result["persona"],
            "Status": result["status"],
            "Timestamp": result["timestamp"]
        })

        if result["status"] == "ESCALATED":
            st.error("🚨 Escalated to human support")
        else:
            st.success("✅ Resolved automatically")
