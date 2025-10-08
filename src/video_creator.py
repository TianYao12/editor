"""
Video creator using MoviePy for compositing background and audio.
"""

import os
from pathlib import Path
from moviepy import (
    ImageClip, 
    AudioFileClip, 
    CompositeVideoClip, 
    TextClip,
    concatenate_videoclips,
    ColorClip
)


def create_video(background_path, audio_path, output_dir):
    """
    Create a sleep video with background image and voiceover.
    
    Args:
        background_path (str): Path to the background image
        audio_path (str): Path to the audio file
        output_dir (Path): Directory to save the output video
        
    Returns:
        str: Path to the generated video file
    """
    try:
        # Use simple video creation for now
        return create_simple_video(background_path, audio_path, output_dir)
        
    except Exception as e:
        print(f"Error creating video: {e}")
        # Try even simpler approach
        try:
            return create_basic_video(background_path, audio_path, output_dir)
        except Exception as e2:
            print(f"Error creating basic video: {e2}")
            raise Exception(f"Could not create video: {e2}")


def create_basic_video(background_path, audio_path, output_dir):
    """
    Create the most basic video - just background image with audio.
    
    Args:
        background_path (str): Path to the background image
        audio_path (str): Path to the audio file
        output_dir (Path): Directory to save the output video
        
    Returns:
        str: Path to the generated video file
    """
    try:
        # Load audio to get duration
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Create background video clip
        background = ImageClip(background_path, duration=duration)
        
        # Add audio to background
        final_video = background.with_audio(audio)
        
        # Export video with macOS-compatible settings
        output_path = output_dir / "output.mp4"
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            audio_bitrate='128k',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            ffmpeg_params=['-movflags', '+faststart', '-pix_fmt', 'yuv420p']
        )
        
        # Clean up
        audio.close()
        background.close()
        final_video.close()
        
        return str(output_path)
        
    except Exception as e:
        print(f"Error creating basic video: {e}")
        raise Exception(f"Could not create video: {e}")


def create_simple_video(background_path, audio_path, output_dir):
    """
    Create a simpler version of the video without complex effects.
    Fallback function if the main video creation fails.
    
    Args:
        background_path (str): Path to the background image
        audio_path (str): Path to the audio file
        output_dir (Path): Directory to save the output video
        
    Returns:
        str: Path to the generated video file
    """
    try:
        # Load audio to get duration
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Create background video clip
        background = ImageClip(background_path, duration=duration)
        background = background.resized((1920, 1080))
        
        # Add audio to background
        final_video = background.with_audio(audio)
        
        # Export video with macOS-compatible settings
        output_path = output_dir / "output.mp4"
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            audio_bitrate='128k',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            ffmpeg_params=['-movflags', '+faststart', '-pix_fmt', 'yuv420p']
        )
        
        # Clean up
        audio.close()
        background.close()
        final_video.close()
        
        return str(output_path)
        
    except Exception as e:
        print(f"Error creating simple video: {e}")
        raise Exception(f"Could not create video: {e}")