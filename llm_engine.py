"""
llm_engine.py — Code Review Assistant
LangChain + Groq chain with conversation memory.
Compatible with:
  langchain>=0.3.0
  langchain-groq>=0.2.0
  groq>=0.9.0
"""

from langchain_groq import ChatGroq  # type: ignore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from groq import Groq  # type: ignore
from dotenv import load_dotenv
import os
from config import SYSTEM_PROMPT, MODEL_NAME, TEMPERATURE, MAX_HISTORY

load_dotenv()


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """Make a real test call to Groq to verify the key is valid.
    Returns (is_valid, error_message).
    """
    try:
        client = Groq(api_key=api_key)
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=1,
        )
        return True, ""
    except Exception as e:
        err = str(e)
        if "401" in err or "invalid_api_key" in err.lower() or "authentication" in err.lower():
            return False, "Invalid API key. Get yours at console.groq.com/keys"
        elif "429" in err or "rate_limit" in err.lower():
            # Key is valid but rate limited — still accept it
            return True, ""
        else:
            return False, f"Connection error: {err}"


def build_chain(api_key: str = None):  # type: ignore
    """Build LangChain chain with Groq model.
    Uses api_key if provided (from sidebar), otherwise falls back to .env file.
    """
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError(
            "No API key found. Add GROQ_API_KEY=your_key to your .env file."
        )

    llm = ChatGroq(
        model=MODEL_NAME,
        groq_api_key=key,
        temperature=TEMPERATURE,
        streaming=True,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    return prompt | llm | StrOutputParser()


def build_user_message(code: str, language: str, mode: str, mode_desc: str) -> str:
    """Format the user's code + context into a prompt."""
    lang_str = f" ({language})" if language != "Auto-detect" else ""
    lang_tag = language.lower().split("/")[0] if language != "Auto-detect" else ""
    return (
        f"Please review the following code{lang_str}.\n"
        f"Review mode: **{mode}** — {mode_desc}\n\n"
        f"```{lang_tag}\n"
        f"{code.strip()}\n"
        f"```"
    )


def build_followup_message(question: str, language: str) -> str:
    """Format a follow-up question message."""
    return question


def get_lc_history(st_history: list) -> list:
    """Convert Streamlit session history to LangChain message objects."""
    messages = []
    for msg in st_history[-MAX_HISTORY:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    return messages


def stream_response(chain, user_input: str, history: list):
    """Yield streamed tokens from the chain."""
    lc_history = get_lc_history(history)
    try:
        for chunk in chain.stream(
            {
                "input": user_input,
                "history": lc_history,
            }
        ):
            yield chunk
    except Exception as e:
        err = str(e)
        if "rate_limit" in err.lower() or "429" in err:
            yield (
                "\n\n> ⚠️ **Rate limit hit.** You've sent too many requests. "
                "Wait 60 seconds and try again. Groq free tier allows 30 req/min."
            )
        elif "401" in err or "invalid_api_key" in err.lower():
            yield (
                "\n\n> ❌ **Invalid API Key.** Check your Groq key at "
                "[console.groq.com](https://console.groq.com/keys)."
            )
        else:
            yield f"\n\n> ❌ **Error:** {err}"
