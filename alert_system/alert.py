import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")

def translate_message(message, target_lang):
    """
    Translate message to target language using DeepL API
    
    Args:
        message: Text to be translated
        target_lang: Target language code (e.g., 'EN', 'KO')
        
    Returns:
        str: Translated message
    """
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": message,
        "target_lang": target_lang
    }
    response = requests.post(url, data=data)
    return response.json()["translations"][0]["text"]

def send_alert(alert_data):
    """
    Send alert with translation to specified recipient
    
    Args:
        alert_data: Dictionary containing alert information
            {
                "message": "Alert message",
                "lang": "Target language code",
                "to": "Recipient address",
                "type": "Alert type (e.g., 'health_reminder')"
            }
            
    Returns:
        dict: Alert sending status and translated message
    """
    message = alert_data["message"]
    
    # Add specific format for health reminders
    if alert_data.get("type") == "health_reminder":
        message = f"Reminder: {message} If you've already taken it, say 'yes'."
    
    # Translate message
    translated = translate_message(message, alert_data["lang"])
    
    # Prepare and send alert
    payload = {
        "message": translated,
        "to": alert_data["to"],
        "type": alert_data.get("type", "general"),
        "severity": alert_data.get("severity", "normal")
    }
    
    response = requests.post(ALERT_WEBHOOK_URL, json=payload)
    return {
        "status": "sent",
        "translated_message": translated,
        "original_message": message,
        "alert_type": alert_data.get("type", "general")
    } 