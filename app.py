"""
app.py — CodeSense AI Code Review Assistant
Multi-model free stack: 6 free Groq LLMs, select before chat
Resume Project #3 | Akshay Kiran Rajput
Run: streamlit run app.py
"""

import streamlit as st
import os
from llm_engine import (
    build_chain, validate_api_key,
    build_user_message, build_followup_message, stream_response,
)
from config import (
    LANGUAGES, REVIEW_MODES, QUICK_PROMPTS,
    EXAMPLE_SNIPPETS, FREE_MODELS, DEFAULT_MODEL,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodeSense — AI Code Review",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Provider accent colors ────────────────────────────────────────────────────
PROVIDER_COLOR = {
    "OpenAI OSS": "#06D6A0",   # mint — GPT-OSS models
    "Alibaba":    "#C77DFF",   # violet — Qwen
}

def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _chip(text, bg="#131929", color="#7A7E99", border="#1C2235"):
    return (
        f'<span style="display:inline-block;font-family:monospace;font-size:10px;'
        f'padding:3px 9px;border-radius:4px;background:{bg};color:{color};'
        f'border:1px solid {border};margin:2px 3px 2px 0">{text}</span>'
    )

def _model_card(key, info, is_active):
    pc = PROVIDER_COLOR.get(info["provider"], "#FF5E5B")
    r, g, b = _hex_rgb(pc)
    bg     = f"rgba({r},{g},{b},.07)" if is_active else "#0D1120"
    border = pc if is_active else "#1C2235"
    clean  = key.lstrip("⚡🧠🔭🔬💎🌐 ").split("—")[0].strip()
    badge  = (
        f'<div style="position:absolute;top:11px;right:11px;background:{pc};'
        f'color:#0B0F1A;font-family:monospace;font-size:9px;font-weight:700;'
        f'padding:2px 8px;border-radius:3px">SELECTED</div>'
    ) if is_active else ""
    chips = "".join(_chip(c) for c in [info["speed"], info["ctx"]+" ctx", info["limit"]])
    return (
        f'<div style="position:relative;background:{bg};border:1px solid {border};'
        f'border-left:3px solid {pc};border-radius:12px;padding:15px 15px 13px;'
        f'margin-bottom:3px;min-height:138px">'
        f'{badge}'
        f'<div style="font-family:monospace;font-size:9px;font-weight:600;'
        f'letter-spacing:.12em;text-transform:uppercase;color:{pc};margin-bottom:5px">'
        f'{info["provider"]}</div>'
        f'<div style="font-size:15px;font-weight:700;color:#F0EDFF;margin-bottom:9px;'
        f'line-height:1.25">{clean}</div>'
        f'<div style="margin-bottom:7px">{chips}</div>'
        f'<div style="font-size:11px;color:#5A6080;line-height:1.5">{info["best_for"]}</div>'
        f'</div>'
    )

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*,*::before,*::after{box-sizing:border-box}

[data-testid="stAppViewContainer"]{background:#0B0F1A !important;font-family:'Inter',sans-serif;color:#C9C4E8}
[data-testid="stSidebar"]{background:#0D1120 !important;border-right:1px solid #1C2235 !important}
[data-testid="stSidebar"] > div:first-child{padding-top:1.2rem}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:1.6rem !important;padding-bottom:4rem !important;max-width:1140px}

h1,h2,h3,h4{font-family:'Space Grotesk',sans-serif !important;color:#F0EDFF !important;letter-spacing:-.02em}

/* Code blocks */
code{font-family:'JetBrains Mono',monospace !important;font-size:13px;color:#e8e3ff}
pre{background:#0D1120 !important;border:1px solid #1C2235 !important;border-radius:8px !important;padding:14px !important}

/* Inputs */
.stTextInput > label,.stTextArea > label,.stSelectbox > label{color:#5A6080 !important;font-size:12px !important}
.stTextInput > div > div > input,.stTextArea textarea{
    background:#131929 !important;border:1px solid #1C2235 !important;
    color:#F0EDFF !important;border-radius:8px !important;font-family:'JetBrains Mono',monospace !important}
.stTextInput > div > div > input:focus,.stTextArea textarea:focus{
    border-color:#FF5E5B !important;box-shadow:0 0 0 2px rgba(255,94,91,.15) !important}
.stTextArea textarea{font-size:13px !important;line-height:1.6 !important}

/* Buttons */
.stButton > button{
    font-family:'Space Grotesk',sans-serif !important;font-weight:600 !important;
    border-radius:8px !important;transition:all .15s !important;font-size:13px !important}
.stButton > button[kind="primary"]{background:#FF5E5B !important;border:none !important;color:#fff !important}
.stButton > button[kind="primary"]:hover{background:#ff3f3c !important;transform:translateY(-1px);box-shadow:0 4px 18px rgba(255,94,91,.4) !important}
.stButton > button:not([kind="primary"]){background:#131929 !important;border:1px solid #1C2235 !important;color:#C9C4E8 !important}
.stButton > button:not([kind="primary"]):hover{border-color:#FF5E5B !important;color:#F0EDFF !important}

/* Selectbox */
.stSelectbox > div > div{background:#131929 !important;border:1px solid #1C2235 !important;border-radius:8px !important;color:#F0EDFF !important}

/* Chat messages */
[data-testid="stChatMessage"]{background:#0D1120 !important;border:1px solid #1C2235 !important;border-radius:12px !important;margin-bottom:10px !important}

/* Expander */
div[data-testid="stExpander"]{background:#131929 !important;border:1px solid #1C2235 !important;border-radius:8px !important}
div[data-testid="stExpander"] summary{color:#7A7E99 !important;font-size:13px !important}

/* Chat input */
.stChatInput > div{background:#0D1120 !important;border:1px solid #1C2235 !important;border-radius:12px !important}

/* Progress */
.stProgress > div > div > div{background:linear-gradient(90deg,#FF5E5B,#FFD166) !important}

/* File uploader */
[data-testid="stFileUploader"]{background:#131929 !important;border:1px dashed #2A3050 !important;border-radius:10px !important}

hr{border-color:#1C2235 !important;margin:18px 0 !important}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
_defaults = {
    "messages":       [],
    "review_count":   0,
    "chain":          None,
    "api_key_valid":  False,
    "last_language":  "Python",
    "selected_model": DEFAULT_MODEL,
    "chat_started":   False,
    "file_reviews":   0,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Brand
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">'
        '<div style="width:34px;height:34px;background:linear-gradient(135deg,#FF5E5B,#FFD166);'
        'border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:17px">🔍</div>'
        '<div><div style="font-family:\'Space Grotesk\',sans-serif;font-size:18px;font-weight:700;'
        'color:#F0EDFF;line-height:1.1">CodeSense</div>'
        '<div style="font-size:11px;color:#5A6080;font-family:monospace">AI Code Review</div></div></div>'
        '<div style="display:inline-flex;align-items:center;gap:5px;background:rgba(6,214,160,.12);'
        'border:1px solid rgba(6,214,160,.3);border-radius:20px;padding:3px 12px;font-size:11px;'
        'font-weight:600;color:#06D6A0;font-family:monospace;margin:8px 0 16px">'
        '⚡ 100% FREE · NO CREDIT CARD</div>',
        unsafe_allow_html=True,
    )

    # API Key
    st.markdown(
        '<div style="font-family:monospace;font-size:10px;font-weight:500;letter-spacing:.12em;'
        'color:#3D4460;text-transform:uppercase;margin:0 0 6px">Groq API Key</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:11px;color:#3D4460;margin-bottom:8px">Free at '
        '<a href="https://console.groq.com/keys" target="_blank" style="color:#FFD166;'
        'text-decoration:none">console.groq.com/keys</a> — no card needed</div>',
        unsafe_allow_html=True,
    )
    api_key = st.text_input("API Key", type="password", placeholder="gsk_...", label_visibility="collapsed")

    if api_key and not st.session_state.api_key_valid:
        with st.spinner("Verifying key…"):
            ok, err = validate_api_key(api_key)
        if ok:
            st.session_state.api_key_valid = True
            st.session_state.chain = build_chain(api_key, st.session_state.selected_model)
            os.environ["GROQ_API_KEY"] = api_key
            st.rerun()
        else:
            st.markdown(
                f'<div style="background:rgba(255,94,91,.1);border:1px solid rgba(255,94,91,.3);'
                f'border-radius:6px;padding:8px 12px;font-size:12px;color:#ff8fa3;margin-top:6px">'
                f'❌ {err}</div>',
                unsafe_allow_html=True,
            )

    if st.session_state.api_key_valid:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:6px;font-size:12px;color:#06D6A0;'
            'font-family:monospace;margin-top:6px"><div style="width:7px;height:7px;background:#06D6A0;'
            'border-radius:50%;box-shadow:0 0 6px #06D6A0"></div>Connected to Groq</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr>', unsafe_allow_html=True)

    # Review settings (visible after key)
    if st.session_state.api_key_valid:
        st.markdown(
            '<div style="font-family:monospace;font-size:10px;font-weight:500;letter-spacing:.12em;'
            'color:#3D4460;text-transform:uppercase;margin-bottom:8px">Settings</div>',
            unsafe_allow_html=True,
        )
        language = st.selectbox("Language", LANGUAGES, index=LANGUAGES.index("Python"), label_visibility="collapsed")
        st.session_state.last_language = language

        review_mode = st.selectbox("Review Mode", list(REVIEW_MODES.keys()), label_visibility="collapsed")

        st.markdown('<hr>', unsafe_allow_html=True)

        # Examples
        st.markdown(
            '<div style="font-family:monospace;font-size:10px;font-weight:500;letter-spacing:.12em;'
            'color:#3D4460;text-transform:uppercase;margin-bottom:8px">Load Example</div>',
            unsafe_allow_html=True,
        )
        example_choice = st.selectbox(
            "Example", ["— pick one —"] + list(EXAMPLE_SNIPPETS.keys()), label_visibility="collapsed"
        )

        st.markdown('<hr>', unsafe_allow_html=True)

    # Stats
    st.markdown(
        '<div style="font-family:monospace;font-size:10px;font-weight:500;letter-spacing:.12em;'
        'color:#3D4460;text-transform:uppercase;margin-bottom:8px">Session</div>',
        unsafe_allow_html=True,
    )
    n_reviews = st.session_state.review_count
    n_msgs    = len(st.session_state.messages)
    model_short = st.session_state.selected_model.split("—")[0].strip().lstrip("⚡🧠🔭🔬💎🌐 ").strip()
    st.markdown(
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px">'
        f'<div style="background:#131929;border:1px solid #1C2235;border-radius:8px;padding:10px 8px;text-align:center">'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:20px;font-weight:700;color:#F0EDFF">{n_reviews}</div>'
        f'<div style="font-family:monospace;font-size:9px;color:#3D4460;letter-spacing:.08em">REVIEWS</div></div>'
        f'<div style="background:#131929;border:1px solid #1C2235;border-radius:8px;padding:10px 8px;text-align:center">'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:20px;font-weight:700;color:#F0EDFF">{n_msgs}</div>'
        f'<div style="font-family:monospace;font-size:9px;color:#3D4460;letter-spacing:.08em">MESSAGES</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.messages:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages     = []
            st.session_state.review_count = 0
            st.session_state.chat_started = False
            st.rerun()
        if st.session_state.chat_started:
            if st.button("Switch model", use_container_width=True, help="Clears chat, keeps key"):
                st.session_state.messages     = []
                st.session_state.review_count = 0
                st.session_state.chat_started = False
                st.session_state.chain        = None
                st.rerun()

    st.markdown(
        '<div style="margin-top:16px;font-family:monospace;font-size:10px;color:#2A3050;line-height:1.8">'
        'LangChain · Groq LPU · Streamlit<br>6 free models · streaming · memory</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════
# MAIN — HERO
# ═══════════════════════════════════════════════════════
st.markdown(
    '<div style="background:#0D1120;border:1px solid #1C2235;border-radius:16px;'
    'padding:26px 30px 20px;margin-bottom:22px">'
    '<div style="font-family:monospace;font-size:11px;color:#FF5E5B;letter-spacing:.1em;'
    'text-transform:uppercase;margin-bottom:5px">Resume Project #3 · Akshay Kiran Rajput</div>'
    '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:30px;font-weight:700;'
    'color:#F0EDFF;line-height:1.15;letter-spacing:-.03em;margin-bottom:7px">'
    'Get a <span style="color:#FF5E5B">senior engineer\'s review</span> in seconds.</div>'
    '<div style="font-size:14px;color:#7A7E99;line-height:1.6;max-width:580px;margin-bottom:13px">'
    'Paste any code snippet, pick your free AI model, and get back a full review — '
    'bugs, security issues, refactored code, complexity analysis, and unit tests. '
    'Multi-turn memory keeps context across follow-up questions.</div>'
    '<div style="display:flex;flex-wrap:wrap;gap:6px">'
    + "".join(
        f'<span style="font-family:monospace;font-size:10px;padding:4px 10px;border-radius:4px;'
        f'color:{c};border:1px solid {c}33;background:{c}11">{t}</span>'
        for t, c in [
            ("LangChain", "#FF5E5B"), ("Groq Free Tier", "#FFD166"),
            ("6 Free Models", "#06D6A0"), ("Streaming", "#C77DFF"),
            ("Conversation Memory", "#FF5E5B"), ("8 Review Modes", "#FFD166"),
        ]
    )
    + '</div></div>',
    unsafe_allow_html=True,
)

# Pipeline strip
_steps = [("📋","Paste Code"),("🤖","Pick Model"),("🔍","Get Review"),("💬","Follow-up"),("✅","Ship Better Code")]
_pipe  = ""
for i, (ic, lb) in enumerate(_steps):
    _pipe += (
        f'<div style="display:flex;align-items:center;gap:5px;font-size:12px;'
        f'color:#7A7E99;padding:4px 10px"><span>{ic}</span><span>{lb}</span></div>'
    )
    if i < len(_steps)-1:
        _pipe += '<span style="color:#2A3050;font-size:16px;margin:0 2px">›</span>'

st.markdown(
    f'<div style="display:flex;align-items:center;flex-wrap:wrap;background:#131929;'
    f'border:1px solid #1C2235;border-radius:10px;padding:10px 16px;margin-bottom:22px">'
    f'{_pipe}</div>',
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════
# NO KEY NOTICE
# ═══════════════════════════════════════════════════════
if not st.session_state.api_key_valid:
    st.markdown(
        '<div style="background:rgba(255,209,102,.06);border:1px solid rgba(255,209,102,.2);'
        'border-left:3px solid #FFD166;border-radius:8px;padding:13px 16px;font-size:13px;'
        'color:#C9C4E8;margin-bottom:20px">'
        '🔑 <strong>Paste your free Groq API key in the sidebar.</strong> '
        'Get one at <a href="https://console.groq.com/keys" target="_blank" '
        'style="color:#FFD166">console.groq.com/keys</a> — just an email, no card needed.</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════
# MODEL SELECTOR (Step 1 — before chat starts)
# ═══════════════════════════════════════════════════════
if st.session_state.api_key_valid and not st.session_state.chat_started:

    st.markdown(
        '<div style="display:flex;align-items:center;gap:12px;margin-bottom:18px">'
        '<div style="width:30px;height:30px;background:linear-gradient(135deg,#FF5E5B,#FFD166);'
        'border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;'
        'font-size:13px;color:#0B0F1A;flex-shrink:0">1</div>'
        '<div><div style="font-family:\'Space Grotesk\',sans-serif;font-size:19px;font-weight:700;'
        'color:#F0EDFF">Choose your AI model</div>'
        '<div style="font-size:13px;color:#5A6080;margin-top:1px">'
        'All six run on Groq\'s free tier — no payment required</div></div></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for idx, (key, info) in enumerate(FREE_MODELS.items()):
        is_active = (key == st.session_state.selected_model)
        with cols[idx % 2]:
            st.markdown(_model_card(key, info, is_active), unsafe_allow_html=True)
            lbl = "✓ Selected" if is_active else "Select"
            btype = "primary" if is_active else "secondary"
            if st.button(lbl, key=f"m_{idx}", use_container_width=True, type=btype):
                st.session_state.selected_model = key
                if st.session_state.api_key_valid and api_key:
                    st.session_state.chain = build_chain(api_key, key)
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

elif st.session_state.api_key_valid and st.session_state.chat_started:
    # Compact active model banner
    info   = FREE_MODELS[st.session_state.selected_model]
    pc     = PROVIDER_COLOR.get(info["provider"], "#FF5E5B")
    r,g,b  = _hex_rgb(pc)
    short  = st.session_state.selected_model.split("—")[0].strip().lstrip("⚡🧠🔭🔬💎🌐 ").strip()
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;background:#0D1120;'
        f'border:1px solid #1C2235;border-radius:10px;padding:11px 16px;margin-bottom:18px">'
        f'<div style="width:8px;height:8px;border-radius:50%;background:{pc};'
        f'box-shadow:0 0 7px rgba({r},{g},{b},.7);flex-shrink:0"></div>'
        f'<div><div style="font-family:monospace;font-size:9px;color:#3D4460;'
        f'letter-spacing:.1em;text-transform:uppercase">Active Model</div>'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:14px;font-weight:700;'
        f'color:#F0EDFF">{short}</div></div>'
        f'<div style="margin-left:auto;font-family:monospace;font-size:10px;color:#5A6080">'
        f'{info["provider"]} · {info["speed"]} · {info["ctx"]} ctx</div></div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════
# CODE INPUT (Step 2)
# ═══════════════════════════════════════════════════════
if st.session_state.api_key_valid:

    if not st.session_state.chat_started:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">'
            '<div style="width:30px;height:30px;background:linear-gradient(135deg,#FF5E5B,#FFD166);'
            'border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;'
            'font-size:13px;color:#0B0F1A;flex-shrink:0">2</div>'
            '<div><div style="font-family:\'Space Grotesk\',sans-serif;font-size:19px;font-weight:700;'
            'color:#F0EDFF">Paste your code</div>'
            '<div style="font-size:13px;color:#5A6080;margin-top:1px">'
            'Or pick an example from the sidebar. Then click Review →</div></div></div>',
            unsafe_allow_html=True,
        )

    # example loader
    default_code = ""
    try:
        if example_choice != "— pick one —":
            default_code = EXAMPLE_SNIPPETS[example_choice]
    except NameError:
        pass

    code_input = st.text_area(
        "Code input",
        value=default_code,
        height=240,
        placeholder="# Paste your code here…\ndef my_function():\n    pass",
        label_visibility="collapsed",
    )

    # File upload (new feature)
    uploaded = st.file_uploader(
        "Or upload a file (.py .js .ts .java .go .rs .sql .sh)",
        type=["py","js","ts","java","go","rs","sql","sh","txt","cpp","c","php","rb","swift","kt"],
        label_visibility="visible",
    )
    if uploaded:
        code_input = uploaded.read().decode("utf-8", errors="ignore")
        st.session_state.file_reviews += 1
        st.markdown(
            f'<div style="font-size:12px;color:#06D6A0;font-family:monospace;margin:-8px 0 10px">'
            f'✓ Loaded: {uploaded.name} ({len(code_input)} chars)</div>',
            unsafe_allow_html=True,
        )

    # Review controls
    try:
        sel_mode = review_mode
    except NameError:
        sel_mode = list(REVIEW_MODES.keys())[0]
    try:
        sel_lang = language
    except NameError:
        sel_lang = "Python"

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        review_btn = st.button(
            "Review My Code →",
            use_container_width=True,
            type="primary",
            disabled=not st.session_state.api_key_valid,
        )
    with col_info:
        clean_mode = sel_mode.lstrip("🔍🐛🔒⚡🧪📖✨🎓 ")
        st.markdown(
            f'<div style="background:rgba(255,209,102,.06);border:1px solid rgba(255,209,102,.18);'
            f'border-left:3px solid #FFD166;border-radius:7px;padding:9px 14px;margin-top:3px;'
            f'font-size:13px;color:#C9C4E8">'
            f'⚙️ <strong style="color:#FFD166">{clean_mode}</strong> · '
            f'<span style="color:#7A7E99">{REVIEW_MODES[sel_mode]}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Handle review button
    if review_btn:
        if not code_input.strip():
            st.warning("Paste some code first, or upload a file.")
        else:
            user_msg = build_user_message(code_input, sel_lang, sel_mode, REVIEW_MODES[sel_mode])
            st.session_state.messages.append({"role": "user", "content": user_msg,
                                               "lang": sel_lang, "mode": sel_mode,
                                               "snippet": code_input})
            st.session_state.review_count += 1
            st.session_state.chat_started  = True
            if not st.session_state.chain:
                st.session_state.chain = build_chain(api_key or os.getenv("GROQ_API_KEY"),
                                                     st.session_state.selected_model)


# ═══════════════════════════════════════════════════════
# QUICK PROMPTS
# ═══════════════════════════════════════════════════════
if st.session_state.messages and st.session_state.chat_started:
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:13px;font-weight:600;'
        'color:#F0EDFF;margin-bottom:8px">⚡ Quick follow-ups</div>',
        unsafe_allow_html=True,
    )
    qc = st.columns(4)
    for i, q in enumerate(QUICK_PROMPTS):
        with qc[i % 4]:
            if st.button(q[:30] + ("…" if len(q)>30 else ""), key=f"qp_{i}", use_container_width=True):
                st.session_state._pending_q = q

    st.markdown("<hr>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# CHAT HISTORY
# ═══════════════════════════════════════════════════════
if not st.session_state.chat_started:
    # Empty state
    st.markdown(
        '<div style="background:#0D1120;border:1px dashed #2A3050;border-radius:12px;'
        'padding:40px 24px;text-align:center;margin-top:8px">'
        '<div style="font-size:36px;margin-bottom:12px">👨‍💻</div>'
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:18px;font-weight:600;'
        'color:#F0EDFF;margin-bottom:5px">Ready when you are</div>'
        '<div style="font-size:13px;color:#5A6080;max-width:400px;margin:0 auto">'
        'Select a model above, paste your code, and hit <strong style="color:#F0EDFF">'
        'Review My Code →</strong> to get a senior engineer\'s take in seconds.</div></div>',
        unsafe_allow_html=True,
    )
else:
    is_new = (
        review_btn
        and "review_btn" in dir()
        and st.session_state.messages
        and code_input.strip() if "code_input" in dir() else False
    )

    # Determine which messages to show
    history_to_show = st.session_state.messages[:-1] if is_new else st.session_state.messages

    for msg in history_to_show:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user" and msg.get("snippet"):
                lang_disp = msg.get("lang","")
                mode_disp = msg.get("mode","").lstrip("🔍🐛🔒⚡🧪📖✨🎓 ")
                st.markdown(
                    f'<div style="font-size:13px;color:#C9C4E8;margin-bottom:6px">'
                    f'🔍 <strong>Code review submitted</strong> &nbsp;'
                    f'<span style="font-family:monospace;font-size:11px;background:#131929;'
                    f'border:1px solid #1C2235;border-radius:4px;padding:2px 8px">{lang_disp}</span> &nbsp;'
                    f'<span style="font-family:monospace;font-size:11px;background:#131929;'
                    f'border:1px solid #1C2235;border-radius:4px;padding:2px 8px">{mode_disp}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                with st.expander("View submitted code"):
                    st.code(msg["snippet"], language=lang_disp.lower().split("/")[0])
            elif msg["role"] == "user":
                st.markdown(f'**{msg["content"]}**')
            else:
                st.markdown(msg["content"])
                if msg.get("model"):
                    st.markdown(
                        f'<div style="font-family:monospace;font-size:10px;color:#3D4460;'
                        f'margin-top:8px;padding-top:8px;border-top:1px solid #1C2235">'
                        f'via {msg["model"]}</div>',
                        unsafe_allow_html=True,
                    )

    # Stream new review
    if is_new and st.session_state.messages:
        last_msg = st.session_state.messages[-1]

        with st.chat_message("user"):
            lang_disp = last_msg.get("lang","")
            mode_disp = last_msg.get("mode","").lstrip("🔍🐛🔒⚡🧪📖✨🎓 ")
            st.markdown(
                f'<div style="font-size:13px;color:#C9C4E8;margin-bottom:6px">'
                f'🔍 <strong>Code review submitted</strong> &nbsp;'
                f'<span style="font-family:monospace;font-size:11px;background:#131929;'
                f'border:1px solid #1C2235;border-radius:4px;padding:2px 8px">{lang_disp}</span> &nbsp;'
                f'<span style="font-family:monospace;font-size:11px;background:#131929;'
                f'border:1px solid #1C2235;border-radius:4px;padding:2px 8px">{mode_disp}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            with st.expander("View submitted code"):
                st.code(last_msg.get("snippet",""), language=lang_disp.lower().split("/")[0])

        with st.chat_message("assistant"):
            response  = ""
            container = st.empty()
            for chunk in stream_response(st.session_state.chain, last_msg["content"],
                                         st.session_state.messages[:-1]):
                response += chunk
                container.markdown(response + "▌")
            container.markdown(response)
            model_id = FREE_MODELS[st.session_state.selected_model]["id"]
            st.markdown(
                f'<div style="font-family:monospace;font-size:10px;color:#3D4460;'
                f'margin-top:8px;padding-top:8px;border-top:1px solid #1C2235">'
                f'via {model_id}</div>',
                unsafe_allow_html=True,
            )

        st.session_state.messages.append({
            "role": "assistant", "content": response,
            "model": FREE_MODELS[st.session_state.selected_model]["id"],
        })

    # Handle pending quick prompts
    pending_q = getattr(st.session_state, "_pending_q", None)
    if pending_q:
        st.session_state._pending_q = None
        fmsg = build_followup_message(pending_q, st.session_state.last_language)
        st.session_state.messages.append({"role": "user", "content": fmsg})
        with st.chat_message("user"):
            st.markdown(f"**{pending_q}**")
        with st.chat_message("assistant"):
            response  = ""
            container = st.empty()
            for chunk in stream_response(st.session_state.chain, fmsg,
                                         st.session_state.messages[:-1]):
                response += chunk
                container.markdown(response + "▌")
            container.markdown(response)
        st.session_state.messages.append({
            "role": "assistant", "content": response,
            "model": FREE_MODELS[st.session_state.selected_model]["id"],
        })
        st.rerun()


# ═══════════════════════════════════════════════════════
# FREE-TEXT FOLLOW-UP
# ═══════════════════════════════════════════════════════
if st.session_state.chat_started and st.session_state.chain:
    st.markdown("<hr>", unsafe_allow_html=True)
    followup = st.chat_input("Ask anything about your code…")
    if followup:
        st.session_state.messages.append({"role": "user", "content": followup})
        with st.chat_message("user"):
            st.markdown(followup)
        with st.chat_message("assistant"):
            response  = ""
            container = st.empty()
            for chunk in stream_response(st.session_state.chain, followup,
                                         st.session_state.messages[:-1]):
                response += chunk
                container.markdown(response + "▌")
            container.markdown(response)
        st.session_state.messages.append({
            "role": "assistant", "content": response,
            "model": FREE_MODELS[st.session_state.selected_model]["id"],
        })
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;font-family:monospace;font-size:10px;color:#2A3050;'
    'padding:16px 0 4px;letter-spacing:.05em">'
    'CODESENSE · RESUME PROJECT #3 ⭐ · AKSHAY KIRAN RAJPUT · '
    'LANGCHAIN · GROQ · 6 FREE MODELS · STREAMLIT</div>',
    unsafe_allow_html=True,
)
