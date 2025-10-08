"""
Background image generator using OpenAI's image generation API.
"""

import os
import requests
from pathlib import Path
from openai import OpenAI
from src.utils import validate_openai_key


def generate_background(prompt, output_dir):
    """
    Generate a 1920x1080 background image using OpenAI's image generation API.
    
    Args:
        prompt (str): Description of the desired background image
        output_dir (Path): Directory to save the generated image
        
    Returns:
        str: Path to the generated background image
    """
    validate_openai_key()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        # Generate image with OpenAI DALL-E
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A beautiful, calming {prompt}, perfect for a sleep/meditation video background, 16:9 aspect ratio, high quality, peaceful atmosphere",
            size="1792x1024",  # Closest to 1920x1080 available
            quality="standard",
            n=1,
        )
        
        # Download the generated image
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Save the image
        background_path = output_dir / "background.png"
        with open(background_path, 'wb') as f:
            f.write(image_response.content)
        
        return str(background_path)
        
    except Exception as e:
        print(f"Error generating background image: {e}")
        # Create a simple fallback background
        return create_fallback_background(output_dir)


def create_fallback_background(output_dir):
    """
    Create a simple fallback background if image generation fails.
    
    Args:
        output_dir (Path): Directory to save the fallback image
        
    Returns:
        str: Path to the fallback background image
    """
    try:
        from PIL import Image, ImageDraw
        
        # Create a dark gradient background
        width, height = 1920, 1080
        image = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Create a simple gradient from dark blue to black
        for y in range(height):
            # Gradient from dark blue (25, 25, 112) to black (0, 0, 0)
            ratio = y / height
            r = int(25 * (1 - ratio))
            g = int(25 * (1 - ratio))
            b = int(112 * (1 - ratio))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Save the fallback background
        background_path = output_dir / "background.png"
        image.save(background_path, "PNG")
        
        print("Created fallback background image.")
        return str(background_path)
        
    except Exception as e:
        print(f"Error creating fallback background: {e}")
        raise Exception("Could not generate or create background image")