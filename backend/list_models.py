import os
import sys

try:
    import google.generativeai as genai
except ImportError:
    print("Please install google-generativeai: pip install google-generativeai")
    sys.exit(1)

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    print("Run this script as: GOOGLE_API_KEY='your-key' python list_models.py")
    sys.exit(1)

print("Authenticating with Google AI Studio...")
genai.configure(api_key=api_key)

print("\n--- Available Models for this API Key ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    print("-----------------------------------------")
    print("If you don't see 'models/gemini-1.5-flash' or 'models/gemini-1.5-pro',")
    print("it means your API key/account does not have access to the 1.5 models (likely due to region restrictions).")
except Exception as e:
    print(f"Failed to list models: {e}")
