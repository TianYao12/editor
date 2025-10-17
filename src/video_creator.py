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
    ColorClip,
    CompositeAudioClip,
    concatenate_audioclips
)
from src.music_generator import generate_calming_music


def create_video(background_path, audio_path, output_dir, music_type="ambient"):
    """
    Create a sleep video with background image, voiceover, and background music.
    
    Args:
        background_path (str): Path to the background image
        audio_path (str): Path to the audio file
        output_dir (Path): Directory to save the output video
        music_type (str): Type of background music to generate
        
    Returns:
        str: Path to the generated video file
    """
    try:
        # Use enhanced video creation with music
        return create_video_with_music(background_path, audio_path, output_dir, music_type)
        
    except Exception as e:
        print(f"Error creating video with music: {e}")
        print("Falling back to video without background music...")
        # Try simple video creation without music
        try:
            return create_simple_video(background_path, audio_path, output_dir)
        except Exception as e2:
            print(f"Error creating simple video: {e2}")
            # Try even simpler approach
            try:
                return create_basic_video(background_path, audio_path, output_dir)
            except Exception as e3:
                print(f"Error creating basic video: {e3}")
                raise Exception(f"Could not create video: {e3}")


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


def create_video_with_music(background_path, audio_path, output_dir, music_type="ambient"):
    """
    Create a video with background image, voiceover, and background music.
    
    Args:
        background_path (str): Path to the background image
        audio_path (str): Path to the audio file
        output_dir (Path): Directory to save the output video
        music_type (str): Type of background music to generate
        
    Returns:
        str: Path to the generated video file
    """
    try:
        # Load voiceover audio to get duration
        voiceover = AudioFileClip(audio_path)
        duration = voiceover.duration
        
        print("Generating background music...")
        # Generate background music
        music_path = generate_calming_music(duration, output_dir, music_type)
        
        if music_path and Path(music_path).exists():
            # Load background music
            background_music = AudioFileClip(music_path)
            
            # Use background music (adjust if needed)
            if background_music.duration > duration:
                # If music is longer, trim it
                background_music = background_music.subclip(0, duration)
            elif background_music.duration < duration:
                # If music is shorter, that's ok - it will just be shorter
                print(f"Background music ({background_music.duration:.1f}s) is shorter than voiceover ({duration:.1f}s)")
            
            # Mix voiceover with background music (voiceover louder)
            voiceover_volume = 1.0
            music_volume = 0.25  # Background music at 25% volume
            
            # Adjust volumes
            voiceover = voiceover.with_volume_scaled(voiceover_volume)
            background_music = background_music.with_volume_scaled(music_volume)
            
            # Composite the audio tracks
            final_audio = CompositeAudioClip([voiceover, background_music])
            
            print(f"Mixed voiceover with {music_type} background music")
        else:
            # No background music, use voiceover only
            final_audio = voiceover
            print("Using voiceover only (no background music)")
        
        # Create background video clip
        background = ImageClip(background_path, duration=duration)
        background = background.resized((1920, 1080))
        
        # Add mixed audio to background
        final_video = background.with_audio(final_audio)
        
        # Export video with enhanced settings
        output_path = output_dir / "output.mp4"
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            audio_bitrate='192k',  # Higher quality audio
            bitrate='2000k',      # Higher quality video
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Clean up
        voiceover.close()
        if 'background_music' in locals():
            background_music.close()
        final_audio.close()
        background.close()
        final_video.close()
        
        return str(output_path)
        
    except Exception as e:
        print(f"Error creating video with music: {e}")
        raise Exception(f"Could not create video with music: {e}")


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