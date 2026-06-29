<div align="center">

# 🔍 CodeSense — AI Code Review Assistant

**Resume Project #3 ⭐ · Akshay Kiran Rajput · GenAI Developer Portfolio**

> Paste any code → get a senior engineer's review in seconds.
> Bugs · Security · Refactored Code · Unit Tests · Streamed live.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=flat-square)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Free_Tier-F55036?style=flat-square)](https://groq.com)
[![Live App](https://img.shields.io/badge/🚀_Live_App-codesense.streamlit.app-FF4B4B?style=flat-square)](YOUR_STREAMLIT_URL_HERE)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

### 🚀 [Live Demo → your-app.streamlit.app](https://code-review-bot.streamlit.app/)

**3 Free LLMs · 8 Review Modes · 22 Languages · File Upload · Conversation Memory · Streamed**

</div>

---

## 📋 Table of Contents

- [📸 Screenshots](#-application-screenshots)
- [🧠 What It Does](#-what-it-does)
- [💡 Why CodeSense Stands Out](#-why-codesense-stands-out)
- [✨ Features](#-features)
- [🏗 Architecture](#-architecture)
- [📁 Project Structure](#-project-structure)
- [⚡ Run Locally](#-run-locally)
- [🌐 Deploy on Streamlit Cloud](#-deploy-free-on-streamlit-cloud)
- [🔑 Review Modes](#-review-modes)
- [🤖 Available Models](#-available-models-all-free-on-groq)
- [🛠 Tech Stack](#-tech-stack)
- [✍️ Resume Bullets](#️-resume-bullets)
- [💬 Interview Talking Points](#-interview-talking-points)
- [🔮 Future Improvements](#-future-improvements)
- [👤 Author](#-author)

---

## 📸 Application Screenshots

> 📌 **To add screenshots:** Run the app → take screenshots of each screen below → save in a `screenshots/` folder in the repo root.

### 🏠 Home — Hero Banner, Pipeline & Model Selector

<p align="center">
  <img src="screenshots/home.png" width="100%" alt="CodeSense Home — Hero Banner and Model Selector">
</p>

The home screen shows the **"Get a senior engineer's review in seconds"** hero banner, a workflow pipeline strip (Paste Code → Pick Model → Get Review → Follow-up → Ship Better Code), and the 3-model card selector. The sidebar shows the Groq API key field with **⚡ 100% FREE · NO CREDIT CARD** badge.

---

### 🔍 Code Input & Review Mode Selector

<p align="center">
  <img src="screenshots/code_input.png" width="100%" alt="Code Input with Review Mode and File Upload">
</p>

Paste code directly into the editor or upload a file (`.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.sql`, `.sh`, and more). Select language from 22 options and choose one of 8 review modes — the active mode description updates live below the **Review My Code →** button.

---

### 💬 Full Code Review — Streamed Response

<p align="center">
  <img src="screenshots/review.png" width="100%" alt="Full AI Code Review Streamed Response">
</p>

CodeSense streams back a structured senior-engineer review covering Code Quality, Bugs & Issues, Security Analysis, Performance, Best Practices, Refactored Code, Unit Tests, and Learning Resources — all in real time, token by token.

---

### ⚡ Quick Follow-up Prompts & Conversation Memory

<p align="center">
  <img src="screenshots/followup.png" width="100%" alt="Quick Follow-up Prompts and Conversation Memory">
</p>

After the initial review, 8 one-click follow-up prompts appear — time complexity, unit tests, design patterns, async conversion, error handling, and more. The full conversation history is preserved via LangChain `MessagesPlaceholder` so every follow-up has full context.

---

### ☁️ Live on Streamlit Cloud

<p align="center">
  <img src="screenshots/deploy.png" width="100%" alt="CodeSense Live on Streamlit Cloud">
</p>

CodeSense runs live on Streamlit Cloud — accessible from any browser worldwide, no local setup required.

---

## 🧠 What It Does

Most developers paste code into ChatGPT and get an unstructured wall of text back. **CodeSense gives you a structured pull-request review** — the kind you'd get from a senior engineer before merging to production.

Paste any code snippet or upload a file → select a language and review mode → get back a fully structured review streamed token-by-token in real time. Ask follow-up questions and CodeSense remembers the full conversation context.

**Built to demonstrate:**
- Real-world **LangChain LCEL** chain composition with multi-turn memory
- **Groq API** integration with token-by-token streaming via `chain.stream()`
- **Live API key validation** — real Groq test call on entry, rejects fake keys instantly
- **8 dynamic review modes** using adaptive system prompting that restructures LLM output format per mode
- Clean, modular Python architecture deployed on Streamlit Cloud

---

## 💡 Why CodeSense Stands Out

| | **CodeSense** | **Typical AI Code Tool** |
|---|---|---|
| **Review Structure** | 8-section structured output (Bugs · Security · Tests · Refactor) | Unstructured text blob |
| **Review Modes** | 8 modes — each restructures the LLM's output format | Single generic prompt |
| **Languages** | 22 languages + Auto-detect | Usually Python-only demos |
| **Input Methods** | Paste code OR upload a file | Paste only |
| **Memory** | LangChain `MessagesPlaceholder` — last 20 messages | Stateless, no follow-ups |
| **Key Validation** | Live Groq test call — fake keys rejected instantly | No validation |
| **Models** | 3 switchable LLMs mid-session | Single hardcoded model |
| **Cost** | **$0.00** — Groq free tier | Paid API |

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎯 **8 Review Modes** | Full Review · Bug Hunt · Security Audit · Performance · Unit Tests · Explain Code · Refactor Only · Beginner Friendly |
| 🌐 **22 Languages** | Python · JS · TypeScript · Java · Go · Rust · SQL · C++ · C · Bash · PHP · Swift · Kotlin · React/JSX · Vue · Ruby · Scala · R · MATLAB · Dart · HTML/CSS · Auto-detect |
| 📁 **File Upload** | Upload `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.sql`, `.sh` and more — no copy-paste needed |
| ⚡ **Streaming Responses** | Token-by-token output via Groq LPU — near-instant feel |
| 🧠 **Conversation Memory** | LangChain `MessagesPlaceholder` keeps last 20 messages in context |
| 🔑 **Live API Key Validation** | Real Groq test call on entry — invalid keys rejected immediately with error message |
| 💬 **8 Quick Follow-ups** | One-click: time complexity · unit tests · design patterns · async · error handling · type hints |
| 📦 **6 Built-in Examples** | SQL injection · Async race condition · O(n²) loop · Memory leak · Missing error handling · Clean code reference |
| 🤖 **3-Model Selector** | Switch GPT-OSS 20B · 120B · Qwen 3.6 27B before each session |
| 📊 **Session Stats** | Live review count and message count tracked in sidebar |
| 🎨 **Dark Theme UI** | Custom CSS dark theme — Space Grotesk + JetBrains Mono fonts |
| 🔧 **test_groq.py** | Standalone key validator script — verify your key before running the app |

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend  (app.py)              │
│   Sidebar · Model Cards · Code Input · File Upload · Chat    │
└──────────────────────┬───────────────────────────────────────┘
                       │  API key entry
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              Key Validation  (llm_engine.py)                  │
│                                                              │
│  validate_api_key()                                          │
│    └→ live Groq().chat.completions.create(max_tokens=1)      │
│    └→ 401 → invalid · 429 → valid (rate limited) · else ok   │
└──────────────────────┬───────────────────────────────────────┘
                       │  valid key → build chain
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              LangChain LCEL Chain  (llm_engine.py)            │
│                                                              │
│  ChatPromptTemplate.from_messages([                          │
│    ("system", SYSTEM_PROMPT),        ← CodeSense persona     │
│    MessagesPlaceholder("history"),   ← last 20 messages      │
│    ("human", "{input}"),             ← code + mode + lang    │
│  ])                                                          │
│                       │                                      │
│  ChatGroq(model=model_id, streaming=True, temperature=0.3)   │
│    └→ GPT-OSS 20B / 120B / Qwen 3.6 27B                     │
│                       │                                      │
│  StrOutputParser()  →  streamed text chunks                  │
└──────────────────────┬───────────────────────────────────────┘
                       │  chain.stream({input, history})
                       ▼
┌──────────────────────────────────────────────────────────────┐
│    st.empty() accumulates chunks → live markdown render       │
│    "▌" cursor appended on each chunk for typewriter feel     │
└──────────────────────────────────────────────────────────────┘
```

**Review prompt construction:**
```
build_user_message(code, language, mode, mode_desc)
  → "Please review the following code (Python).
     Review mode: Full Review — Complete audit…
     ```python
     <code>
     ```"
```

---

## 📁 Project Structure

```
CodeSense/
│
├── app.py              ← Streamlit UI: sidebar, model cards, code input, file upload, chat
├── llm_engine.py       ← LangChain chain · API key validation · prompt builder · streaming
├── config.py           ← System prompt · models · languages · review modes · examples
├── test_groq.py        ← Standalone key validator — run before app to verify key works
│
├── screenshots/        ← App screenshots used in this README
│   ├── home.png
│   ├── code_input.png
│   ├── review.png
│   ├── followup.png
│   └── deploy.png
│
├── requirements.txt    ← All dependencies
├── .env.example        ← API key template (copy to .env — never commit .env!)
├── .gitignore          ← Excludes .env · __pycache__/
└── README.md
```

---

## ⚡ Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/Akshay291/CodeSense.git
cd CodeSense
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key

Go to **[console.groq.com/keys](https://console.groq.com/keys)** → Sign up → Create API Key
No credit card needed · Free tier: **1,000 requests/day**

### 4. Set up your `.env` file

**Windows:**
```cmd
copy .env.example .env
```

**Mac / Linux:**
```bash
cp .env.example .env
```

Open `.env` and paste your key:
```env
GROQ_API_KEY=gsk_your_key_here
```

> ⚠️ Never commit `.env` — it's already in `.gitignore`

### 5. (Optional) Verify your key works

```bash
python test_groq.py
# ✅ Groq API is working!
```

### 6. Launch the app

```bash
streamlit run app.py
```

Open **[http://localhost:8501](http://localhost:8501)** in your browser.

**Workflow:** Enter API key in sidebar → key validated live → select model → paste code or upload file → select language & mode → click **Review My Code →** → ask follow-up questions!

---

## 🌐 Deploy Free on Streamlit Cloud

1. Push this repo to GitHub
2. Go to **[share.streamlit.io](https://share.streamlit.io)** → Sign in with GitHub
3. Click **New app** → Select your repo → Set main file path to `app.py`
4. Click **Advanced settings** → **Secrets** → paste:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
5. Click **Deploy** — Streamlit auto-installs from `requirements.txt`, live in ~2 minutes

---

## 🔑 Review Modes

| Mode | What It Does |
|---|---|
| 🔍 **Full Review** | Complete 8-section audit — bugs, security, performance, refactored code, unit tests |
| 🐛 **Bug Hunt** | Laser-focused on logical errors and incorrect behaviour only |
| 🔒 **Security Audit** | SQL injection · exposed secrets · unvalidated input · unsafe patterns |
| ⚡ **Performance Review** | Algorithmic complexity · bottlenecks · memory usage · Big-O analysis |
| 🧪 **Add Unit Tests** | Writes a comprehensive unit test suite for the submitted code |
| 📖 **Explain This Code** | Plain English explanation — perfect for onboarding or unfamiliar codebases |
| ✨ **Refactor Only** | Rewrites the code cleaner and more idiomatic — no logic changes |
| 🎓 **Beginner Friendly** | Encouraging tone · plain explanations · learning-focused feedback |

---

## 🤖 Available Models (all free on Groq)

| Model | Provider | Speed | Context | Best For |
|---|---|---|---|---|
| **GPT-OSS 20B** | OpenAI OSS | Very Fast | 128K | Speed-critical tasks, high-volume reviews |
| **GPT-OSS 120B** | OpenAI OSS | Fast | 128K | Deep analysis, complex bugs, architecture review |
| **Qwen 3.6 27B** | Alibaba | Fast | 128K | Multilingual code, broad language support |

Switch models before each session from the model card selector — clear chat to switch mid-session.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit 1.28+ · Custom CSS dark theme · Space Grotesk + JetBrains Mono |
| **LLM** | Groq API — GPT-OSS 20B / 120B · Qwen 3.6 27B · `streaming=True` |
| **LLM Orchestration** | LangChain 0.3 · `ChatGroq` · `ChatPromptTemplate` · `MessagesPlaceholder` · `StrOutputParser` |
| **Memory** | `MessagesPlaceholder` — stateful multi-turn conversation (last 20 messages) |
| **Streaming** | `chain.stream()` → `st.empty()` live markdown renderer with `▌` cursor |
| **Key Validation** | Live `groq.Groq()` test call — 401 = invalid, 429 = valid (rate limited) |
| **Config** | `python-dotenv` · centralized `config.py` · `test_groq.py` standalone validator |

---

## ✍️ Resume Bullets

```
• Built CodeSense, an AI Code Review Assistant using LangChain + Groq API with
  real-time token-by-token streaming and multi-turn conversation memory; users
  paste or upload code and get a structured senior-engineer review — deployed
  live on Streamlit Cloud

• Engineered 8 dynamic review modes (Full Review, Bug Hunt, Security Audit,
  Performance, Unit Tests, Explain Code, Refactor, Beginner Friendly) using
  adaptive system prompting that restructures the LLM's 8-section output format
  based on user selection across 22 supported programming languages

• Implemented live API key validation via real Groq test call on entry,
  LangChain MessagesPlaceholder memory retaining last 20 messages for contextual
  follow-ups, file upload for 14+ extensions, and graceful error handling for
  rate limits and auth failures
```

---

## 💬 Interview Talking Points

**Q: What is the system prompt doing and why is it so detailed?**
> The system prompt defines the CodeSense persona — a senior engineer with 10+ years of experience — and prescribes the exact 8-section output format: Summary, What's Good, Bugs, Improvements, Security, Metrics, Refactored Code, Unit Tests, and Resources. Without this structure, the LLM returns unformatted text. The prompt is the contract between the application and the model — it's the most important engineering decision in the whole system.

**Q: How do the 8 review modes work technically?**
> Each mode has a description string in `config.py`. When the user selects a mode, `build_user_message()` injects both the mode name and its description into the human message: `"Review mode: Bug Hunt — Focus ONLY on bugs and logical errors."` This single line overrides the full-review default in the system prompt, causing the model to restructure its entire response around that focus area — no separate chain or prompt needed per mode.

**Q: How does the conversation memory work?**
> `MessagesPlaceholder` is a special LangChain prompt slot that injects a list of past `HumanMessage` and `AIMessage` objects into the prompt at inference time. `get_lc_history()` converts Streamlit's session state list into LangChain message objects and slices the last 20 to stay within context limits. Every call to `chain.stream()` passes this history — so the model has full context of the previous review when answering follow-up questions.

**Q: How does the live API key validation work?**
> `validate_api_key()` makes a real, minimal Groq API call (`max_tokens=1`, content="hi") the moment the user pastes a key. A `401` response means the key is invalid and we show an error immediately — the user can't proceed with a fake key. A `429` (rate limit) means the key is valid but temporarily throttled, so we let the user in. This is far better than just checking the key format — it catches revoked keys, wrong environment keys, and typos instantly.

**Q: How does streaming work in this app?**
> `chain.stream()` returns a Python generator that yields text chunks as the LLM produces them. In Streamlit, we loop over these chunks with `for chunk in stream_response(...)`, accumulate them into a `response` string, and call `container.markdown(response + "▌")` on every iteration — the `▌` cursor gives the typewriter effect. Once streaming finishes, we call `container.markdown(response)` without the cursor to set the final text.

**Q: Why use LangChain instead of calling Groq directly?**
> Groq's SDK handles a single completion call well, but LangChain adds three things we need: `ChatPromptTemplate` for structured prompt composition with typed slots, `MessagesPlaceholder` for clean history injection, and `StrOutputParser` for turning the chat response into a plain string. The LCEL `|` pipe syntax also makes the chain easy to swap — changing the model is one line (`ChatGroq(model=new_id)`), and the rest of the chain is untouched.

**Q: What's the difference between the 8 review modes from an LLM perspective?**
> The system prompt defines the default 8-section output. Each review mode appends a focused instruction to the human message that overrides the default behaviour — "Focus ONLY on vulnerabilities" for Security Audit, "Write a comprehensive unit test suite" for Add Unit Tests. The LLM follows instruction hierarchy: human message overrides system prompt for specifics, so the mode instruction reliably reshapes the output without needing a separate system prompt per mode.

---

## 🔮 Future Improvements

| Improvement | Why It Matters |
|---|---|
| **GitHub PR integration** | Review actual pull request diffs instead of pasted snippets |
| **Diff view for refactored code** | Side-by-side original vs refactored instead of just showing the new version |
| **Severity scoring** | Rate bugs/issues as Critical / High / Medium / Low for triage prioritization |
| **Export review to PDF/DOCX** | Let developers save and share the full review as a document |
| **Multi-file upload** | Review an entire module or package, not just single files |
| **Chat history persistence** | Save review sessions to disk so developers can revisit past reviews |

---

## 👤 Author

**Akshay Kiran Rajput**
MCA Student · Jain Online University · Surat, Gujarat, India

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Akshay_Rajput-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/akshay-rajput-0925b8264)
[![GitHub](https://img.shields.io/badge/GitHub-Akshay291-181717?style=flat-square&logo=github)](https://github.com/Akshay291)
[![Email](https://img.shields.io/badge/Email-akshayrajput2914@gmail.com-EA4335?style=flat-square&logo=gmail)](mailto:akshayrajput2914@gmail.com)
[![Live App](https://img.shields.io/badge/Live_App-CodeSense-FF4B4B?style=flat-square&logo=streamlit)](YOUR_STREAMLIT_URL_HERE)

---

<div align="center">

If this project helped you, consider giving it a ⭐ — it helps others find it!

<sub>CodeSense · Resume Project #3 ⭐ · LangChain · Groq · Streamlit · Space Grotesk</sub>

</div>
