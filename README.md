# 🧠 Persona Adaptive Customer Support Agent (RAG-Based AI System)

## 🚀 Overview

This project is an intelligent **Persona-Aware Customer Support Agent** built using **Retrieval-Augmented Generation (RAG)**.
It retrieves relevant knowledge from a vector database and generates responses based on the selected user persona.

The system adapts responses for:

* 👤 General Users
* 🧑‍💻 Technical Experts
* 🏢 Business Executives

It also includes **confidence scoring** and **automatic escalation to human support** for low-confidence or sensitive queries.

---

## 🏗️ Architecture

```
User Query
   ↓
Persona Selection
   ↓
Sentence Embedding (MiniLM)
   ↓
ChromaDB Vector Search
   ↓
Top-K Document Retrieval
   ↓
Confidence Evaluation
   ↓
Response Generation (Persona-Based)
   ↓
Escalation (if needed)
```

---

## ✨ Features

* 🔍 Semantic Search using Sentence Transformers
* 📚 Vector Database using ChromaDB
* 🧠 Persona-based response generation
* 📊 Confidence scoring system
* 🚨 Smart escalation to human support
* 🎫 Ticket generation for each query
* 💻 Streamlit interactive UI

---

## 🧠 Personas Supported

### 👤 General User

Simple, step-by-step instructions.

### 🧑‍💻 Technical Expert

Detailed technical troubleshooting guidance.

### 🏢 Business Executive

High-level business impact and summary insights.

---

## 🧰 Tech Stack

* Python 🐍
* Streamlit
* ChromaDB
* SentenceTransformers
* HuggingFace Models
* PyTorch

---

## 📁 Project Structure

```
persona-support-agent/
│
├── app.py
├── rag_pipeline.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── api_authentication.md
│   ├── billing_support.txt
│   ├── password_reset.txt
│   └── troubleshooting.txt
│
├── src/
│   ├── classifier.py
│   ├── config.py
│   ├── escalator.py
│   ├── generator.py
│   └── rag_pipeline.py
```

---

## ⚙️ How It Works

1. User enters a query in Streamlit UI
2. Query is converted into embeddings
3. ChromaDB retrieves most relevant documents
4. System evaluates confidence score
5. Persona-based response is generated
6. If confidence is low → escalation triggered

---

## 📊 Confidence & Escalation Logic

The system escalates when:

* Confidence score is low
* Query contains sensitive keywords (refund, fraud, legal, complaint)

### Escalation Output:

* Ticket ID generated
* Query logged
* Human support recommended

---

## ▶️ Installation & Run

### 1. Clone repo

```bash
git clone https://github.com/nagajyothidudekula982-cmyk/persona-support-agent.git
cd persona-support-agent
```

### 2. Create environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run app

```bash
streamlit run app.py
```

---

## 🌐 Future Improvements

* LLM integration (GPT/Gemini)
* Multi-turn conversations
* User authentication
* Feedback loop system
* Analytics dashboard

---

## 👨‍💻 Author

**Dudekula Nagajyothi**

AI/ML Enthusiast | RAG Systems Developer | Python Developer
