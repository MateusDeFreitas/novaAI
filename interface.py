import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/chat"

st.set_page_config(page_title="Nova AI", layout="centered")

st.title("Hello, I am Nova")
st.caption("What can I do for you today?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = requests.post(API_URL, json={"question": user_input})

        if response.status_code == 200:
            data = response.json()
            bot_reply = "\n\n".join(data["response"])
        else:
            bot_reply = "Error: Unable to get response from server."

    except Exception as e:
        bot_reply = "Connection error. Make sure the Flask API is running."

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })