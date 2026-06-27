<div align="center">

# 🔍 AI Code Review Assistant

**Resume Project #3 · Akshay Kiran Rajput · GenAI Developer Portfolio**

Paste code → get a senior engineer's review in seconds.
Bugs · Security · Best Practices · Refactored Code · Streamed live.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=flat-square)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=flat-square)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

🚀 **[Live Demo →](YOUR_STREAMLIT_URL_HERE)**

</div>

---

## 📸 Screenshots

> _Add a screenshot of your running app here after deployment_

---

## 🧠 What It Does

Upload any code snippet and this tool acts as a **senior engineer reviewing your pull request** — streaming a structured, detailed review back to you in real time. Ask follow-up questions and it remembers the full conversation context.

Built to demonstrate:
- Real-world **LangChain** chain composition with memory
- **Groq API** integration with token-by-token streaming
- Multi-turn **conversational AI** in a production-style Streamlit UI
- Clean, modular Python project structure ready for deployment

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎯 **5 Review Modes** | Full Review · Bug Hunt · Security Audit · Performance · Beginner Friendly |
| 🌐 **16 Languages** | Python · JavaScript · TypeScript · Java · Go · Rust · SQL · C++ · Bash · and more |
| ⚡ **Streaming Responses** | Token-by-token output via Groq's LPU — faster than any GPU inference |
| 🧠 **Conversation Memory** | LangChain `MessagesPlaceholder` keeps last 20 messages in context |
| 🔑 **Real API Key Validation** | Live test call on key entry — rejects fake/invalid keys instantly |
| 💬 **Quick Follow-up Prompts** | One-click: time complexity · unit tests · design patterns · error handling |
| 📦 **4 Built-in Examples** | SQL injection bug · Async race condition · O(n²) loop · Clean code reference |
| 📊 **Session Stats** | Review count and message count tracked live in sidebar |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│         Code Input · Mode Selector · Chat History           │
└─────────────────────┬───────────────────────────────────────┘
                      │  user message
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    LangChain Chain                           │
│                                                             │
│   ChatPromptTemplate                                        │
│   ├── SystemMessage  →  Senior Engineer persona             │
│   ├── MessagesPlaceholder  →  last 20 messages (memory)    │
│   └── HumanMessage  →  code + language + review mode       │
│                      │                                      │
│                      ▼                                      │
│   ChatGroq  (llama-3.3-70b-versatile, streaming=True)      │
│                      │                                      │
│                      ▼                                      │
│   StrOutputParser  →  streamed text chunks                  │
└─────────────────────┬───────────────────────────────────────┘
                      │  streamed tokens
                      ▼
┌─────────────────────────────────────────────────────────────┐
│          st.empty() live markdown renderer                   │
│          response builds character by character             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
code_review_bot/
│
├── app.py            ← Streamlit UI — sidebar, chat, streaming renderer
├── llm_engine.py     ← LangChain chain · API key validation · streaming
├── config.py         ← System prompt · model config · languages · examples
│
├── requirements.txt  ← Pinned dependencies
├── .env              ← GROQ_API_KEY (never commit this!)
├── .gitignore        ← Excludes .env and __pycache__
├── test_groq.py      ← Standalone key validator script
└── README.md
```

---

## ⚡ Run Locally

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/code-review-assistant.git
cd code-review-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key

Go to **[console.groq.com/keys](https://console.groq.com/keys)** → Sign up → Create API Key
No credit card needed. Free tier: **30 req/min · 14,400 req/day**

### 4. Add key to `.env`

```env
GROQ_API_KEY=gsk_your_key_here
```

### 5. (Optional) Verify your key

```bash
python test_groq.py
# ✅ Groq API is working!
```

### 6. Launch

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🌐 Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to **[share.streamlit.io](https://share.streamlit.io)**
3. Connect repo → select `app.py` → click **Deploy**
4. In app settings → **Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
5. Copy the live URL → paste into your resume + LinkedIn

---

## 🔑 Review Modes

| Mode | What It Does |
|---|---|
| **Full Review** | Complete audit — bugs, best practices, security, refactored code |
| **Bug Hunt Only** | Laser-focused on logical errors and incorrect behaviour |
| **Security Audit** | SQL injection · exposed secrets · unvalidated input · unsafe patterns |
| **Performance Review** | Algorithmic complexity · bottlenecks · memory usage · optimisation |
| **Beginner Friendly** | Encouraging tone · plain explanations · learning-focused feedback |

---

## 🤖 Model

| Property | Value |
|---|---|
| **Provider** | [Groq](https://groq.com) |
| **Model** | `llama-3.3-70b-versatile` |
| **Free Tier** | ✅ 30 req/min · 14,400 req/day |
| **Inference Speed** | ~500 tokens/sec (Groq LPU hardware) |
| **Works in India** | ✅ No regional restrictions |
| **Context Window** | 128K tokens |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit · Custom CSS (dark glassmorphism theme) |
| **LLM Orchestration** | LangChain 0.3 · `ChatGroq` · `ChatPromptTemplate` |
| **AI Model** | LLaMA 3.3 70B via Groq API |
| **Memory** | `MessagesPlaceholder` — stateful multi-turn conversation |
| **Streaming** | `chain.stream()` → `st.empty()` live renderer |
| **Config** | `python-dotenv` · centralised `config.py` |

---

## ✍️ Resume Bullets

Copy-paste ready for your CV or LinkedIn:

```
• Built an AI Code Review chatbot using LangChain + Groq API (LLaMA 3.3 70B)
  with real-time token-by-token streaming and multi-turn conversation memory
  across follow-up questions — deployed live on Streamlit Cloud

• Engineered 5 dynamic review modes (Full Review, Bug Hunt, Security Audit,
  Performance, Beginner Friendly) using adaptive system prompting that
  restructures the LLM's output format based on user selection

• Implemented real API key validation via live Groq test call on entry,
  LangChain MessagesPlaceholder memory retaining last 20 messages, and
  graceful error handling for rate limits and auth failures
```

---

## 👤 Author

**Akshay Kiran Rajput**
MCA Student · Jain Online University · Surat, India

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/YOUR_USERNAME)
[![Email](https://img.shields.io/badge/Email-akshayrajput2914@gmail.com-EA4335?style=flat-square&logo=gmail)](mailto:akshayrajput2914@gmail.com)

---

<div align="center">
<sub>Code Review Assistant · Resume Project #3 · Built with LangChain · Groq · Streamlit</sub>
</div>
