import os
from config import Config
import google.generativeai as genai

class LLMClient:
    def __init__(self):
        self.provider = "offline"
        self.model = None
        
        # Check for valid keys (ignoring placeholders and empty strings)
        gemini_key = str(Config.GEMINI_API_KEY).strip() if Config.GEMINI_API_KEY else None
        if gemini_key and ("your_gemini_key" in gemini_key or len(gemini_key) < 10): 
            gemini_key = None

        print(f"DEBUG: Detected Gemini Key: {'Yes' if gemini_key else 'No'}")

        # Initialize Gemini
        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
                self.provider = "gemini"
                print("Initialized Gemini client.")
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
        
        if self.provider == "offline":
            print("No valid API keys found. Defaulting to OFFLINE/MOCK mode.")

    def generate(self, system_prompt, user_message, max_tokens=1000, temperature=0.7):
        """
        Unified generation method (Gemini Only).
        """
        if self.provider == "gemini":
            try:
                # Gemini doesn't support system prompts in the same way, so we prepend it
                full_prompt = f"{system_prompt}\n\nUser Message: {user_message}"
                
                # Configure safety settings to allow supportive discussions of sensitive topics
                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                ]

                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    ),
                    safety_settings=safety_settings
                )
                return response.text
            except Exception as e:
                error_msg = str(e)
                # Check for 429 Quota Exceeded
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"Gemini/Quota Error: {error_msg}. Falling back to Mock.")
                    return self._mock_response(user_message, is_fallback=True)
                return f"[Error calling Gemini API: {e}]"

        else:
            return self._mock_response(user_message)

    def _mock_response(self, message, is_fallback=False):
        msg = message.lower()
        prefix = "(Quota/Rate Limit Exceeded - Offline Mode) " if is_fallback else ""
        
        if any(word in msg for word in ["bully", "mean", "tease", "harass", "hurt"]):
            return prefix + "I'm sorry to hear that you're being treated this way. It's not your fault. Remember that you don't have to face this alone—consider talking to a trusted adult or teacher."
        return prefix + "I am currently in Offline Mode because the AI limit was reached. I can still list resources in the sidebar!"
