from flask import Flask, request, jsonify
import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)

def analyze_emotion(audio_data: str) -> dict:
    """
    Analyze emotion from audio data using VAPI
    
    Args:
        audio_data: Base64 encoded audio data
        
    Returns:
        dict: Analysis results
    """
    try:
        # VAPI API request configuration
        headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # VAPI Call Analysis API
        payload = {
            "audioData": audio_data,
            "config": {
                "language": "en",
                "model": "emotion-detection",
                "sensitivity": 0.8,
                "analysisPlan": {
                    "summaryPrompt": "You are an expert emotion analyzer. Summarize the emotional state of the speaker in 2-3 sentences.",
                    "structuredDataPrompt": "Extract emotional data from the call transcript.",
                    "structuredDataSchema": {
                        "type": "object",
                        "properties": {
                            "emotion": { "type": "string" },
                            "intensity": { "type": "number" },
                            "confidence": { "type": "number" }
                        },
                        "required": ["emotion", "intensity", "confidence"]
                    },
                    "successEvaluationPrompt": "Evaluate the emotional state of the speaker on a scale of 1-10, where 1 is extremely negative and 10 is extremely positive.",
                    "successEvaluationRubric": "NumericScale"
                }
            }
        }
        
        # VAPI API call
        response = requests.post(
            "https://api.vapi.ai/analyze/emotion",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # response validation
        if response.status_code != 200:
            logger.error(f"VAPI API error: {response.status_code} - {response.text}")
            raise Exception(f"VAPI analysis failed: {response.text}")
        
        # response processing
        result = response.json()
        analysis = result.get("analysis", {})
        
        # extract emotion data
        emotion = analysis.get("structuredData", {}).get("emotion", "neutral")
        intensity = analysis.get("structuredData", {}).get("intensity", 0.5)
        confidence = analysis.get("structuredData", {}).get("confidence", 0.0)
        transcript = result.get("transcript", "")
        
        # convert NumericScale to severity (1-10 scale)
        severity = analysis.get("successEvaluation", {}).get("score", 5)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "emotion": emotion,
            "severity": severity,
            "confidence": confidence,
            "transcript": transcript
        }
        
    except Exception as e:
        logger.error(f"Emotion analysis error: {str(e)}")
        raise

def send_email_notification(analysis_result: dict, recipient_email: str):
    """
    Send email notification with analysis results
    
    Args:
        analysis_result: Emotion analysis results
        recipient_email: Email address to send notification
    """
    try:
        # Email configuration
        sender_email = "safespeak@example.com"
        subject = "Emotion analysis result notification"
        
        # Create email content
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        
        # Email body
        body = f"""
        Emotion analysis result:
        
        Time: {analysis_result['timestamp']}
        Emotion: {analysis_result['emotion']}
        Severity: {analysis_result['severity']}/10
        Confidence: {analysis_result['confidence']}
        
        Transcript:
        {analysis_result['transcript']}
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, EMAIL_PASSWORD)
            server.send_message(message)
            
        logger.info(f"Email notification sent to {recipient_email}")
        
    except Exception as e:
        logger.error(f"Email sending error: {str(e)}")
        raise

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze emotion and send email notification
    """
    try:
        data = request.json
        audio_data = data.get('audio_data')
        recipient_email = data.get('recipient_email')
        
        if not audio_data or not recipient_email:
            return jsonify({
                "status": "error",
                "message": "audio_data and recipient_email are required"
            }), 400
        
        # Analyze emotion
        analysis_result = analyze_emotion(audio_data)
        
        # Send email notification
        send_email_notification(analysis_result, recipient_email)
        
        return jsonify({
            "status": "success",
            "data": analysis_result
        })
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 