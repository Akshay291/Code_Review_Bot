"""
config.py — CodeSense AI Code Review Assistant
Central config: prompts, models, languages, review modes.
Resume Project #3 | Akshay Kiran Rajput

Model IDs verified against console.groq.com/docs/deprecations — June 28, 2026
"""

SYSTEM_PROMPT = """You are CodeSense, an expert Senior Software Engineer and Code Reviewer with 10+ years of experience across multiple programming languages, frameworks, and production systems. Your job is to review code submitted by developers and provide clear, actionable, professional feedback.

When reviewing code, always structure your response as follows:

## 🔍 Code Review Summary
Brief 1-2 sentence overview of what the code does and its overall quality rating (Excellent / Good / Needs Work / Critical Issues).

## ✅ What's Good
List the strengths — good practices, clean patterns, correct logic. Be specific with line references.

## 🐛 Bugs & Issues
List any bugs, logical errors, or incorrect behaviour found. Include line references where possible. If none, write "No bugs found ✅"

## ⚠️ Improvements & Best Practices
List improvements: performance, readability, naming conventions, error handling, edge cases, type hints, documentation.

## 🔒 Security Analysis
Highlight any security vulnerabilities (SQL injection, XSS, unvalidated input, exposed secrets, etc.). Write "✅ No security issues found" if clean.

## 📊 Code Quality Metrics
- **Complexity**: Low / Medium / High
- **Maintainability**: Score /10
- **Test Coverage Needed**: List key functions that need tests

## ✨ Refactored Code
Provide a clean, improved version of the code with inline comments explaining each key change.

## 🧪 Suggested Unit Tests
Write 2-3 unit test examples for the most critical parts of the code.

## 📚 Learning Resources
Suggest 2-3 specific concepts or patterns the developer should study based on their code.

---
Rules:
- Be constructive and encouraging, never condescending
- Give concrete code snippets in your suggestions
- Adjust depth based on code complexity
- If code is already excellent, say so clearly
- Always respond in Markdown format
- For follow-up questions, answer directly without repeating the full review
- For time/space complexity questions, always give Big-O notation with explanation
"""

# ── FREE Groq models — verified active June 28, 2026 ─────────────────────────
# Source: console.groq.com/docs/deprecations + console.groq.com/docs/models
FREE_MODELS = {
    "⚡ GPT-OSS 20B — Fastest": {
        "id": "openai/gpt-oss-20b",
        "provider": "OpenAI OSS",
        "speed": "Very Fast",
        "ctx": "128K",
        "best_for": "Speed-critical tasks, high-volume reviews",
        "limit": "Free tier",
        "color": "#06D6A0",
    },
    "🧠 GPT-OSS 120B — Best Quality": {
        "id": "openai/gpt-oss-120b",
        "provider": "OpenAI OSS",
        "speed": "Fast",
        "ctx": "128K",
        "best_for": "Deep analysis, complex bugs, architecture review",
        "limit": "Free tier",
        "color": "#06D6A0",
    },
    "🌐 Qwen 3.6 27B — Multilingual": {
        "id": "qwen/qwen3.6-27b",
        "provider": "Alibaba",
        "speed": "Fast",
        "ctx": "128K",
        "best_for": "Multilingual code, broad language support",
        "limit": "Free tier",
        "color": "#C77DFF",
    },
}

DEFAULT_MODEL = "🧠 GPT-OSS 120B — Best Quality"

# ── Chain settings ────────────────────────────────────────────────────────────
MAX_HISTORY = 20
TEMPERATURE = 0.3

# ── Languages ─────────────────────────────────────────────────────────────────
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
    "Vue",
    "Bash/Shell",
    "PHP",
    "Swift",
    "Kotlin",
    "Ruby",
    "Scala",
    "R",
    "MATLAB",
    "Dart/Flutter",
    "Auto-detect",
]

# ── Review modes ──────────────────────────────────────────────────────────────
REVIEW_MODES = {
    "🔍 Full Review": "Complete audit — bugs, best practices, security, refactoring, tests.",
    "🐛 Bug Hunt": "Focus ONLY on bugs and logical errors. Skip style suggestions.",
    "🔒 Security Audit": "Focus ONLY on vulnerabilities — injection, auth flaws, secrets.",
    "⚡ Performance Review": "Focus ONLY on complexity, bottlenecks, memory, algorithmic efficiency.",
    "🧪 Add Unit Tests": "Write a comprehensive unit test suite for the submitted code.",
    "📖 Explain This Code": "Explain what this code does in plain English for onboarding.",
    "✨ Refactor Only": "Rewrite cleaner and more idiomatic, with no logic changes.",
    "🎓 Beginner Friendly": "Review for a beginner. Be encouraging, explain every suggestion simply.",
}

# ── Quick follow-up prompts ───────────────────────────────────────────────────
QUICK_PROMPTS = [
    "What's the time & space complexity?",
    "Write unit tests for this",
    "How do I handle edge cases?",
    "Can you add type hints?",
    "Explain this to a junior dev",
    "What design pattern fits here?",
    "How do I make this async?",
    "Add proper error handling",
]

# ── Built-in example snippets ─────────────────────────────────────────────────
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
    "JavaScript — Async Race Condition": """\
function fetchUserData(userId) {
    let userData;
    fetch(`/api/users/${userId}`)
        .then(res => res.json())
        .then(data => { userData = data; });
    return userData;  // always undefined!
}
console.log(fetchUserData(1));
""",
    "Python — O(n\u00b2) Duplicate Finder": """\
def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i != j and lst[i] == lst[j]:
                if lst[i] not in duplicates:
                    duplicates.append(lst[i])
    return duplicates
""",
    "Python — Memory Leak Risk": """\
class DataProcessor:
    cache = {}   # class-level mutable shared across ALL instances!

    def process(self, key, data):
        if key not in self.cache:
            result = self.expensive_operation(data)
            self.cache[key] = result
        return self.cache[key]

    def expensive_operation(self, data):
        return [x * 2 for x in data]
""",
    "TypeScript — Missing Error Handling": """\
async function getUserProfile(id: number) {
    const res = await fetch(`/api/users/${id}`);
    const user = await res.json();
    return user.profile.name.toUpperCase();
}
""",
    "Python — Clean Code (Reference)": """\
from dataclasses import dataclass, field
from typing import Optional
import re

@dataclass
class User:
    name: str
    email: str
    age: int
    bio: Optional[str] = None
    _tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not re.match(r'^[^@]+@[^@]+\\.[^@]+$', self.email):
            raise ValueError(f"Invalid email: {self.email}")
        if self.age < 0:
            raise ValueError("Age cannot be negative")

    def is_adult(self) -> bool:
        return self.age >= 18

    def add_tag(self, tag: str) -> None:
        if tag not in self._tags:
            self._tags.append(tag.lower().strip())
""",
}
