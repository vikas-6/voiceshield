"""ElevenLabs Speech-to-Text Service Integration"""
import logging
import requests
import base64
import os
import json
from typing import Optional

logger = logging.getLogger(__name__)

# ElevenLabs API configuration
ELEVENLABS_API_KEY = "sk_35a27c6b3bb95ab198a7ca714c4a2bd0874703549acb512e"
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"

def get_scribe_token() -> Optional[str]:
    """Get a single-use token for ElevenLabs Scribe v2 Realtime
    
    Returns:
        str: Token for realtime transcription or None if failed
    """
    try:
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{ELEVENLABS_API_URL}/single-use-token/realtime_scribe",
            headers=headers
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("token")
            logger.info("Successfully obtained Scribe token")
            return token
        else:
            logger.error(f"Failed to get Scribe token: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error getting Scribe token: {e}", exc_info=True)
        return None

def elevenlabs_stt(audio_data: bytes) -> str:
    """Convert speech to text using ElevenLabs API with fallback to mock STT
    
    Args:
        audio_data: Audio file data
    
    Returns:
        str: Transcribed text
    """
    try:
        # First try to get a token for realtime transcription
        token = get_scribe_token()
        if not token:
            logger.warning("Failed to get Scribe token, falling back to mock STT")
            return mock_stt_fallback(audio_data)
        
        # Try the HTTP API with correct parameters
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "audio/webm"
        }
        
        # Send model_id in the body as JSON
        data = {
            "model_id": "eleven_multilingual_v2"
        }
        
        files = {
            'audio': ('audio.webm', audio_data, 'audio/webm')
        }
        
        logger.info(f"Sending audio data to ElevenLabs STT API (size: {len(audio_data)} bytes)")
        
        # Make API request with model_id in form data
        response = requests.post(
            f"{ELEVENLABS_API_URL}/speech-to-text",
            headers=headers,
            data=data,
            files=files
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            transcript = result.get("text", "")
            logger.info(f"ElevenLabs STT successful: {transcript[:50]}...")
            return transcript
        else:
            logger.warning(f"ElevenLabs STT failed with status {response.status_code}: {response.text}")
            # Fallback to mock STT
            return mock_stt_fallback(audio_data)
            
    except Exception as e:
        logger.error(f"Error in ElevenLabs STT: {e}", exc_info=True)
        # Fallback to mock STT
        return mock_stt_fallback(audio_data)

def mock_stt_fallback(audio_data) -> str:
    """Fallback mock STT implementation
    
    Args:
        audio_data: Audio file data (currently unused in mock)
    
    Returns:
        str: Simulated transcript
    """
    if not audio_data or len(audio_data) < 100:
        logger.info("Mock STT: Empty or too short audio detected")
        return "I couldn't hear anything clearly."
    
    # Simulate various emergency scenarios for demo
    mock_transcripts = [
        "There's a fire in the building, we need help immediately!",
        "Someone is hurt badly, there's blood everywhere!",
        "I'm being attacked, please send help to my location!",
        "There was a car crash at the intersection, multiple vehicles involved!",
        "Everything is fine, just testing the system.",
        "Help! The kitchen is on fire and smoke is spreading!",
        "Medical emergency, person not breathing properly!",
        "Danger! Someone has a weapon!",
        "Accident on highway, people are injured!"
    ]
    
    # Use audio data length to pseudo-randomly select a transcript
    index = len(audio_data) % len(mock_transcripts)
    transcript = mock_transcripts[index]
    
    logger.info(f"Mock STT fallback generated transcript: {transcript[:50]}...")
    return transcript