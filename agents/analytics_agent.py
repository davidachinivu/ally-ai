import pandas as pd
from datetime import datetime

class AnalyticsAgent:
    def __init__(self):
        # In a real app, this would connect to a database.
        # Here we use an in-memory list for the session.
        self.session_data = []

    def log_interaction(self, user_message, analysis_result):
        """
        Logs the interaction data for the dashboard.
        """
        entry = {
            "timestamp": datetime.now(),
            "sentiment": analysis_result.get("sentiment", "neutral"),
            "risk_level": analysis_result.get("risk_level", "low"),
            "primary_emotion": analysis_result.get("emotions", ["neutral"])[0] if analysis_result.get("emotions") else "neutral"
        }
        self.session_data.append(entry)

    def get_dataframe(self):
        """
        Returns a pandas DataFrame of the session data.
        """
        if not self.session_data:
            return pd.DataFrame(columns=["timestamp", "sentiment", "risk_level", "primary_emotion"])
        return pd.DataFrame(self.session_data)
