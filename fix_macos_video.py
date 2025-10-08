#!/usr/bin/env python3
"""
Create a macOS-optimized version of the generated video.
This script creates a more compatible version for macOS playback.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def create_macos_compatible_video():
    """Create a macOS-compatible version of the video."""
    try:
        from moviepy import VideoFileClip
        
        input_path = Path("out/output.mp4")
        output_path = Path("out/output_macos.mp4")
        
        if not input_path.exists():
            print("No output.mp4 found. Please run 'python start.py' first.")
            return False
        
        print("Creating macOS-compatible video...")
        print("This may take a moment...")
        
        # Load the existing video
        video = VideoFileClip(str(input_path))
        
        # Re-export with maximum compatibility settings
        video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            audio_bitrate='128k',
            bitrate='2000k',
            temp_audiofile='temp-audio-macos.m4a',
            remove_temp=True,
            ffmpeg_params=[
                '-movflags', '+faststart',  # Optimize for streaming/quick preview
                '-pix_fmt', 'yuv420p',      # Ensure compatibility
                '-profile:v', 'baseline',   # Use baseline profile for maximum compatibility
                '-level', '3.0',            # Compatibility level
                '-preset', 'slow',          # Better compression
                '-crf', '23'                # Good quality
            ]
        )
        
        video.close()
        
        print(f"macOS-compatible video saved as: {output_path.name}")
        print("Try playing this version in Quick Look or Finder preview.")
        return True
        
    except Exception as e:
        print(f"Error creating macOS-compatible video: {e}")
        return False

def main():
    """Main function."""
    print("macOS Video Compatibility Tool")
    print("=" * 40)
    
    success = create_macos_compatible_video()
    
    if success:
        print("\nSUCCESS: Compatible video created!")
        print("Files in out/ directory:")
        output_dir = Path("out")
        for file in output_dir.glob("*.mp4"):
            print(f"  - {file.name}")
    else:
        print("\nFAILED: Could not create compatible video.")

if __name__ == "__main__":
    main()