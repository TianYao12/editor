#!/usr/bin/env python3
"""
Video audio checker - verifies that generated videos have audio tracks.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_video_audio(video_path):
    """Check if a video file has audio."""
    try:
        from moviepy import VideoFileClip
        
        video = VideoFileClip(video_path)
        has_audio = video.audio is not None
        
        print(f"Video: {Path(video_path).name}")
        print(f"Duration: {video.duration:.2f} seconds")
        print(f"Has audio: {'YES' if has_audio else 'NO'}")
        
        if has_audio:
            print(f"Audio duration: {video.audio.duration:.2f} seconds")
            print(f"Audio sample rate: {video.audio.fps} Hz")
            
        video.close()
        return has_audio
        
    except Exception as e:
        print(f"Error checking video: {e}")
        return False

def main():
    """Check audio in generated video."""
    output_dir = Path("out")
    video_path = output_dir / "output.mp4"
    
    if not video_path.exists():
        print("No output.mp4 found in out/ directory.")
        print("Please run 'python start.py' first to generate a video.")
        return
    
    print("Checking video audio...")
    print("=" * 40)
    
    has_audio = check_video_audio(str(video_path))
    
    print("=" * 40)
    if has_audio:
        print("SUCCESS: Video has audio track!")
        print("The video should play with sound in media players.")
    else:
        print("WARNING: Video has no audio track!")
        print("This indicates an issue with video generation.")

if __name__ == "__main__":
    main()