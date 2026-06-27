"""
app.py — Code Review Assistant
Resume Project #3 | Akshay Kiran Rajput
Run: streamlit run app.py
"""

import streamlit as st
from llm_engine import (
    build_chain,
    validate_api_key,
    build_user_message,
    build_followup_message,
    stream_response,
)
from config import LANGUAGES, REVIEW_MODES, QUICK_PROMPTS, EXAMPLE_SNIPPETS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Code Review Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

[data-testid="stAppViewContainer"]{background:#07070f;font-family:'Plus Jakarta Sans',sans-serif}
[data-testid="stSidebar"]{background:#0d0d1d;border-right:1px solid #1e1e3a}
h1,h2,h3,p,label{color:#edeaf8 !important}

[data-testid="stChatMessage"]{background:#131328;border:1px solid #222240;border-radius:10px;margin-bottom:8px}

code{font-family:'JetBrains Mono',monospace !important;font-size:13px}
pre{background:#0d0d1d !important;border:1px solid #222240;border-radius:8px;padding:14px}

.stSelectbox label,.stTextArea label,.stSlider label{color:#8b89a8 !important;font-size:12px}
.stButton button{border-radius:7px;font-weight:600;font-size:13px}
.stButton button[kind="primary"]{background:linear-gradient(135deg,#8b7cf8,#6c63d8);border:none}

.badge{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:10px;
       padding:3px 10px;border-radius:4px;font-weight:600;letter-spacing:1px}
.badge-purple{background:rgba(139,124,248,.15);color:#b4a9ff;border:1px solid rgba(139,124,248,.3)}
.badge-green {background:rgba(16,217,160,.12); color:#4eedc4;border:1px solid rgba(16,217,160,.25)}
.badge-red   {background:rgba(255,95,126,.12); color:#ff8fa3;border:1px solid rgba(255,95,126,.25)}
.badge-gold  {background:rgba(255,179,71,.12); color:#ffb347;border:1px solid rgba(255,179,71,.25)}

.stat-row{display:flex;gap:12px;margin:10px 0 18px}
.stat-box{background:#131328;border:1px solid #222240;border-radius:8px;
          padding:10px 14px;flex:1;text-align:center}
.stat-box .n{font-size:20px;font-weight:800;color:#b4a9ff;line-height:1}
.stat-box .l{font-size:10px;color:#6e6c90;margin-top:3px;font-family:'JetBrains Mono',monospace}

.callout{background:rgba(139,124,248,.07);border-left:3px solid #8b7cf8;
         border-radius:6px;padding:10px 14px;margin:8px 0;color:#edeaf8;font-size:13px}
.callout-green{background:rgba(16,217,160,.07);border-left-color:#10d9a0}
.callout-gold {background:rgba(255,179,71,.07); border-left-color:#ffb347}
</style>
""",
    unsafe_allow_html=True,
)


# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "review_count" not in st.session_state:
    st.session_state.review_count = 0
if "chain" not in st.session_state:
    st.session_state.chain = None
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "last_language" not in st.session_state:
    st.session_state.last_language = "Python"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Code Review Assistant")
    st.markdown("**Resume Project #3** · Akshay Kiran Rajput")
    st.markdown("---")

    # API Key
    st.markdown("### 🔑 Groq API Key")
    api_key = st.text_input(
        "Enter your Groq API key",
        type="password",
        placeholder="gsk_...",
        help="Get a free key at console.groq.com — no credit card needed",
    )

    if api_key and not st.session_state.api_key_valid:
        with st.spinner("Verifying key..."):
            is_valid, error_msg = validate_api_key(api_key)
        if is_valid:
            st.session_state.chain = build_chain(api_key)
            st.session_state.api_key_valid = True
            st.success("✅ API key verified!")
        else:
            st.error(f"❌ {error_msg}")
    elif st.session_state.api_key_valid:
        st.markdown(
            '<span class="badge badge-green">✓ API CONNECTED</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Settings
    st.markdown("### ⚙️ Review Settings")
    language = st.selectbox(
        "Programming Language", LANGUAGES, index=LANGUAGES.index("Python")
    )
    st.session_state.last_language = language

    review_mode = st.selectbox("Review Mode", list(REVIEW_MODES.keys()))

    st.markdown("---")

    # Example loader
    st.markdown("### 💡 Load Example Code")
    example_choice = st.selectbox(
        "Pick an example", ["— Select —"] + list(EXAMPLE_SNIPPETS.keys())
    )

    st.markdown("---")

    # Stats
    st.markdown("### 📊 Session Stats")
    st.markdown(
        f"""
    <div class="stat-row">
        <div class="stat-box"><div class="n">{st.session_state.review_count}</div><div class="l">REVIEWS</div></div>
        <div class="stat-box"><div class="n">{len(st.session_state.messages)}</div><div class="l">MESSAGES</div></div>
    </div>""",
        unsafe_allow_html=True,
    )

    if st.button("🗑 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.review_count = 0
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px;color:#6e6c90'>"
        "Stack: Python · LangChain · Groq API<br>"
        "LangChain Memory · Streamlit · Markdown"
        "</div>",
        unsafe_allow_html=True,
    )


# ── Main header ───────────────────────────────────────────────────────────────
col_head, col_badges = st.columns([3, 1])
with col_head:
    st.markdown("# 🔍 AI Code Review Assistant")
    st.markdown(
        "Paste your code → get a **senior engineer's review** in seconds. "
        "Bugs, security issues, best practices, refactoring — all covered."
    )
with col_badges:
    st.markdown(
        """
    <div style='text-align:right;margin-top:16px'>
        <span class="badge badge-purple">LangChain</span>&nbsp;
        <span class="badge badge-green">Groq API</span><br><br>
        <span class="badge badge-gold">Streaming</span>&nbsp;
        <span class="badge badge-red">Memory</span>
    </div>""",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── API key warning ───────────────────────────────────────────────────────────
if not st.session_state.api_key_valid:
    st.markdown(
        """
    <div class="callout">
        🔑 <strong>Enter your Groq API key in the sidebar to start.</strong><br>
        Get a free key at
        <a href="https://console.groq.com/keys" target="_blank" style="color:#b4a9ff">
        console.groq.com/keys</a> — no credit card needed.
    </div>""",
        unsafe_allow_html=True,
    )

# ── Code input ────────────────────────────────────────────────────────────────
st.markdown("### 📝 Paste Your Code")

default_code = ""
if example_choice != "— Select —":
    default_code = EXAMPLE_SNIPPETS[example_choice]

code_input = st.text_area(
    label="Code input",
    value=default_code,
    height=260,
    placeholder="# Paste your code here...\ndef my_function():\n    pass",
    label_visibility="collapsed",
)

col_btn, col_mode_info = st.columns([1, 3])
with col_btn:
    review_btn = st.button(
        "🔍 Review My Code",
        use_container_width=True,
        type="primary",
        disabled=not st.session_state.api_key_valid,
    )
with col_mode_info:
    st.markdown(
        f'<div class="callout callout-gold" style="margin-top:4px">'
        f"⚙️ Mode: <strong>{review_mode}</strong> — {REVIEW_MODES[review_mode]}</div>",
        unsafe_allow_html=True,
    )

# ── Quick follow-up prompts ───────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown("**⚡ Quick follow-up questions:**")
    q_cols = st.columns(3)
    for i, q in enumerate(QUICK_PROMPTS):
        with q_cols[i % 3]:
            if st.button(
                q, key=f"quick_{i}", disabled=not st.session_state.api_key_valid
            ):
                followup_msg = build_followup_message(q, st.session_state.last_language)
                st.session_state.messages.append(
                    {"role": "user", "content": followup_msg}
                )
                with st.chat_message("user"):
                    st.markdown(f"**{q}**")
                with st.chat_message("assistant"):
                    response = ""
                    placeholder = st.empty()
                    for chunk in stream_response(
                        st.session_state.chain,
                        followup_msg,
                        st.session_state.messages[:-1],
                    ):
                        response += chunk
                        placeholder.markdown(response + "▌")
                    placeholder.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.rerun()

st.markdown("---")

# ── Handle review button ──────────────────────────────────────────────────────
if review_btn:
    if not code_input.strip():
        st.warning("⚠️ Please paste some code first!")
    elif not st.session_state.api_key_valid:
        st.error("❌ Please enter a valid Groq API key in the sidebar.")
    else:
        user_msg = build_user_message(
            code_input, language, review_mode, REVIEW_MODES[review_mode]
        )
        st.session_state.messages.append({"role": "user", "content": user_msg})
        st.session_state.review_count += 1

# ── Chat history ──────────────────────────────────────────────────────────────
st.markdown("### 💬 Review History")

if not st.session_state.messages:
    st.markdown(
        """
    <div class="callout callout-green" style="text-align:center;padding:32px">
        🚀 <strong>Paste your code above and click "Review My Code" to start!</strong><br>
        <span style='font-size:13px;color:#6e6c90'>
        Supports Python, JavaScript, Java, SQL, Go, Rust and more</span>
    </div>""",
        unsafe_allow_html=True,
    )
else:
    is_new_review = review_btn and code_input.strip() and st.session_state.api_key_valid
    history_msgs = (
        st.session_state.messages[:-1] if is_new_review else st.session_state.messages
    )

    for msg in history_msgs:
        with st.chat_message(msg["role"]):
            if (
                msg["role"] == "user"
                and "Please review the following code" in msg["content"]
            ):
                st.markdown("🔍 **Code submitted for review**")
                with st.expander("View submitted code"):
                    st.markdown(msg["content"])
            else:
                st.markdown(msg["content"])

    if is_new_review:
        last_user_msg = st.session_state.messages[-1]["content"]

        with st.chat_message("user"):
            st.markdown(
                f"🔍 **Code submitted for review** · Language: `{language}` · Mode: `{review_mode}`"
            )
            with st.expander("View submitted code"):
                st.code(code_input, language=language.lower().split("/")[0])

        with st.chat_message("assistant"):
            response = ""
            container = st.empty()
            for chunk in stream_response(
                st.session_state.chain,
                last_user_msg,
                st.session_state.messages[:-1],
            ):
                response += chunk
                container.markdown(response + "▌")
            container.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# ── Follow-up chat input ──────────────────────────────────────────────────────
if st.session_state.messages and st.session_state.api_key_valid:
    st.markdown("---")
    followup = st.chat_input("Ask a follow-up question about your code...")
    if followup:
        st.session_state.messages.append({"role": "user", "content": followup})
        with st.chat_message("user"):
            st.markdown(followup)
        with st.chat_message("assistant"):
            response = ""
            container = st.empty()
            for chunk in stream_response(
                st.session_state.chain,
                followup,
                st.session_state.messages[:-1],
            ):
                response += chunk
                container.markdown(response + "▌")
            container.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#6e6c90;font-size:12px'>"
    "Code Review Assistant · Resume Project #3 · "
    "Akshay Kiran Rajput · LangChain · Groq API · Streamlit"
    "</center>",
    unsafe_allow_html=True,
)
