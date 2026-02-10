import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        self.client = OpenAI(api_key=self.api_key)
        
        self.system_prompt = """
You are a supportive, empathetic, and non-judgmental AI companion designed to help users who may be experiencing bullying, harassment, or emotional distress.

Your goals are:
1. **Detect Distress**: Identify signs of bullying, harassment, negative sentiment, or crisis in the user's message.
2. **Validate and Support**: Acknowledge the user's feelings. Use phrases like "I'm sorry you're going through this," "It's understandable to feel that way," and "You are not alone."
3. **Provide Guidance**: Offer gentle, practical advice for dealing with bullying (e.g., disengaging, documenting evidence, seeking help).
4. **Suggest Resources**: If the user seems very distressed or mentions self-harm, immediately provide crisis resources or suggest contacting a trusted adult or professional.
5. **Set Boundaries**: Clearly state that you are an AI, not a therapist or counselor.

**Tone**: Warm, safe, encouraging, and calm.

**Critical Safety Rule**: If the user mentions suicide, self-harm, or immediate danger to themselves or others, you MUST prioritize safety. Urge them to contact emergency services or a crisis hotline immediately.
"""

    def get_response(self, message, chat_history=[]):
        """
        Generates a response from the LLM based on the user's message and chat history.
        """
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add chat history context (limited to last 5 turns to save tokens/context)
            for turn in chat_history[-5:]:
                messages.append(turn)
            
            messages.append({"role": "user", "content": message})

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Or gpt-4o if available/preferred
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # Check for quota or billing errors
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                return self._get_mock_response(message)
            return f"I'm sorry, I encountered an error. (Error: {error_msg})"

    def _get_mock_response(self, message):
        """
        Fallback responses when the API is unavailable (e.g., quota exceeded).
        """
        msg = message.lower()
        if any(word in msg for word in ["bully", "mean", "tease", "harass", "hurt"]):
            return "I'm sorry to hear that you're being treated this way. It's not your fault. Remember that you don't have to face this alone—consider talking to a trusted adult or teacher."
        elif any(word in msg for word in ["sad", "depressed", "lonely", "cry", "upset"]):
            return "I'm sorry you're feeling down. It's okay to feel this way. Please be gentle with yourself today."
        elif any(word in msg for word in ["kill", "suicide", "die", "end it"]):
            return "CHECK_CRISIS_RESOURCES: If you are in immediate danger, please contact emergency services (911 in the US) or call/text 988 immediately."
        else:
            return "I am currently in 'Offline Mode' because the AI quota was exceeded. I can still listen, but my responses are limited. How else can I help?"
