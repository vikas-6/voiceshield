"""ElevenLabs Text-to-Speech Service Integration"""
import logging
from elevenlabs import ElevenLabs, play
from typing import Optional, Iterator

logger = logging.getLogger(__name__)

# ElevenLabs API configuration
ELEVENLABS_API_KEY = "sk_35a27c6b3bb95ab198a7ca714c4a2bd0874703549acb512e"

def elevenlabs_tts(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb", 
                  model_id: str = "eleven_multilingual_v2", 
                  output_format: str = "mp3_44100_128") -> Optional[Iterator[bytes]]:
    """Convert text to speech using ElevenLabs API
    
    Args:
        text: Text to convert to speech
        voice_id: Voice ID to use (default: Matthew)
        model_id: Model ID to use (default: eleven_multilingual_v2)
        output_format: Output format (default: mp3_44100_128)
    
    Returns:
        Iterator[bytes]: Audio data stream or None if failed
    """
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        logger.info(f"Converting text to speech: {text[:50]}...")
        
        # Generate audio from text
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
        
        logger.info("ElevenLabs TTS successful")
        return audio_stream
        
    except Exception as e:
        logger.error(f"Error in ElevenLabs TTS: {e}", exc_info=True)
        return None

def play_audio(audio_stream: Iterator[bytes]) -> bool:
    """Play audio stream
    
    Args:
        audio_stream: Audio data stream
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if audio_stream:
            play(audio_stream)
            logger.info("Audio played successfully")
            return True
        else:
            logger.warning("No audio stream to play")
            return False
    except Exception as e:
        logger.error(f"Error playing audio: {e}", exc_info=True)
        return False