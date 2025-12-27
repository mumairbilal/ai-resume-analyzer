import google.generativeai as genai
import os

API_KEY = os.getenv("GOOGLE_API_KEY") 

genai.configure(api_key=API_KEY)

async def analyze_document(text: str):
    try:
        # Hum 'gemini-1.5-flash' use kar rahe hain jo direct API par available hai
        model = genai.GenerativeModel("gemini-flash-latest")
        
        prompt = f"""
        You are an Expert HR Manager & Tech Recruiter. Review this resume strictly.
        
        RESUME TEXT:
        {text[:30000]}
        
        TASK:
        Provide a brutal but constructive critique. Format the output using clear Markdown.
        
        Follow this structure exactly:
        
        # 🎯 Executive Summary
        (2-3 lines summarizing the candidate's profile and main verdict)
        
        # ⚠️ Critical Weak Points & Fixes
        
        ### 1. [Weakness Name]
        * **Problem:** (Explain why this is bad)
        * **💡 Solution:** (Specific action to fix it)
        
        ### 2. [Weakness Name]
        * **Problem:** ...
        * **💡 Solution:** ...
        
        ### 3. [Weakness Name]
        * **Problem:** ...
        * **💡 Solution:** ...
        
        # 🛠️ Skill Gap Analysis
        (Create a Markdown Table with two columns: "Missing Skill" and "Why it matters")
        
        # 🚀 Final Verdict
        (Score out of 100 and one final motivating line)
        """

        # Direct Async Call
        response = await model.generate_content_async(prompt)
        
        return response.text

    except Exception as e:
        # Agar koi bhi error aye to humein saaf pata chal jaye
        return f"Error connecting to AI: {str(e)}"
    
async def chat_with_document(text: str, question: str):
    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        
        # Chat Prompt - Hum AI ko context aur sawal dono denge
        prompt = f"""
        You are an expert Contract Assistant. Answer the user's question based ONLY on the text provided below.
        
        CONTRACT TEXT:
        {text[:50000]}
        
        USER QUESTION:
        {question}
        
        ANSWER (Keep it short and direct):
        """
        
        response = await model.generate_content_async(prompt)
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"    