import google.generativeai as genai

API_KEY_FILE = 'C:/Users/User/OneDrive/Desktop/llm ai chatbot/gemini api key.txt'
try:
    with open(API_KEY_FILE, 'r') as file:
        GEMINI_API_KEY = file.read().strip()
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("Available Models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
