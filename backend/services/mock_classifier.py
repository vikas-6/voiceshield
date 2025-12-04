"""Mock Emergency Classifier Service
TODO: Replace with Google Gemini API integration
"""
import logging
import random
from typing import Dict, Any

logger = logging.getLogger(__name__)

def mock_classifier(transcript: str) -> Dict[str, Any]:
    """Classify emergency type from transcript
    
    Args:
        transcript: Text to classify
    
    Returns:
        dict: Contains type, severity, and assistant_reply
    """
    transcript_lower = transcript.lower()
    
    # Classify emergency type based on keywords
    emergency_type = "NORMAL"
    severity = 1
    assistant_reply = "Your message has been received. How can I assist you further?"
    
    if any(word in transcript_lower for word in ["fire", "flame", "smoke", "burning", "burn"]):
        emergency_type = "FIRE"
        severity = random.randint(7, 10)
        assistant_reply = "Fire emergency detected! Evacuate immediately. Fire services have been alerted. Stay low to avoid smoke and use the nearest safe exit."
    
    elif any(word in transcript_lower for word in ["hurt", "blood", "injured", "medical", "breathing", "unconscious", "pain"]):
        emergency_type = "MEDICAL"
        severity = random.randint(6, 9)
        assistant_reply = "Medical emergency identified! Stay calm. Medical services are being dispatched. If someone is unconscious, check breathing and pulse. Do not move them unless in immediate danger."
    
    elif any(word in transcript_lower for word in ["attack", "danger", "weapon", "threat", "help", "scared"]):
        emergency_type = "VIOLENCE"
        severity = random.randint(8, 10)
        assistant_reply = "Violence threat detected! Get to a safe location immediately. Police have been notified. Lock doors if possible and stay quiet. Do not confront the threat."
    
    elif any(word in transcript_lower for word in ["crash", "accident", "collision", "vehicle", "car", "highway"]):
        emergency_type = "ACCIDENT"
        severity = random.randint(5, 8)
        assistant_reply = "Accident reported! Emergency services are on the way. Check for injuries but do not move injured persons unless necessary. Turn on hazard lights and stay safe."
    
    else:
        severity = random.randint(1, 3)
        assistant_reply = "Thank you for reaching out. Your message has been logged. If this is an emergency, please provide more details."
    
    logger.info(f"Mock Classifier: Type={emergency_type}, Severity={severity}")
    
    return {
        "type": emergency_type,
        "severity": severity,
        "assistant_reply": assistant_reply
    }
