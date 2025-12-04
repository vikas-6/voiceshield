"""Voice Processing Routes"""
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

# Use ElevenLabs STT instead of mock STT
from services.elevenlabs_stt import elevenlabs_stt
from services.event_store import event_store
from services.elevenlabs_tts import elevenlabs_tts
from websocket.ws_manager import manager

logger = logging.getLogger(__name__)

router = APIRouter()

class EmergencyEvent(BaseModel):
    """Emergency Event Model"""
    id: str
    transcript: str
    type: str
    severity: int
    assistant_reply: str
    timestamp: str

def mock_classifier_by_keywords(transcript: str) -> Dict[str, Any]:
    """Classify emergency type from transcript keywords
    
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
        severity = 8
        assistant_reply = "Fire emergency detected! Evacuate immediately. Fire services have been alerted. Stay low to avoid smoke and use the nearest safe exit."
    
    elif any(word in transcript_lower for word in ["hurt", "blood", "injured", "medical", "breathing", "unconscious", "pain", "heart", "chest"]):
        emergency_type = "MEDICAL"
        severity = 7
        assistant_reply = "Medical emergency identified! Stay calm. Medical services are being dispatched. If someone is unconscious, check breathing and pulse. Do not move them unless in immediate danger."
    
    elif any(word in transcript_lower for word in ["attack", "danger", "weapon", "threat", "help", "scared", "assault", "violence"]):
        emergency_type = "VIOLENCE"
        severity = 9
        assistant_reply = "Violence threat detected! Get to a safe location immediately. Police have been notified. Lock doors if possible and stay quiet. Do not confront the threat."
    
    elif any(word in transcript_lower for word in ["crash", "accident", "collision", "vehicle", "car", "highway", "truck", "bus"]):
        emergency_type = "ACCIDENT"
        severity = 6
        assistant_reply = "Accident reported! Emergency services are on the way. Check for injuries but do not move injured persons unless necessary. Turn on hazard lights and stay safe."
    
    else:
        severity = 2
        assistant_reply = "Thank you for reaching out. Your message has been logged. If this is an emergency, please provide more details."
    
    logger.info(f"Classifier: Type={emergency_type}, Severity={severity}")
    
    return {
        "type": emergency_type,
        "severity": severity,
        "assistant_reply": assistant_reply
    }

@router.post("/voice", response_model=EmergencyEvent)
async def process_voice(audio: UploadFile = File(...)) -> Dict[str, Any]:
    """Process voice recording and classify emergency
    
    Args:
        audio: Audio file upload
    
    Returns:
        EmergencyEvent: Processed emergency event
    """
    try:
        logger.info(f"Processing voice upload: {audio.filename}")
        
        # Read audio data
        audio_data = await audio.read()
        logger.info(f"Audio data received: {len(audio_data)} bytes")
        
        # Step 1: Speech-to-Text (using ElevenLabs with fallback)
        transcript = elevenlabs_stt(audio_data)
        logger.info(f"Transcript generated: {transcript[:50]}...")
        
        # Step 2: Classify emergency based on keywords in transcript
        classification = mock_classifier_by_keywords(transcript)
        logger.info(f"Classification: {classification['type']}")
        
        # Step 3: Generate audio response (using ElevenLabs TTS)
        audio_response = elevenlabs_tts(classification["assistant_reply"])
        if audio_response is None:
            logger.warning("Failed to generate audio response")
        
        # Step 4: Create event object
        event = {
            "id": str(uuid.uuid4()),
            "transcript": transcript,
            "type": classification["type"],
            "severity": classification["severity"],
            "assistant_reply": classification["assistant_reply"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Step 5: Store event in MongoDB
        await event_store.add_event(event)
        logger.info(f"Event stored in MongoDB: {event['id']}")
        
        # Step 6: Broadcast to WebSocket clients
        await manager.broadcast(event)
        logger.info(f"Event broadcast via WebSocket: {event['id']}")
        
        return event
        
    except Exception as e:
        logger.error(f"Error processing voice: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")

@router.get("/events")
async def get_events(limit: int = 50):
    """Get recent emergency events
    
    Args:
        limit: Maximum number of events to return
    
    Returns:
        List of recent events
    """
    try:
        events = await event_store.get_events(limit=limit)
        logger.info(f"Retrieved {len(events)} events from MongoDB")
        return {"events": events, "count": len(events)}
    except Exception as e:
        logger.error(f"Error retrieving events: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving events: {str(e)}")