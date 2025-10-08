"""
Utility functions for the Sleep Video Generator.
"""

import os
import subprocess
import platform
from pathlib import Path


def create_output_folder():
    """Create output folder for generated files."""
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def open_video(video_path):
    """Open video file with system default media player."""
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", video_path], check=True)
        elif system == "Windows":
            subprocess.run(["start", video_path], shell=True, check=True)
        else:  # Linux and others
            subprocess.run(["xdg-open", video_path], check=True)
        print(f"Opening {os.path.basename(video_path)} with default media player...")
    except subprocess.CalledProcessError:
        print(f"Could not open video file. Please manually open: {video_path}")
    except Exception as e:
        print(f"Error opening video: {e}")


def validate_openai_key():
    """Validate that OpenAI API key is available."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
    return api_key


def ensure_dependencies():
    """Check if required dependencies are available."""
    try:
        import openai
        import moviepy
        from PIL import Image
        return True
    except ImportError as e:
        print(f"Missing required dependency: {e}")
        print("Please install required packages:")
        print("pip install openai moviepy pillow python-dotenv")
        return False