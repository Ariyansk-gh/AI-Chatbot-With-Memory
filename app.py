"""
Simple AI Chatbot with Memory
------------------------------
A beginner-friendly chatbot built with:
  - Streamlit   -> the web page/chat screen you see and click on
  - LangChain   -> a toolkit that makes it easy to talk to AI models
  - Groq        -> a FREE AI model provider (no credit card needed) that
                   runs the "brain" writing the replies

What does "memory" mean here?
On its own, an AI model forgets everything the moment it answers you.
To give it "memory", we keep a running record of everything said so
far in the chat, and we send that whole record back to the AI every
time you send a new message. That's what makes it feel like it
remembers your name, your last question, etc.

How to run this file:
  1. Install the requirements:  pip install -r requirements.txt
  2. Run the app:                streamlit run app.py
  3. Paste your free Groq API key in the sidebar when the browser opens.
     Get one at: https://console.groq.com/keys (just needs an email,
     no credit card).

See README.md in this folder for full setup steps and where the
ideas in this code come from.
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# ---------- 1. Page setup (the title and layout you see) ----------
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("🤖 My AI Chatbot")
st.caption("A simple chatbot built with Streamlit + LangChain + Groq (free)")

# ---------- 2. Get the API key from the person using the app ----------
# Never type your real API key directly into the code. We ask for it
# in the sidebar instead, so it's never saved in the file or on GitHub.
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("[Get a free API key here](https://console.groq.com/keys)")
    if st.button("Clear chat"):
        st.session_state.clear()
        st.rerun()

if not api_key:
    st.info("👈 Please add your free Groq API key in the sidebar to start chatting.")
    st.stop()

# ---------- 3. Set up the "brain" (the AI model) and its memory ----------
# st.session_state is Streamlit's way of remembering things between
# messages, for as long as the browser tab stays open. We create the
# memory and the message list only ONCE per session, not every message.
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # what gets displayed on screen

llm = ChatGroq(
    api_key=api_key,
    model="openai/gpt-oss-20b",  # a fast, free model - great for learning
    temperature=0.7,                # 0 = focused/predictable, 1 = more creative
)

# ConversationChain automatically reads and updates the memory for you,
# so you don't have to manually stitch past messages together.
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.memory,
    verbose=False,
)

# ---------- 4. Re-display any earlier messages ----------
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# ---------- 5. Handle a new message from the user ----------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show the user's message right away
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Ask the AI for a reply - it automatically uses the memory above,
    # so it can refer back to earlier parts of the conversation.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input=user_input)
            st.markdown(response)

    # Save the AI's reply so it's still shown after the page refreshes
    st.session_state.chat_history.append(("assistant", response))
