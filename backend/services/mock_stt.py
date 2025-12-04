"""Mock Speech-to-Text Service
TODO: Replace with ElevenLabs STT integration
"""
import logging

logger = logging.getLogger(__name__)

def mock_stt(audio_data) -> str:
    """Simulate speech-to-text conversion
    
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
    
    logger.info(f"Mock STT generated transcript: {transcript[:50]}...")
    return transcript
