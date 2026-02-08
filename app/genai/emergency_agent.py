class EmergencyAgent:
    def __init__(self):
        pass

    def get_response(self, user_input):
        # Mock response for now. 
        # In a real app, this would call OpenAI/Gemini API.
        user_input = user_input.lower()
        if "chest pain" in user_input or "heart" in user_input:
            return "Critical: Please call emergency services (911/112) immediately. Do not drive yourself. Chew an aspirin if not allergic."
        elif "fever" in user_input:
            return "Monitor temperature. Stay hydrated. If above 103F or lasts >3 days, consult a doctor."
        elif "headache" in user_input:
            return "Rest in a dark room. Hydrate. Take over-the-counter pain relief if needed. Seek help if accompanied by vision loss or slurred speech."
        else:
            return "I am an AI assistant. For serious symptoms, please consult a doctor immediately. I recommend booking an appointment."
