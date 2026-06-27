"""
test_groq.py — Quick test to verify your Groq API key works.
Run: python test_groq.py
"""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ No GROQ_API_KEY found in .env file!")
    exit(1)

print("Testing Groq API key...\n")

try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say 'Groq API is working!' and nothing else."}],
        max_tokens=20,
    )
    print("✅ " + response.choices[0].message.content)
    print("\nAvailable free models for this project:")
    print("  • llama-3.3-70b-versatile  (best quality)")
    print("  • llama-3.1-8b-instant     (fastest)")
    print("  • gemma2-9b-it             (alternative)")
except Exception as e:
    print(f"❌ Error: {e}")
