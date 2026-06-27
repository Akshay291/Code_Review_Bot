"""
config.py — Code Review Assistant
Central config: system prompt, supported languages, model settings.
"""

SYSTEM_PROMPT = """You are an expert Senior Software Engineer and Code Reviewer with 10+ years of experience across multiple languages and frameworks. Your job is to review code submitted by developers and provide clear, actionable, professional feedback.

When reviewing code, always structure your response as follows:

## 🔍 Code Review Summary
Brief 1-2 sentence overview of what the code does and its overall quality.

## ✅ What's Good
List the strengths — good practices, clean patterns, correct logic. Be specific.

## 🐛 Bugs & Issues
List any bugs, logical errors, or incorrect behaviour found. Include line references where possible.

## ⚠️ Improvements & Best Practices
List improvements: performance, readability, naming conventions, error handling, edge cases, security issues.

## 🔒 Security Concerns
Highlight any security vulnerabilities (SQL injection, unvalidated input, exposed secrets, etc.). Write "None found" if clean.

## ✨ Refactored Code
Provide a clean, improved version of the code with comments explaining key changes.

## 📚 Learning Resources
Suggest 2-3 specific concepts the developer should study based on their code.

---
Rules:
- Be constructive and encouraging, never condescending
- Give concrete examples and code snippets in your suggestions
- Adjust depth based on code complexity
- If code is already excellent, say so clearly
- Always respond in Markdown format
- If the user asks a follow-up question about the review, answer it directly without repeating the full review
"""

# ── Groq model — free tier, fast, works in India ─────────────────────────────
# Options (all free): "llama-3.3-70b-versatile" | "llama-3.1-8b-instant" | "gemma2-9b-it"
MODEL_NAME = "llama-3.3-70b-versatile"

MAX_HISTORY = 20       # max messages to keep in memory
TEMPERATURE = 0.3      # lower = more precise/technical

LANGUAGES = [
    "Python",
    "JavaScript",
    "TypeScript",
    "Java",
    "C++",
    "C",
    "Go",
    "Rust",
    "SQL",
    "HTML/CSS",
    "React/JSX",
    "Bash/Shell",
    "PHP",
    "Swift",
    "Kotlin",
    "Auto-detect",
]

REVIEW_MODES = {
    "Full Review": "Do a complete review covering bugs, best practices, security, and refactoring.",
    "Bug Hunt Only": "Focus ONLY on finding bugs and logical errors. Skip style/best-practice suggestions.",
    "Security Audit": "Focus ONLY on security vulnerabilities, unsafe patterns, and data exposure risks.",
    "Performance Review": "Focus ONLY on performance bottlenecks, algorithmic complexity, and optimization.",
    "Beginner Friendly": "Review for a beginner developer. Be extra encouraging and explain concepts simply.",
}

QUICK_PROMPTS = [
    "What is the time complexity of this code?",
    "How can I make this more Pythonic?",
    "Are there any memory leaks?",
    "Can you add proper error handling?",
    "How do I write unit tests for this?",
    "What design patterns apply here?",
]

EXAMPLE_SNIPPETS = {
    "Python — SQL Injection Bug": """\
import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()
""",
    "JavaScript — Async Issue": """\
function fetchUserData(userId) {
    let userData;
    fetch(`/api/users/${userId}`)
        .then(res => res.json())
        .then(data => {
            userData = data;
        });
    return userData;
}

console.log(fetchUserData(1));
""",
    "Python — Inefficient Loop": """\
def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i != j and lst[i] == lst[j]:
                if lst[i] not in duplicates:
                    duplicates.append(lst[i])
    return duplicates
""",
    "Python — Good Code (for reference)": """\
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    age: int
    bio: Optional[str] = None

    def is_adult(self) -> bool:
        return self.age >= 18

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, email={self.email!r})"
""",
}
