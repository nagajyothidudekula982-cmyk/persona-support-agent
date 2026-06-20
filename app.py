import gradio as gr
from rag_pipeline import build_pipeline, generate_answer

# ==========================================================
# Load DB (same as Streamlit cache idea)
# ==========================================================
db = build_pipeline()

# ==========================================================
# Main function (NO LOGIC CHANGE)
# ==========================================================
def process(query, persona):

    result = generate_answer(
        query=query,
        persona=persona,
        db=db
    )

    return (
        result["response"],
        result["confidence"],
        result["status"],
        result["documents_used"],
        result["ticket_id"],
        result["timestamp"],
        result["persona"]
    )

# ==========================================================
# UI (minimal + equivalent to your Streamlit app)
# ==========================================================
demo = gr.Interface(
    fn=process,

    inputs=[
        gr.Textbox(
            label="Enter your question",
            placeholder="Example: How do I reset my password?"
        ),
        gr.Dropdown(
            ["General User", "Technical Expert", "Business Executive"],
            label="Choose Persona"
        )
    ],

    outputs=[
        gr.Textbox(label="AI Response"),
        gr.Number(label="Confidence Score"),
        gr.Textbox(label="Status"),
        gr.Textbox(label="Documents Used"),
        gr.Textbox(label="Ticket ID"),
        gr.Textbox(label="Timestamp"),
        gr.Textbox(label="Detected Persona")
    ],

    title="🧠 Persona Adaptive Support Agent",
    description="RAG system with persona adaptation, confidence scoring, and escalation logic"
)

# ==========================================================
# Launch
# ==========================================================
demo.launch()
