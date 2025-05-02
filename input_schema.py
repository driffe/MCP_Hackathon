from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class VAPIConfig(BaseModel):
    """
    Configuration for VAPI emotion detection
    """
    emotion_detection: bool = True
    language: str = "ko"
    sensitivity: float = 0.8  # Emotion detection sensitivity

class RoutineConfig(BaseModel):
    """
    Configuration for routine monitoring
    """
    check_interval_hours: int = 3
    max_silence_hours: int = 6
    medication_times: List[str] = []  # List of medication times in HH:MM format

class AlertConfig(BaseModel):
    """
    Configuration for alert system
    """
    primary_contact: str
    secondary_contact: Optional[str] = None
    welfare_center: Optional[str] = None
    preferred_language: str = "ko"

class UserProfile(BaseModel):
    """
    User profile and configuration
    """
    user_id: str
    name: str
    age: int
    vapi_config: VAPIConfig
    routine_config: RoutineConfig
    alert_config: AlertConfig

class EmotionData(BaseModel):
    """
    Emotion analysis data from VAPI
    """
    timestamp: datetime
    emotion: str
    severity: float  # 0-10 scale
    confidence: float
    transcript: Optional[str] = None

class RoutineData(BaseModel):
    """
    Routine monitoring data
    """
    timestamp: datetime
    last_interaction: datetime
    medication_status: List[dict]  # List of medication events
    activity_level: float  # 0-1 scale
    silence_duration: float  # Hours of silence

class AlertData(BaseModel):
    """
    Alert data for emergency notifications
    """
    type: str  # "emotional", "routine", "medication", "silence"
    severity: str  # "low", "medium", "high", "critical"
    message: str
    context: dict  # Additional context data
    recipients: List[str] 