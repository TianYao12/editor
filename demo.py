#!/usr/bin/env python3
"""
Demo script for the Sleep Video Generator.
Creates a short demo video to test all functionality.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from src.background_generator import generate_background
from src.tts_generator import generate_tts
from src.video_creator import create_video
from src.thumbnail_generator import generate_thumbnail
from src.metadata_handler import save_metadata
from src.utils import create_output_folder

def run_demo():
    """Run a quick demo of the video generation process."""
    print("Sleep Video Generator - Quick Demo")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Create output folder
    output_dir = create_output_folder()
    print(f"Output directory: {output_dir}")
    
    # Short demo script
    demo_script = """Welcome to this peaceful moment. 
Take a deep breath and let yourself relax. 
Feel the calm wash over you as you drift into tranquility."""
    
    try:
        print("\nGenerating background image...")
        background_path = generate_background("peaceful starry night sky", output_dir)
        print(f"Background saved: {os.path.basename(background_path)}")
        
        print("\nGenerating voiceover...")
        voiceover_path = generate_tts(demo_script, output_dir)
        print(f"Voiceover saved: {os.path.basename(voiceover_path)}")
        
        print("\nCreating video...")
        video_path = create_video(background_path, voiceover_path, output_dir)
        print(f"Video saved: {os.path.basename(video_path)}")
        
        print("\nGenerating thumbnail...")
        thumbnail_path = generate_thumbnail("calm sleep video with stars", output_dir)
        print(f"Thumbnail saved: {os.path.basename(thumbnail_path)}")
        
        # Save metadata
        metadata_path = save_metadata(
            "Demo Sleep Video",
            "A peaceful demo video for relaxation",
            thumbnail_path,
            video_path,
            voiceover_path,
            background_path,
            output_dir
        )
        print(f"Metadata saved: {os.path.basename(metadata_path)}")
        
        print("\nDemo completed successfully!")
        print(f"All files saved in: {output_dir}")
        print("\nGenerated files:")
        for file in output_dir.glob("*"):
            print(f"  - {file.name}")
            
    except Exception as e:
        print(f"\nDemo failed: {e}")
        print("Make sure your OpenAI API key is valid and has sufficient credits.")
        return False
    
    return True

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)