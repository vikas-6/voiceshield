"""Google Gemini API Integration for Emergency Response Generation"""
import logging
import google.generativeai as genai
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Configure Gemini API from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Validate API key is present
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is not set")
    raise ValueError(
        "GEMINI_API_KEY is required. Please add it to your backend/.env file:\n"
        "GEMINI_API_KEY=your_key_here"
    )

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model with a supported model name
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    logger.info("Successfully initialized Gemini model: gemini-2.0-flash")
except Exception as e:
    logger.error(f"Failed to initialize primary model: {e}")
    # Fallback to another model
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        logger.info("Successfully initialized fallback model: gemini-1.5-pro")
    except Exception as e2:
        logger.error(f"Failed to initialize fallback model: {e2}")
        model = None

def gemini_generate_response(emergency_type: str, severity: int, transcript: str) -> str:
    """Generate emergency response using Google Gemini API (no fallback)
    
    Args:
        emergency_type: Type of emergency (FIRE, MEDICAL, VIOLENCE, ACCIDENT, NORMAL)
        severity: Severity level (1-10)
        transcript: Original transcript
        
    Returns:
        str: Generated emergency response
    """
    # If model failed to initialize, raise exception
    if model is None:
        logger.error("Gemini model not available")
        raise Exception("Gemini model not available")
    
    try:
        # Create prompt for Gemini
        prompt = f"""
        You are an emergency response assistant. Based on the emergency type and severity, 
        generate a professional, helpful, and urgent response.
        
        Emergency Type: {emergency_type}
        Severity Level: {severity}/10
        Original Message: "{transcript}"
        
        Provide a clear, actionable response that includes:
        1. Acknowledgment of the emergency type
        2. Immediate safety advice
        3. Recommended actions
        4. Reassurance that help is being dispatched (if applicable)
        
        Keep the response concise but comprehensive. Do not include markdown or special formatting.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        
        if response.text:
            # Clean up the response
            assistant_reply = response.text.strip()
            logger.info(f"Gemini response generated successfully")
            return assistant_reply
        else:
            logger.error("Gemini returned empty response")
            raise Exception("Gemini returned empty response")
            
    except Exception as e:
        logger.error(f"Error in Gemini response generation: {e}", exc_info=True)
        raise Exception(f"Error in Gemini response generation: {str(e)}")

# Fallback responses removed - using only Gemini API for real processing