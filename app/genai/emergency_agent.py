import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class EmergencyAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found in .env")
            self.model = None
            return
            
        genai.configure(api_key=api_key)
        # Using the same model as VideoAgent for consistency
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        
        self.system_instruction = """
        You are an AI Medical Assistant for an emergency triage chat.
        Your goal is to assess symptoms and provide immediate guidance.
        
        RULES:
        1. If the user describes life-threatening symptoms (chest pain, severe bleeding, difficulty breathing, stroke signs), 
           IMMEDIATELY tell them to call Emergency Services (911/112) and do not provide other advice until that is emphasized.
        2. Be concise and empathetic.
        3. Explain that you are an AI and not a doctor.
        4. Suggest booking an appointment if the issue is non-critical.
        
        Keep responses short (under 50 words unless detailed triage is needed).
        """

    def get_response(self, user_input):
        if not self.model:
            return "Error: AI not configured. Please check API Key."
            
        try:
            # Construct a prompt with system instruction
            full_prompt = f"{self.system_instruction}\n\nUser: {user_input}\nAI:"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"I am having trouble connecting to the AI brain right now. Please consult a doctor. Error: {str(e)}"
