#!/usr/bin/env python3
"""
Sleep Video Generator CLI
Main entry point for the YouTube-ready sleep/relaxation video generator.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import helper modules
from src.background_generator import generate_background
from src.tts_generator import generate_tts
from src.video_creator import create_video
from src.thumbnail_generator import generate_thumbnail
from src.metadata_handler import save_metadata
from src.utils import create_output_folder, open_video
from src.music_generator import get_music_types


def main():
    """Main function to run the Sleep Video Generator CLI."""
    print("Welcome to the Sleep Video Generator.")
    print("This tool will turn your script into a YouTube-ready video with AI voiceover and background.")
    print()
    
    # Create output folder
    output_dir = create_output_folder()
    
    # Step 2: Script Input
    script_content = get_script_input()
    
    # Step 3: Background Image Generation
    background_path = generate_background_image(output_dir)
    
    # Step 4: Voice Generation
    voiceover_path = generate_voice(script_content, output_dir)
    
    # Step 4.5: Music Type Selection
    music_type = get_music_type_selection()
    
    # Step 5: Video Creation
    video_path = create_sleep_video(background_path, voiceover_path, output_dir, music_type)
    
    # Step 6: Review
    review_video(video_path)
    
    # Step 7: YouTube Metadata
    title, description = get_youtube_metadata()
    
    # Step 8: Thumbnail Generation
    thumbnail_path = generate_youtube_thumbnail(output_dir)
    
    # Save metadata
    save_metadata(title, description, thumbnail_path, video_path, voiceover_path, background_path, output_dir)
    
    # Step 9: Summary
    print_summary(video_path, voiceover_path, background_path, thumbnail_path)


def get_script_input():
    """Get script content from script.txt file."""
    script_path = "script.txt"
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            print("The script.txt file appears to be empty. Please add content to script.txt.")
            sys.exit(1)
            
        print(f"Loaded {len(content)} characters from {os.path.basename(script_path)}.")
        print()
        return content
        
    except FileNotFoundError:
        print(f"File '{script_path}' not found. Please create a script.txt file in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def generate_background_image(output_dir):
    """Generate background image based on user prompt."""
    prompt = input("Describe the visual theme for your video background (e.g., \"starry night sky with calm waves\"): ").strip()
    
    if not prompt:
        prompt = "peaceful starry night sky with gentle waves"
        print(f"Using default prompt: {prompt}")
    
    print("Generating background image...")
    background_path = generate_background(prompt, output_dir)
    print(f"Background image generated and saved as {os.path.basename(background_path)}.")
    print()
    return background_path


def generate_voice(script_content, output_dir):
    """Generate TTS voiceover from script content."""
    print("Generating voiceover...")
    voiceover_path = generate_tts(script_content, output_dir)
    print(f"Voiceover generated and saved as {os.path.basename(voiceover_path)}.")
    print()
    return voiceover_path


def get_music_type_selection():
    """Get user's choice for background music type."""
    music_types = get_music_types()
    
    print("Choose background music type:")
    print("1. ambient - Lofi and ambient background music (recommended)")
    print("2. nature - Nature sounds (rain, forest, ocean)")
    print("3. meditation - Calm meditation and zen music")
    print("4. piano - Peaceful piano melodies")
    print("5. space - Deep space and cosmic ambient sounds")
    print("6. silence - No background music")
    
    while True:
        choice = input("Enter your choice (1-6): ").strip()
        
        music_map = {
            "1": "ambient",
            "2": "nature", 
            "3": "meditation",
            "4": "piano",
            "5": "space",
            "6": "silence"
        }
        
        if choice in music_map:
            selected_type = music_map[choice]
            print(f"Selected: {selected_type}")
            print()
            return selected_type
        else:
            print("Please enter a number between 1-6.")


def create_sleep_video(background_path, voiceover_path, output_dir, music_type="ambient"):
    """Create the final video with background, voiceover, and music."""
    print("Creating video...")
    video_path = create_video(background_path, voiceover_path, output_dir, music_type)
    print(f"Video exported successfully to {os.path.basename(video_path)}.")
    print()
    return video_path


def review_video(video_path):
    """Ask user if they want to view the generated video."""
    while True:
        response = input("Would you like to view the video now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            open_video(video_path)
            break
        elif response in ['n', 'no']:
            break
        else:
            print("Please enter 'y' for yes or 'n' for no.")
    print()


def get_youtube_metadata():
    """Get YouTube title and description from user."""
    title = input("Enter a YouTube title for your video: ").strip()
    
    print("Enter a YouTube description (press Enter twice to finish):")
    description_lines = []
    empty_line_count = 0
    
    while empty_line_count < 2:
        line = input()
        if line.strip() == "":
            empty_line_count += 1
        else:
            empty_line_count = 0
        description_lines.append(line)
    
    # Remove the last two empty lines
    description = "\n".join(description_lines[:-2])
    print()
    return title, description


def generate_youtube_thumbnail(output_dir):
    """Generate YouTube thumbnail if user wants one."""
    while True:
        response = input("Would you like to generate a YouTube thumbnail? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return create_thumbnail_workflow(output_dir)
        elif response in ['n', 'no']:
            print()
            return None
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def create_thumbnail_workflow(output_dir):
    """Handle the thumbnail creation workflow with regeneration options."""
    prompt = input("Describe your desired thumbnail (e.g., \"calm night sky with soft glowing stars and relaxing text\"): ").strip()
    
    if not prompt:
        prompt = "calm night sky with soft glowing stars and relaxing sleep text"
        print(f"Using default prompt: {prompt}")
    
    thumbnail_counter = 1
    
    while True:
        print("Generating thumbnail...")
        thumbnail_path = generate_thumbnail(prompt, output_dir, thumbnail_counter)
        print(f"Thumbnail saved as {os.path.basename(thumbnail_path)}.")
        
        while True:
            response = input("Do you like it? (accept / regenerate / edit prompt): ").strip().lower()
            
            if response in ['accept', 'a']:
                print()
                return thumbnail_path
            elif response in ['regenerate', 'r']:
                thumbnail_counter += 1
                break
            elif response in ['edit prompt', 'edit', 'e']:
                prompt = input("Enter new thumbnail description: ").strip()
                if not prompt:
                    prompt = "calm night sky with soft glowing stars and relaxing sleep text"
                thumbnail_counter += 1
                break
            else:
                print("Please enter 'accept', 'regenerate', or 'edit prompt'.")


def print_summary(video_path, voiceover_path, background_path, thumbnail_path):
    """Print final summary of generated files."""
    print("Video generation complete.")
    print(f"Video: {os.path.basename(video_path)}")
    print(f"Voiceover: {os.path.basename(voiceover_path)}")
    print(f"Background: {os.path.basename(background_path)}")
    if thumbnail_path:
        print(f"Thumbnail: {os.path.basename(thumbnail_path)}")
    print("Title and description saved to metadata.json.")
    print("Ready for YouTube upload.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)