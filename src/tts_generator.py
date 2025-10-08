"""
Text-to-Speech generator using OpenAI's TTS API.
"""

import os
from pathlib import Path
from openai import OpenAI
from src.utils import validate_openai_key


def generate_tts(text, output_dir):
    """
    Generate speech from text using OpenAI's TTS API.
    
    Args:
        text (str): Text content to convert to speech
        output_dir (Path): Directory to save the generated audio file
        
    Returns:
        str: Path to the generated audio file
    """
    validate_openai_key()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        # Generate speech with OpenAI TTS
        response = client.audio.speech.create(
            model="tts-1",  # Use tts-1 for faster generation, tts-1-hd for higher quality
            voice="nova",   # calm, soothing voice suitable for sleep content
            input=text,
            response_format="mp3"
        )
        
        # Save the audio file
        voiceover_path = output_dir / "voiceover.mp3"
        with open(voiceover_path, 'wb') as f:
            f.write(response.content)
        
        return str(voiceover_path)
        
    except Exception as e:
        print(f"Error generating TTS: {e}")
        raise Exception(f"Could not generate voiceover: {e}")


def get_available_voices():
    """
    Get list of available TTS voices.
    
    Returns:
        list: List of available voice names
    """
    # OpenAI TTS available voices as of latest API
    return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def generate_tts_with_voice(text, output_dir, voice="nova"):
    """
    Generate speech with a specific voice.
    
    Args:
        text (str): Text content to convert to speech
        output_dir (Path): Directory to save the generated audio file
        voice (str): Voice to use for TTS generation
        
    Returns:
        str: Path to the generated audio file
    """
    validate_openai_key()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    available_voices = get_available_voices()
    if voice not in available_voices:
        print(f"Voice '{voice}' not available. Using 'nova' instead.")
        voice = "nova"
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="mp3"
        )
        
        voiceover_path = output_dir / "voiceover.mp3"
        with open(voiceover_path, 'wb') as f:
            f.write(response.content)
        
        return str(voiceover_path)
        
    except Exception as e:
        print(f"Error generating TTS with voice '{voice}': {e}")
        raise Exception(f"Could not generate voiceover: {e}")