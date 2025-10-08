"""
Metadata handler for saving YouTube video information.
"""

import json
import os
from pathlib import Path
from datetime import datetime


def save_metadata(title, description, thumbnail_path, video_path, voiceover_path, background_path, output_dir):
    """
    Save video metadata to JSON file.
    
    Args:
        title (str): YouTube video title
        description (str): YouTube video description
        thumbnail_path (str): Path to thumbnail image (can be None)
        video_path (str): Path to generated video
        voiceover_path (str): Path to voiceover audio
        background_path (str): Path to background image
        output_dir (Path): Directory containing output files
    """
    metadata = {
        "title": title,
        "description": description,
        "files": {
            "video": os.path.basename(video_path),
            "voiceover": os.path.basename(voiceover_path),
            "background": os.path.basename(background_path),
            "thumbnail": os.path.basename(thumbnail_path) if thumbnail_path else None
        },
        "paths": {
            "video": str(video_path),
            "voiceover": str(voiceover_path),
            "background": str(background_path),
            "thumbnail": str(thumbnail_path) if thumbnail_path else None
        },
        "generation_info": {
            "created_at": datetime.now().isoformat(),
            "output_directory": str(output_dir)
        }
    }
    
    # Save metadata to JSON file
    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return str(metadata_path)


def load_metadata(metadata_path):
    """
    Load metadata from JSON file.
    
    Args:
        metadata_path (str): Path to metadata JSON file
        
    Returns:
        dict: Loaded metadata
    """
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return None


def create_youtube_description_template(title, custom_description=""):
    """
    Create a formatted YouTube description template.
    
    Args:
        title (str): Video title
        custom_description (str): Custom description content
        
    Returns:
        str: Formatted description
    """
    template = f"""{title}

{custom_description}

Perfect for:
• Sleep and relaxation
• Meditation and mindfulness  
• Stress relief
• Background ambiance
• Study or work focus

For the best experience, use headphones or quality speakers.

Please do not drive or operate machinery while listening.

Subscribe for more relaxing content!

#Sleep #Relaxation #Meditation #ASMR #Peaceful #Calm #RestfulSleep #SleepAid"""

    return template


def update_metadata_with_youtube_info(metadata_path, video_id=None, upload_status=None):
    """
    Update metadata with YouTube upload information.
    
    Args:
        metadata_path (str): Path to metadata JSON file
        video_id (str): YouTube video ID (if uploaded)
        upload_status (str): Upload status information
    """
    try:
        metadata = load_metadata(metadata_path)
        if metadata:
            if not "youtube_info" in metadata:
                metadata["youtube_info"] = {}
            
            if video_id:
                metadata["youtube_info"]["video_id"] = video_id
                metadata["youtube_info"]["url"] = f"https://www.youtube.com/watch?v={video_id}"
            
            if upload_status:
                metadata["youtube_info"]["upload_status"] = upload_status
                metadata["youtube_info"]["uploaded_at"] = datetime.now().isoformat()
            
            # Save updated metadata
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
    except Exception as e:
        print(f"Error updating metadata: {e}")