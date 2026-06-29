"""
llm_engine.py — CodeSense AI Code Review Assistant
LangChain + Groq multi-model chain with conversation memory.
Compatible with: langchain>=0.3.0, langchain-groq>=0.2.0, groq>=0.9.0
Resume Project #3 | Akshay Kiran Rajput
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from groq import Groq
from dotenv import load_dotenv
import os
from config import SYSTEM_PROMPT, TEMPERATURE, MAX_HISTORY, FREE_MODELS, DEFAULT_MODEL

load_dotenv()


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """Live test call to Groq — rejects invalid keys instantly."""
    try:
        client = Groq(api_key=api_key)
        model_id = FREE_MODELS[DEFAULT_MODEL]["id"]
        client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=1,
        )
        return True, ""
    except Exception as e:
        err = str(e)
        if (
            "401" in err
            or "invalid_api_key" in err.lower()
            or "authentication" in err.lower()
        ):
            return False, "Invalid API key — get yours at console.groq.com/keys"
        elif "429" in err or "rate_limit" in err.lower():
            return True, ""  # valid key, just rate limited
        else:
            return False, f"Connection error: {err}"


def build_chain(api_key: str, model_key: str = DEFAULT_MODEL):
    """Build LangChain LCEL chain for the selected free Groq model."""
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError(
            "No API key. Add GROQ_API_KEY to .env or enter in the sidebar."
        )

    model_id = FREE_MODELS[model_key]["id"]

    llm = ChatGroq(
        model=model_id,
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
    """Format code + metadata into the review prompt."""
    lang_str = f" ({language})" if language != "Auto-detect" else ""
    lang_tag = language.lower().split("/")[0] if language != "Auto-detect" else ""
    clean_mode = mode.lstrip("🔍🐛🔒⚡🧪📖✨🎓 ")
    return (
        f"Please review the following code{lang_str}.\n"
        f"Review mode: **{clean_mode}** — {mode_desc}\n\n"
        f"```{lang_tag}\n{code.strip()}\n```"
    )


def build_followup_message(question: str, language: str) -> str:
    return question


def get_lc_history(st_history: list) -> list:
    """Convert Streamlit session history → LangChain message objects."""
    msgs = []
    for m in st_history[-MAX_HISTORY:]:
        if m["role"] == "user":
            msgs.append(HumanMessage(content=m["content"]))
        else:
            msgs.append(AIMessage(content=m["content"]))
    return msgs


def stream_response(chain, user_input: str, history: list):
    """Yield streamed tokens; handle Groq errors gracefully."""
    lc_history = get_lc_history(history)
    try:
        for chunk in chain.stream({"input": user_input, "history": lc_history}):
            yield chunk
    except Exception as e:
        err = str(e)
        if "rate_limit" in err.lower() or "429" in err:
            yield (
                "\n\n> ⚠️ **Rate limit hit.** Groq free tier allows 30 req/min. "
                "Please wait ~60 seconds and try again. "
                "To avoid this, switch to **GPT-OSS 20B** using the 'Switch model' "
                "button in the sidebar — it has higher throughput on the free tier."
            )
        elif "401" in err or "invalid_api_key" in err.lower():
            yield (
                "\n\n> ❌ **Invalid API Key.** Check your key at "
                "[console.groq.com/keys](https://console.groq.com/keys)."
            )
        else:
            yield f"\n\n> ❌ **Error:** {err}"
