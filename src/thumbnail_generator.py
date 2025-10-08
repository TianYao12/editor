"""
YouTube thumbnail generator using OpenAI's image generation API.
"""

import os
import requests
from pathlib import Path
from openai import OpenAI
from src.utils import validate_openai_key


def generate_thumbnail(prompt, output_dir, counter=1):
    """
    Generate a YouTube thumbnail (1280x720) using OpenAI's image generation API.
    
    Args:
        prompt (str): Description of the desired thumbnail
        output_dir (Path): Directory to save the generated thumbnail
        counter (int): Counter for thumbnail naming (thumbnail_1.png, etc.)
        
    Returns:
        str: Path to the generated thumbnail
    """
    validate_openai_key()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    try:
        # Generate thumbnail with OpenAI DALL-E
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"YouTube thumbnail: {prompt}, 16:9 aspect ratio, eye-catching, high quality, vibrant colors, professional look",
            size="1792x1024",  # Closest to 1280x720 available
            quality="standard",
            n=1,
        )
        
        # Download the generated image
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Save the thumbnail
        thumbnail_path = output_dir / f"thumbnail_{counter}.png"
        with open(thumbnail_path, 'wb') as f:
            f.write(image_response.content)
        
        return str(thumbnail_path)
        
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        # Create a simple fallback thumbnail
        return create_fallback_thumbnail(output_dir, counter, prompt)


def create_fallback_thumbnail(output_dir, counter, prompt="Sleep Video"):
    """
    Create a simple fallback thumbnail if image generation fails.
    
    Args:
        output_dir (Path): Directory to save the fallback thumbnail
        counter (int): Counter for thumbnail naming
        prompt (str): Text to include in the thumbnail
        
    Returns:
        str: Path to the fallback thumbnail
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create thumbnail dimensions (1280x720)
        width, height = 1280, 720
        image = Image.new('RGB', (width, height), (25, 25, 112))  # Dark blue background
        draw = ImageDraw.Draw(image)
        
        # Create a gradient background
        for y in range(height):
            ratio = y / height
            r = int(25 + (50 * ratio))
            g = int(25 + (50 * ratio))
            b = int(112 + (50 * ratio))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add text
        try:
            # Try to use a system font
            font_size = 80
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            try:
                # Fallback to default font
                font = ImageFont.load_default()
            except:
                font = None
        
        # Prepare text
        text_lines = ["Sleep &", "Relaxation", "Video"]
        if "calm" in prompt.lower() or "peaceful" in prompt.lower():
            text_lines = ["Peaceful", "Sleep", "Journey"]
        elif "night" in prompt.lower() or "star" in prompt.lower():
            text_lines = ["Starry", "Night", "Sleep"]
        
        # Draw text
        y_offset = height // 4
        for line in text_lines:
            if font:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            else:
                text_width = len(line) * 10
                text_height = 20
            
            x = (width - text_width) // 2
            y = y_offset
            
            # Draw text with outline
            if font:
                # Outline
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0))
                # Main text
                draw.text((x, y), line, font=font, fill=(255, 255, 255))
            else:
                draw.text((x, y), line, fill=(255, 255, 255))
            
            y_offset += text_height + 20
        
        # Save the fallback thumbnail
        thumbnail_path = output_dir / f"thumbnail_{counter}.png"
        image.save(thumbnail_path, "PNG")
        
        print("Created fallback thumbnail.")
        return str(thumbnail_path)
        
    except Exception as e:
        print(f"Error creating fallback thumbnail: {e}")
        raise Exception("Could not generate or create thumbnail")