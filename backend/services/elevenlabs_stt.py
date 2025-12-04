"""ElevenLabs Speech-to-Text Service Integration"""
import logging
import requests
import base64
import os
import json
import hashlib
from typing import Optional

logger = logging.getLogger(__name__)

# ElevenLabs API configuration
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
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
    """Convert speech to text using ElevenLabs API (no fallback)
    
    Args:
        audio_data: Audio file data
    
    Returns:
        str: Transcribed text
    """
    try:
        # Try the HTTP API with correct parameters
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        # Send audio data with the correct model
        # Send as form data with proper field names
        files = {
            'file': ('audio.webm', audio_data, 'audio/webm')
        }
        data = {
            'model_id': 'scribe_v2'
        }
        
        logger.info(f"Sending audio data to ElevenLabs STT API (size: {len(audio_data)} bytes)")
        
        # Make API request with files and data
        response = requests.post(
            f"{ELEVENLABS_API_URL}/speech-to-text",
            headers=headers,
            files=files,
            data=data,
            timeout=30  # 30 second timeout to prevent hanging
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            transcript = result.get("text", "")
            logger.info(f"ElevenLabs STT successful: {transcript[:50]}...")
            return transcript
        else:
            logger.error(f"ElevenLabs STT failed with status {response.status_code}: {response.text}")
            raise Exception(f"ElevenLabs STT failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"Error in ElevenLabs STT: {e}", exc_info=True)
        raise Exception(f"Error in ElevenLabs STT: {str(e)}")

# Mock STT fallback removed - using only ElevenLabs API for real processing