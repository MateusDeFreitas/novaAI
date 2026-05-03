# 🤖 Nova - AI Chatbot for Technology & AI Knowledge

Nova is an AI-powered chatbot designed to answer questions about artificial intelligence and technology. It uses semantic search and natural language processing (NLP) techniques to retrieve and deliver relevant, context-aware information.

---

## 🚀 Features

- 🔍 Semantic search using sentence embeddings  
- 🧠 Natural language understanding with NLP  
- 🌐 Web scraping from trusted sources (IBM, Coursera, Wikipedia)  
- 📦 Text chunking for better context retrieval  
- ⚡ Fast similarity matching using cosine similarity  
- 💬 Intent detection (greetings, farewells, identity)  
- 🌍 REST API built with Flask  

---

## 🧠 How It Works

Nova follows a Retrieval-Augmented Generation (RAG)-like pipeline:

1. **Data Collection**
   - Extracts text from web pages using BeautifulSoup

2. **Text Processing**
   - Splits text into sentences
   - Filters low-quality sentences
   - Groups sentences into chunks with overlap

3. **Embedding**
   - Converts text chunks into vectors using `SentenceTransformer`

4. **User Query Handling**
   - Detects simple intents
   - Converts user input into embeddings

5. **Similarity Search**
   - Compares user query with stored embeddings using cosine similarity
   - Retrieves the most relevant text chunk

6. **Response Generation**
   - Returns the most relevant information with a structured response

---

## 🛠️ Tech Stack

- **Python**
- **Flask** (API)
- **BeautifulSoup** (web scraping)
- **NLTK** (text processing)
- **SentenceTransformers** (embeddings)
- **Scikit-learn** (cosine similarity)
- **NumPy**

---

## 🧪 Input Sugestions
- "What is AI?"
- "Explain machine learning"
- "Who are you?"
- "Hello"
- "Bye"

---

## ⚠️ Limitations
Does not generate original answers (retrieval-based only)
Limited intent detection (rule-based)
No conversation memory
Depends on quality of scraped data

---

## 🚀 Future Improvements
Add LLM for answer generation (true RAG)
Improve intent detection using embeddings
Add conversation memory
Use vector database (FAISS / Pinecone)
Improve data cleaning and ranking

---

## 👨‍💻 Author

Mateus Freitas
AI & Software Engineering

---

## 📅 Project Info
Name: Nova
Created on: April 15th, 2026
Purpose: Help users understand AI and technology through intelligent information retrieval

---

## ⭐ Final Note

Nova is a foundational AI system that demonstrates how modern chatbots work under the hood using embeddings and semantic search — a stepping stone toward more advanced AI systems.
