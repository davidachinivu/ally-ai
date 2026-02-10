from agents.base_agent import BaseAgent
import utils

class ResponseAgent(BaseAgent):
    def process(self, message, analysis_result):
        """
        Generates a supportive response based on the analysis.
        """
        risk_level = analysis_result.get("risk_level", "low")
        topics = analysis_result.get("topics", [])
        
        # 1. Crisis Intervention (Hardcoded safety override)
        if risk_level == "crisis":
            return self._get_crisis_message()

        # 2. Dynamic Persona Prompt Construction
        system_prompt = self._build_system_prompt(analysis_result)
        
        # 3. Generate Response
        response = self.llm.generate(
            system_prompt=system_prompt,
            user_message=message,
            temperature=0.7
        )
        
        return response

    def _get_crisis_message(self):
        return (
            "I am very concerned about what you're sharing. It sounds like you are in significant pain or danger. "
            "I am an AI and cannot provide the help you need right now. "
            "PLEASE contact a crisis counselor immediately:\n\n" + utils.CRISIS_RESOURCES
        )

    def _build_system_prompt(self, analysis):
        base_prompt = """
        You are Ally, a supportive, empathetic peer-support AI. 
        Your goal is to provide comfort, validation, and practical advice against bullying.
        """
        
        risk = analysis.get("risk_level", "low")
        emotions = ", ".join(analysis.get("emotions", []))
        
        if risk == "high":
            base_prompt += f"\nThe user is experiencing HIGH distress (Risk: High). Emotions detected: {emotions}. Validate their feelings deeply. Be gentle but firm that nobody deserves to be mistreated. Suggest talking to an adult."
        elif risk == "medium":
             base_prompt += f"\nThe user is feeling moderate distress. Emotions: {emotions}. Offer a listening ear and simple coping strategies."
        else:
             base_prompt += "\nThe user is engaging in casual conversation. Be friendly, warm, and welcoming. Keep replies concise."
             
        base_prompt += "\n\nProvide a natural, human-like response. Do NOT start every sentence with 'I understand'. vary your language."
        
        return base_prompt
