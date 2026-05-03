import nltk
import numpy as np
import requests
import random
import re

from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

model = SentenceTransformer('all-MiniLM-L6-v2')

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) 
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_list(text_list):
    return [normalize(item) for item in text_list]

def remove_citations(text):
    return re.sub(r'\[\d+\]', '', text)

def extract_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    return " ".join([p.get_text() for p in paragraphs])


def create_chunks(sentences, chunk_size=5, overlap=2):
    chunks = []
    i = 0

    while i < len(sentences):
        chunk = sentences[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap

    return chunks


urls = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Natural_language_processing",
    "https://www.ibm.com/think/topics/artificial-intelligence",
    "https://www.coursera.org/articles/history-of-ai",
    "https://www.ibm.com/think/topics/artificial-intelligence-business-use-cases"
]

documents = []

for url in urls:
    text = extract_text(url)
    sentences = sent_tokenize(text)

    sentences = [s for s in sentences if 60 < len(s) < 300]

    chunks = create_chunks(sentences, chunk_size=5, overlap=2)
    documents.extend(chunks)

print("Total chunks:", len(documents))


document_embeddings = model.encode(documents)


greetings = [
    "hi", "hello", "hey",
    "good morning", "good afternoon", "good evening",
    "what's up", "whats up"
]

farewells = [
    "bye", "goodbye", "see you", "see ya",
    "later", "good night"
]

greeting_responses = [
    "Hello! How can I help you?",
    "Hi there! What would you like to know?",
    "Hey! Feel free to ask me anything."
]

farewell_responses = [
    "Goodbye! Have a great day!",
    "See you later!",
    "Bye! Come back anytime."
]

response_starters = [
    "Here's a clear explanation based on what I found:\n\n",
    "Based on the information I gathered:\n\n",
    "Here’s what I found about that:\n\n",
    "This is what I could find on your question:\n\n",
    "Let me explain based on available information:\n\n",
    "Here’s a summary of what I found:\n\n",
    "From what I found, here's the explanation:\n\n",
    "This is what the data suggests:\n\n",
    "Here’s a detailed explanation:\n\n",
    "According to the information available:\n\n",
    "Here’s what I discovered:\n\n",
    "Based on relevant sources:\n\n",
    "Here’s what I can tell you:\n\n",
    "From the data I analyzed:\n\n",
    "Here’s a concise explanation:\n\n"
]

bot_identity_questions = [
    "who are you",
    "what are you",
    "what is this chatbot",
    "can you tell me who you are",
    "what kind of bot are you",
    "are you a real person or a bot",
    "what do you do exactly",
    "what’s your purpose",
    "who created you",
    "can you introduce yourself"
]

bot_identity_answers = [
    "I’m Nova, an AI chatbot specialized in artificial intelligence and technology topics. I was created by Mateus Freitas on April 15th, 2026. My purpose is to help users understand complex tech concepts by providing clear and relevant information from multiple data sources.",   
    "I am Nova, an artificial intelligence assistant focused on AI and technology. Developed by Mateus Freitas on April 15th, 2026, my goal is to analyze your questions and deliver accurate, data-driven answers.",
    "I’m Nova, a virtual assistant designed to answer questions about AI and technology. I was created by Mateus Freitas on April 15th, 2026, and my purpose is to make technical knowledge easier to access and understand.",
    "I am Nova, an AI-powered chatbot built to provide insights into technology and artificial intelligence. Created by Mateus Freitas on April 15th, 2026, I use intelligent algorithms to connect your questions with the most relevant answers.",
    "I’m Nova, a chatbot specialized in AI and tech knowledge. I was developed by Mateus Freitas on April 15th, 2026, and my purpose is to deliver accurate information using computational and statistical models.",
    "I am Nova, a digital assistant focused on artificial intelligence and technology. Created by Mateus Freitas on April 15th, 2026, I use multiple data sources and algorithms to understand and respond to your questions effectively.",
    "I’m Nova, an AI chatbot designed to help you explore AI and technology topics. I was built by Mateus Freitas on April 15th, 2026, with the purpose of providing clear, structured, and useful explanations.",
    "I am Nova, an intelligent chatbot created by Mateus Freitas on April 15th, 2026. My purpose is to analyze your questions and generate relevant answers using data and machine learning techniques.",
    "I’m Nova, a technology-focused AI assistant developed by Mateus Freitas on April 15th, 2026. I combine information from multiple sources to provide accurate and helpful responses.",
    "I am Nova, an AI assistant specialized in artificial intelligence and technology. Built by Mateus Freitas on April 15th, 2026, my purpose is to understand your questions and provide clear, reliable answers."
]

def match_intent(text, phrases):
    for term in phrases:
        if term in text:
            return True
    return False

def chatbot(question):
    numero_de_respostas = 1
    original_question = normalize(question.lower())
    print(f"[DEBUG] -> '{original_question}'")

    if match_intent(original_question, normalize_list(greetings)):
        return [random.choice(greeting_responses)]

    if match_intent(original_question, normalize_list(farewells)):
        return [random.choice(farewell_responses)]
    
    if match_intent(original_question, normalize_list(bot_identity_questions)):
        return [random.choice(bot_identity_answers)]

    question_embedding = model.encode([question])

    similarities = cosine_similarity(question_embedding, document_embeddings)

    indices = np.argsort(similarities[0])[-numero_de_respostas:][::-1]
    contexts = [documents[i] for i in indices]

    unique_contexts = []
    for c in contexts:
        if c not in unique_contexts:
            unique_contexts.append(c)

    combined_text = " ".join(unique_contexts)

    combined_text = combined_text[:1000]

    starter = random.choice(response_starters)

    final_response = starter + combined_text

    return [remove_citations(final_response)]


# API Flask
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "")

    response = chatbot(question)

    return jsonify({
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=False)