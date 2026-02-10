import json
from agents.base_agent import BaseAgent

class DetectionAgent(BaseAgent):
    def process(self, message):
        """
        Analyzes the message for sentiment, toxicity, and risk.
        Returns a dictionary with analysis results.
        """
        system_prompt = """
        You are an expert safety and sentiment analysis AI.
        Analyze the following user message.
        
        Return a valid JSON object with the following fields:
        - "sentiment": "positive", "neutral", or "negative"
        - "emotions": list of detected emotions (e.g., ["sadness", "anger", "fear", "joy"])
        - "risk_level": "low", "medium", "high", or "crisis"
        - "topics": list of topics (e.g., ["bullying", "self-harm", "casual", "school"])
        
        Rules for Risk Level:
        - "crisis": Strict trigger for self-harm, suicide, or immediate danger.
        - "high": Severe bullying, harassment, or deep emotional distress.
        - "medium": Moderate distress, complaining about unfair treatment.
        - "low": Casual conversation, greetings, or mild frustration.
        """
        
        try:
            response_text = self.llm.generate(
                system_prompt=system_prompt,
                user_message=message,
                temperature=0.1 # Lower temperature for classification consistency
            )
            
            # Clean up potential markdown code blocks if the LLM adds them
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(clean_text)
            
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from Detection Agent. Raw response: {response_text}")
            # Fallback safe response
            return {
                "sentiment": "neutral",
                "emotions": [],
                "risk_level": "low",
                "topics": []
            }
        except Exception as e:
            print(f"Detection Agent Error: {e}")
            return {
                "sentiment": "neutral",
                "emotions": [],
                "risk_level": "low",
                "topics": []
            }
