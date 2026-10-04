# 🤖 Simple AI Chatbot with Memory

A beginner-friendly chatbot that:
- Answers your questions using an AI model (a free Llama model via Groq)
- **Remembers** what you said earlier in the same conversation
- Runs in a clean web page (no coding needed to *use* it)
- Includes a bonus version that can also use a **tool** (a calculator) — a simple taste of "AI Agents"
- Costs **nothing** to run — Groq's API is free, no credit card required

Built with three main building blocks:

| Piece | What it does, in plain terms |
|---|---|
| **Streamlit** | Turns a Python script into a web page with a chat box, buttons, etc. |
| **LangChain** | A toolkit that handles the "plumbing" between your app and the AI model — including memory |
| **Groq (Llama model)** | A free AI model provider that reads your message and writes a reply, very fast |

---

## 📁 What's in this folder

```
app.py             <- the main chatbot (start here)
agent_app.py        <- bonus: a chatbot that can also use a calculator tool
requirements.txt    <- list of Python packages needed
.env.example        <- example of how to store your API key safely
README.md           <- this file
```

---

## 🧠 How the "memory" works (in plain terms)

By itself, an AI model has no memory — every message you send is treated
like the very first message it's ever seen. To fake "memory", the app:

1. Keeps a running list of everything said so far in the chat.
2. Every time you send a new message, it sends the **whole list** back
   to the AI, not just your latest message.
3. The AI reads that list and replies as if it remembers the conversation.

This is handled for you automatically by LangChain's `ConversationBufferMemory`.

---

## 🚀 How to run it on your own computer

**Step 1 — Get a free Groq API key**
Go to https://console.groq.com/keys, sign up with just an email (no
credit card needed), and create a key. Groq's API is free to use.

**Step 2 — Install Python packages**
Open a terminal in this folder and run:
```
pip install -r requirements.txt
```

**Step 3 — Run the chatbot**
```
streamlit run app.py
```
Your browser will open automatically. Paste your API key into the sidebar
and start chatting.

**Step 4 — Try the bonus Agent version (optional)**
```
streamlit run agent_app.py
```
This version can decide to use a calculator tool when your question
involves math — a small taste of what "AI Agents" are.

---

## ☁️ How to put this online (deploy it) so anyone can use it

The easiest free option is **Streamlit Community Cloud**:

1. Create a free GitHub account (if you don't have one) and a new repository.
2. Upload these files to that repository: `app.py`, `requirements.txt`,
   and `README.md`. **Do not upload your real API key anywhere.**
3. Go to https://share.streamlit.io/, sign in with GitHub, and click
   "New app".
4. Pick your repository and select `app.py` as the file to run.
5. Click "Deploy". After a minute or two, you'll get a public web link
   you can share with anyone — they'll paste in their own API key to use it.

---

## ⚠️ A few beginner-friendly notes

- **Keep your API key secret.** Anyone with your key can use your Groq
  account. Never write it directly inside `app.py` or push it to GitHub.
- **You might see a "deprecation warning"** in the terminal when you run
  this — that's just LangChain telling you a newer way exists.
  The code here still works fine and is written this way because it's
  the clearest version for learning the concepts.
- **Costs:** Groq's API is free to use, though it has rate limits (a cap
  on how many messages per minute/day). That's plenty for learning and
  demos. Check current limits at https://console.groq.com/docs/rate-limits
  since free-tier terms can change over time.
- **Python version:** if you hit installation errors, make sure you're
  using Python 3.11 or 3.12 — very new Python versions sometimes don't
  have ready-made versions of some packages yet.
- **Model names change over time.** Groq regularly retires older models
  and replaces them with newer ones. If you ever see a "model not found"
  error, check https://console.groq.com/docs/models for the current
  list and update the `model=` line in `app.py` and `agent_app.py`.
- The calculator tool in `agent_app.py` uses Python's `eval()` in a
  restricted way for demo purposes only — don't use plain `eval()` on
  user input in a real production app.

---

## 📚 Sources used to build this

- Reference video (starting point / inspiration for the basic chatbot structure):
  https://youtu.be/KEwTJSsvQI0
- Official docs used to write and structure the code:
  - Streamlit chat elements: https://docs.streamlit.io/develop/api-reference/chat
  - LangChain memory concepts: https://python.langchain.com/docs/modules/memory/
  - LangChain agents & tools: https://python.langchain.com/docs/modules/agents/
  - Groq API reference: https://console.groq.com/docs

I don't have live web access while writing this, so please double-check
these links still work and match the latest library versions before
relying on them — LangChain especially changes its API fairly often.
