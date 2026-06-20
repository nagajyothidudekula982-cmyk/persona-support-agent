import streamlit as st
from rag_pipeline import build_pipeline, generate_answer

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    page_icon="🧠",
    layout="centered"
)

# ==========================================================
# Load Vector Database Once
# ==========================================================

@st.cache_resource
def load_db():
    return build_pipeline()

db = load_db()

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("🧠 Persona Support Agent")

st.sidebar.markdown("### Features")

st.sidebar.write("""
✅ Retrieval Augmented Generation (RAG)

✅ ChromaDB Vector Database

✅ Sentence Transformers

✅ Persona Adaptive Responses

✅ Confidence Score

✅ Human Escalation
""")

st.sidebar.markdown("---")

st.sidebar.info(
    "Developed using Python, Streamlit, ChromaDB and Sentence Transformers."
)

# ==========================================================
# Title
# ==========================================================

st.title("🧠 AI Persona Adaptive Customer Support")

st.caption(
    "A Retrieval-Augmented (RAG) chatbot that adapts responses based on different customer personas."
)

st.markdown("---")

# ==========================================================
# User Input
# ==========================================================

query = st.text_area(
    "Enter your question",
    placeholder="Example: How do I reset my password?"
)

persona = st.selectbox(
    "Choose Persona",
    [
        "General User",
        "Technical Expert",
        "Business Executive"
    ]
)

# ==========================================================
# Generate Response
# ==========================================================

if st.button("🚀 Generate Response"):

    if query.strip() == "":
        st.warning("Please enter your question.")

    else:

        with st.spinner("Searching the knowledge base..."):

            result = generate_answer(
                query=query,
                persona=persona,
                db=db
            )

        st.success("Response generated successfully!")

        st.markdown("---")

        st.subheader("👤 Persona")

        st.info(result["persona"])

        st.markdown("---")

        st.subheader("🤖 AI Response")

        st.write(result["response"])

        st.markdown("---")

        st.subheader("📊 Confidence Score")

        confidence = result["confidence"]

        st.progress(min(confidence, 10) / 10)

        if confidence >= 7:
            st.success(f"High Confidence ({confidence}/10)")
        elif confidence >= 4:
            st.warning(f"Medium Confidence ({confidence}/10)")
        else:
            st.error(f"Low Confidence ({confidence}/10)")

        st.markdown("---")

        st.subheader("📄 Retrieved Documents")

        for i, doc in enumerate(result["documents_used"], start=1):

            with st.expander(f"Document {i}"):

                st.write(doc)

        st.markdown("---")

        st.subheader("🎫 Ticket Details")

        st.json({

            "Ticket ID": result["ticket_id"],

            "Issue": result["issue"],

            "Persona": result["persona"],

            "Confidence": result["confidence"],

            "Status": result["status"],

            "Timestamp": result["timestamp"]

        })

        if result["status"] == "ESCALATED":

            st.error("🚨 This issue has been escalated to a human support agent.")

        else:

            st.success("✅ Issue resolved automatically.")

# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    "Built using Python • Streamlit • ChromaDB • Sentence Transformers"
)
