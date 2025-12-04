"""Voice Processing Routes"""
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from pydantic import BaseModel
import base64

# Import complete flow service
from services.complete_flow import process_voice_complete_flow
from services.event_store import event_store
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

@router.post("/voice", response_model=EmergencyEvent)
async def process_voice(audio: UploadFile = File(...)) -> Dict[str, Any]:
    """Process voice recording through complete flow with Gemini API integration
    
    Args:
        audio: Audio file upload
    
    Returns:
        EmergencyEvent: Processed emergency event
    """
    try:
        logger.info(f"Processing voice upload through complete flow: {audio.filename}")
        
        # Read audio data
        audio_data = await audio.read()
        logger.info(f"Audio data received: {len(audio_data)} bytes")
        
        # Process through complete flow: STT -> Classification -> Gemini Response -> TTS -> Storage
        event = await process_voice_complete_flow(audio_data)
        
        # Broadcast to WebSocket clients
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

@router.get("/audio/{event_id}")
async def get_audio_response(event_id: str):
    """Get audio response for a specific event
    
    Args:
        event_id: ID of the event
    
    Returns:
        Audio file response
    """
    try:
        # Retrieve event from database
        events = await event_store.get_events(limit=100)  # Get enough events to find the one we need
        event = None
        
        for e in events:
            if e.get('id') == event_id and e.get('audio_response'):
                event = e
                break
        
        if not event:
            raise HTTPException(status_code=404, detail="Event or audio response not found")
        
        # Decode base64 audio data
        audio_base64 = event['audio_response']
        audio_bytes = base64.b64decode(audio_base64)
        
        # Return audio response
        return Response(content=audio_bytes, media_type="audio/mpeg")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving audio response: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving audio response: {str(e)}")