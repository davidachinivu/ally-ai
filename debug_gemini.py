import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: API Key found: {'Yes' if api_key else 'No'}")

if not api_key:
    print("Please add GEMINI_API_KEY to .env")
    exit()

# strip whitespace
api_key = api_key.strip()
if "your_gemini_key" in api_key:
    print("Error: Placeholder key found.")
    exit()

try:
    genai.configure(api_key=api_key)
    
    print("\n--- Listing Available Models ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
    print("\n--- Testing Generation with 'gemini-1.5-flash' ---")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, can you hear me?")
    print(f"Success! Response: {response.text}")

except Exception as e:
    print(f"\nError: {e}")
