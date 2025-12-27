# check_models.py
import google.generativeai as genai

# 👇 Apni Key yahan paste karo
API_KEY = "AIzaSyAL5bniO-mZHvpQ_BijCGpEmPMC5hLUAFY" 

genai.configure(api_key=API_KEY)

print("Checking available models for your key...")

try:
    # Google se pooch rahe hain: "Tumhare paas kya kya hai?"
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
except Exception as e:
    print(f"Error: {e}")