from flask import Flask, request, jsonify
from input_schema import (
    UserProfile, EmotionData, RoutineData, AlertData,
    VAPIConfig, RoutineConfig, AlertConfig
)
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

class SafeSpeakSystem:
    def __init__(self):
        """
        Initialize SafeSpeak system components
        """
        self.vapi_url = "https://api.vapi.ai/v1"
        self.deepl_url = "https://api-free.deepl.com/v2/translate"
        self.headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }
        self.users = {}  # In-memory user storage (replace with database in production)

    def register_user(self, profile: UserProfile) -> dict:
        """
        Register a new user profile
        
        Args:
            profile: UserProfile object containing user information
            
        Returns:
            dict: Registration status
        """
        self.users[profile.user_id] = profile
        return {"status": "success", "user_id": profile.user_id}

    def analyze_emotion(self, user_id: str, audio_data: str) -> EmotionData:
        """
        Analyze user's emotional state using VAPI
        
        Args:
            user_id: User identifier
            audio_data: Base64 encoded audio data
            
        Returns:
            EmotionData: Analysis results
        """
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")

        # Call VAPI for emotion analysis
        payload = {
            "audio": audio_data,
            "config": user.vapi_config.dict(),
            "language": user.vapi_config.language
        }
        
        response = requests.post(
            f"{self.vapi_url}/analyze",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"VAPI analysis failed: {response.text}")
            
        result = response.json()
        
        return EmotionData(
            timestamp=datetime.now(),
            emotion=result["emotion"],
            severity=result["severity"],
            confidence=result["confidence"],
            transcript=result.get("transcript")
        )

    def check_routine(self, user_id: str) -> RoutineData:
        """
        Check user's routine patterns
        
        Args:
            user_id: User identifier
            
        Returns:
            RoutineData: Routine status
        """
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")

        now = datetime.now()
        last_interaction = self.get_last_interaction(user_id)
        silence_duration = (now - last_interaction).total_seconds() / 3600  # hours
        
        # Check medication status
        medication_status = self.check_medication_status(user)
        
        return RoutineData(
            timestamp=now,
            last_interaction=last_interaction,
            medication_status=medication_status,
            activity_level=self.calculate_activity_level(user_id),
            silence_duration=silence_duration
        )

    def send_alert(self, alert_data: AlertData) -> dict:
        """
        Send emergency alert with translation
        
        Args:
            alert_data: AlertData object containing alert information
            
        Returns:
            dict: Alert status
        """
        # Translate message if needed
        translated_messages = {}
        for recipient in alert_data.recipients:
            user = self.get_user_by_contact(recipient)
            if user and user.alert_config.preferred_language != "ko":
                translated = self.translate_message(
                    alert_data.message,
                    user.alert_config.preferred_language
                )
                translated_messages[recipient] = translated
            else:
                translated_messages[recipient] = alert_data.message

        # Send alerts to all recipients
        results = {}
        for recipient, message in translated_messages.items():
            # Implement actual alert sending (SMS, email, etc.)
            results[recipient] = {
                "status": "sent",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }

        return results

    def translate_message(self, message: str, target_lang: str) -> str:
        """
        Translate message using DeepL
        
        Args:
            message: Text to translate
            target_lang: Target language code
            
        Returns:
            str: Translated message
        """
        response = requests.post(
            self.deepl_url,
            data={
                "auth_key": DEEPL_API_KEY,
                "text": message,
                "target_lang": target_lang
            }
        )
        return response.json()["translations"][0]["text"]

    # Helper methods
    def get_last_interaction(self, user_id: str) -> datetime:
        """Get timestamp of last user interaction"""
        # Implement actual last interaction tracking
        return datetime.now() - timedelta(hours=1)

    def check_medication_status(self, user: UserProfile) -> List[dict]:
        """Check medication schedule status"""
        # Implement actual medication tracking
        return []

    def calculate_activity_level(self, user_id: str) -> float:
        """Calculate user's activity level"""
        # Implement actual activity level calculation
        return 0.8

    def get_user_by_contact(self, contact: str) -> Optional[UserProfile]:
        """Find user profile by contact information"""
        for user in self.users.values():
            if (user.alert_config.primary_contact == contact or 
                user.alert_config.secondary_contact == contact):
                return user
        return None

# Initialize Flask app and system
app = Flask(__name__)
system = SafeSpeakSystem()

@app.route('/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        profile = UserProfile(**request.json)
        result = system.register_user(profile)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/analyze_emotion/<user_id>', methods=['POST'])
def analyze_emotion(user_id):
    """Analyze user's emotional state"""
    try:
        audio_data = request.json.get('audio_data')
        if not audio_data:
            return jsonify({"error": "No audio data provided"}), 400
            
        result = system.analyze_emotion(user_id, audio_data)
        return jsonify(result.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/check_routine/<user_id>', methods=['GET'])
def check_routine(user_id):
    """Check user's routine"""
    try:
        result = system.check_routine(user_id)
        return jsonify(result.dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/send_alert', methods=['POST'])
def send_alert():
    """Send emergency alert"""
    try:
        alert_data = AlertData(**request.json)
        result = system.send_alert(alert_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 