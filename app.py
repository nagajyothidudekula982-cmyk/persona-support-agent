import streamlit as st
from rag_pipeline import generate_answer, build_pipeline

st.set_page_config(page_title="Persona Support Agent")

st.title("🧠 Persona Support Agent")

@st.cache_resource
def load_db():
    return build_pipeline()

db = load_db()

query = st.text_input("Ask your question")
persona = st.selectbox("Choose Persona", [
    "General User",
    "Technical Expert",
    "Business Executive"
])

if st.button("Generate"):
    if query:
        result = generate_answer(query, persona, db)

        st.subheader("Response")
        st.write(result["response"])

        st.subheader("Status")
        st.write(result["status"])

        st.subheader("Documents Used")
        st.write(result["documents_used"])
    else:
        st.warning("Enter a question")
