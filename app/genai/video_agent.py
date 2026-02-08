import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

class VideoAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found in .env")
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')

    def analyze_consultation(self, video_path):
        """
        Uploads video to Gemini and requests transcription + medical insights.
        """
        if not os.path.exists(video_path):
            return {"error": "Video file not found."}

        print(f"Uploading {video_path} to Gemini...")
        video_file = genai.upload_file(video_path)
        
        # Wait for processing
        while video_file.state.name == "PROCESSING":
            print("Waiting for video processing...")
            time.sleep(2)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            return {"error": "Video processing failed at Gemini end."}

        print("Video processed. Generating insights...")
        
        prompt = """
        You are a medical AI assistant. Analyze this consultation video.
        Provide the output in the following format:
        
        **Transcript**:
        (Provide a summary or full transcript of what was said)
        
        **Key Symptoms**:
        (List the symptoms mentioned)
        
        **Recommended Next Steps**:
        (Suggest clinical next steps based on the symptoms)
        """
        
        try:
            response = self.model.generate_content([video_file, prompt])
        except Exception as e:
            return {"error": f"Gemini API Error: {str(e)}"}
        
        # Cleanup: delete file from Gemini to save storage/privacy
        try:
            genai.delete_file(video_file.name)
        except:
            pass
            
        return {"text": response.text}
