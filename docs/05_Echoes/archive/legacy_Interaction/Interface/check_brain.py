import os
import sys
from dotenv import load_dotenv

load_dotenv()

print(f"Python: {sys.executable}")

try:
    import google.generativeai as genai
    print("✅ google-generativeai installed.")
except ImportError:
    print("❌ google-generativeai NOT installed.")

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print("✅ GEMINI_API_KEY found.")
    # Mask key for security in logs
    print(f"   Key: {api_key[:4]}...{api_key[-4:]}")
else:
    print("❌ GEMINI_API_KEY NOT found.")
