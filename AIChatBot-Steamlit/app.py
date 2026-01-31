# Command to run this code
# streamlit run AIChatBot-Steamlit/app.py
import streamlit as st
import ollama

MODEL_NAME = "gemma3:1b"  

st.set_page_config(page_title="Ollama Steamlit Chatbot", page_icon="")
st.title("Local AI Chatbot (Ollama + Streamlit)")

# Store chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Ollama
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        stream = ollama.chat(
            model=MODEL_NAME,
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                full_response += chunk["message"]["content"]
                response_container.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
