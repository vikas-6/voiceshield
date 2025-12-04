"""Complete Voice Emergency Processing Flow with Gemini API Integration"""

import logging
import uuid
import io
import base64
from datetime import datetime, timezone
from typing import Dict, Any
import asyncio
from services.elevenlabs_stt import elevenlabs_stt
from services.gemini_response import gemini_generate_response
from services.elevenlabs_tts import elevenlabs_tts
from services.event_store import event_store

logger = logging.getLogger(__name__)

def classify_emergency_by_keywords(transcript: str) -> Dict[str, Any]:
    """Classify emergency type from transcript keywords
    
    Args:
        transcript: Text to classify
        
    Returns:
        dict: Contains type, severity, and initial response
    """
    transcript_lower = transcript.lower()
    
    # Classify emergency type based on keywords
    emergency_type = "NORMAL"
    severity = 1
    
    if any(word in transcript_lower for word in ["fire", "flame", "smoke", "burning", "burn"]):
        emergency_type = "FIRE"
        severity = 8
    
    elif any(word in transcript_lower for word in ["hurt", "blood", "injured", "medical", "breathing", "unconscious", "pain", "heart", "chest"]):
        emergency_type = "MEDICAL"
        severity = 7
    
    elif any(word in transcript_lower for word in ["attack", "danger", "weapon", "threat", "help", "scared", "assault", "violence"]):
        emergency_type = "VIOLENCE"
        severity = 9
    
    elif any(word in transcript_lower for word in ["crash", "accident", "collision", "vehicle", "car", "highway", "truck", "bus"]):
        emergency_type = "ACCIDENT"
        severity = 6
    
    else:
        severity = 2
    
    logger.info(f"Classifier: Type={emergency_type}, Severity={severity}")
    
    return {
        "type": emergency_type,
        "severity": severity
    }

async def process_voice_complete_flow(audio_data: bytes) -> Dict[str, Any]:
    """Process voice recording through complete flow:
    1. Speech-to-Text (ElevenLabs)
    2. Emergency Classification (Keyword-based)
    3. Response Generation (Gemini API)
    4. Text-to-Speech (ElevenLabs)
    5. Event Storage & Broadcasting
    
    Args:
        audio_data: Audio file data
        
    Returns:
        dict: Complete emergency event with all processing results
    """
    try:
        logger.info(f"Starting complete voice processing flow with {len(audio_data)} bytes of audio data")
        
        # Step 1: Speech-to-Text using ElevenLabs
        transcript = elevenlabs_stt(audio_data)
        logger.info(f"Transcription completed: {transcript[:100]}...")
        
        # Step 2: Classify emergency based on keywords
        classification = classify_emergency_by_keywords(transcript)
        logger.info(f"Emergency classification: {classification}")
        
        # Step 3: Generate intelligent response using Gemini API
        assistant_reply = gemini_generate_response(
            classification["type"],
            classification["severity"],
            transcript
        )
        logger.info(f"Gemini response generated: {assistant_reply[:100]}...")
        
        # Step 4: Generate audio response using ElevenLabs TTS
        audio_response_stream = elevenlabs_tts(assistant_reply)
        
        # Convert audio stream to base64 for storage/transmission
        audio_base64 = None
        if audio_response_stream:
            try:
                # Collect all audio chunks
                audio_chunks = []
                for chunk in audio_response_stream:
                    audio_chunks.append(chunk)
                
                # Combine chunks into single byte array
                audio_bytes = b''.join(audio_chunks)
                
                # Encode as base64 for storage
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                logger.info(f"Audio response encoded: {len(audio_base64)} characters")
            except Exception as audio_error:
                logger.error(f"Error encoding audio response: {audio_error}")
        
        logger.info("Audio response generated successfully")
        
        # Step 5: Create complete event object
        event = {
            "id": str(uuid.uuid4()),
            "transcript": transcript,
            "type": classification["type"],
            "severity": classification["severity"],
            "assistant_reply": assistant_reply,
            "audio_response": audio_base64,  # Include audio response
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "processed_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Step 6: Store event in MongoDB
        await event_store.add_event(event)
        logger.info(f"Event stored in MongoDB: {event['id']}")
        
        return event
        
    except Exception as e:
        logger.error(f"Error in complete voice processing flow: {e}", exc_info=True)
        raise Exception(f"Error processing voice: {str(e)}")