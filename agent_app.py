"""
Bonus: A Simple AI Agent (an AI that can use tools)
-----------------------------------------------------
A regular chatbot can only answer using what it already "knows".
An "Agent" is an AI that can decide, on its own, to use a tool -
like a calculator - to get a better answer, then reply to you.

This example gives the AI ONE tool: a calculator. Try asking it:
  - "What is 245 * 89?"
  - "If I save 500 a month for 2 years, how much is that?"
  - "What's the capital of Japan?" (it will answer directly, no tool needed)

Run it the same way as app.py:
    streamlit run agent_app.py
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="AI Agent with Tools", page_icon="🛠️")
st.title("🛠️ AI Agent with a Calculator Tool")
st.caption("Same idea as app.py, but this AI can also use a tool when it needs to.")

with st.sidebar:
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("[Get a free API key here](https://console.groq.com/keys)")
    if st.button("Clear chat"):
        st.session_state.clear()
        st.rerun()

if not api_key:
    st.info("👈 Please add your free Groq API key in the sidebar to start.")
    st.stop()


# A "tool" is just a normal Python function that we let the AI call
# when it decides it needs one. Here, it's a basic calculator.
# Note: eval() is restricted to numbers/math only - fine for a demo,
# but never use plain eval() on user input in a real production app.
def calculator(expression: str) -> str:
    try:
        allowed = {"__builtins__": {}}
        return str(eval(expression, allowed))
    except Exception as e:
        return f"Couldn't calculate that: {e}"


tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Use this ONLY for math calculations, e.g. '245 * 89' or '(500*24)'.",
    )
]

if "agent_memory" not in st.session_state:
    st.session_state.agent_memory = ConversationBufferMemory(memory_key="chat_history")

if "agent_chat" not in st.session_state:
    st.session_state.agent_chat = []

llm = ChatGroq(api_key=api_key, model="openai/gpt-oss-20b", temperature=0)

# This agent type is made for chatbots: it keeps conversation memory
# AND can decide when to reach for a tool from the list above.
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=st.session_state.agent_memory,
    verbose=True,          # prints the agent's "thinking steps" in your terminal
    handle_parsing_errors=True,
)

for role, text in st.session_state.agent_chat:
    with st.chat_message(role):
        st.markdown(text)

user_input = st.chat_input("Ask me anything, or give me a math problem...")
if user_input:
    st.session_state.agent_chat.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.run(user_input)
            st.markdown(response)

    st.session_state.agent_chat.append(("assistant", response))
