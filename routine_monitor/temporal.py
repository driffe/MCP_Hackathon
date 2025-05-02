import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TEMPORAL_API_KEY = os.getenv("TEMPORAL_API_KEY")

class ElderlyCareMonitor:
    """
    Class for monitoring elderly care routines and emotional states
    """
    def __init__(self):
        # Initialize monitoring parameters
        self.last_interaction = None
        self.consecutive_no_response = 0
        self.check_interval = timedelta(hours=3)  # Check every 3 hours
        self.max_no_response = 2  # Maximum allowed consecutive no responses

    def check_interaction(self, user_data):
        """
        Check user's interaction patterns
        
        Args:
            user_data: Dictionary containing user interaction data
            
        Returns:
            dict: Status of user interaction
        """
        current_time = datetime.now()
        
        # Handle first interaction
        if not self.last_interaction:
            self.last_interaction = current_time
            return {"status": "first_interaction", "message": "First interaction recorded"}

        # Check for missed interactions
        if current_time - self.last_interaction > self.check_interval:
            self.consecutive_no_response += 1
            if self.consecutive_no_response >= self.max_no_response:
                return self.trigger_no_response_alert()
        else:
            self.consecutive_no_response = 0
            self.last_interaction = current_time

        return {"status": "normal", "message": "Regular interaction detected"}

    def check_emotional_state(self, emotion_data):
        """
        Check user's emotional state
        
        Args:
            emotion_data: Dictionary containing emotion analysis results
            
        Returns:
            dict: Status of emotional state
        """
        if emotion_data.get("severity", 0) >= 7:
            return self.trigger_high_risk_alert(emotion_data)
        return {"status": "normal", "message": "Emotional state stable"}

    def trigger_no_response_alert(self):
        """
        Trigger alert for no response
        
        Returns:
            dict: Alert response
        """
        url = "https://api.temporal.com/v1/alerts"
        headers = {"Authorization": f"Bearer {TEMPORAL_API_KEY}"}
        payload = {
            "type": "No Response Alert",
            "message": "No response detected for 6 hours",
            "severity": "high"
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def trigger_high_risk_alert(self, emotion_data):
        """
        Trigger alert for high emotional risk
        
        Args:
            emotion_data: Dictionary containing emotion analysis results
            
        Returns:
            dict: Alert response
        """
        url = "https://api.temporal.com/v1/alerts"
        headers = {"Authorization": f"Bearer {TEMPORAL_API_KEY}"}
        payload = {
            "type": "High Risk Alert",
            "message": f"High emotional risk detected: {emotion_data['emotion']} (severity: {emotion_data['severity']})",
            "severity": "critical"
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

def check_routine(user_data):
    """
    Main function to check user's routine and emotional state
    
    Args:
        user_data: Dictionary containing user data
        
    Returns:
        dict: Combined status of interaction and emotional state
    """
    monitor = ElderlyCareMonitor()
    interaction_result = monitor.check_interaction(user_data)
    
    if "emotion_data" in user_data:
        emotion_result = monitor.check_emotional_state(user_data["emotion_data"])
        return {
            "interaction_status": interaction_result,
            "emotion_status": emotion_result
        }
    
    return interaction_result 