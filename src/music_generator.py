"""
Background music downloader for sleep videos.
Downloads free relaxing music from YouTube for background audio.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path


def check_existing_music(output_dir):
    """Check if background music already exists in the output directory."""
    music_extensions = ['.mp3', '.wav', '.m4a', '.aac']
    music_names = ['background_music', 'music', 'bgm']
    
    for name in music_names:
        for ext in music_extensions:
            music_path = output_dir / f"{name}{ext}"
            if music_path.exists():
                return str(music_path)
    
    return None


def generate_calming_music(duration, output_dir, music_type="ambient"):
    """
    Generate or provide calming background music.
    
    Args:
        duration (float): Duration of music needed in seconds
        output_dir (Path): Directory to save the music
        music_type (str): Type of music to generate
        
    Returns:
        str: Path to the music file or None for silence
    """
    if music_type == "silence":
        print("No background music selected")
        return None
    
    # First check if background music already exists
    existing_music = check_existing_music(output_dir)
    if existing_music:
        print(f"Using existing background music: {Path(existing_music).name}")
        return existing_music
    
    try:
        # Try to download from YouTube
        youtube_url = get_youtube_url_for_type(music_type)
        
        if youtube_url:
            print(f"Attempting to download {music_type} music from YouTube...")
            music_path = download_youtube_audio(youtube_url, output_dir, duration)
            
            if music_path and Path(music_path).exists():
                print(f"Downloaded background music: {Path(music_path).name}")
                return music_path
        
        # If download fails, create instructions for user
        print("YouTube download not available. Creating placeholder...")
        return create_music_placeholder(duration, output_dir, music_type)
            
    except Exception as e:
        print(f"Error getting background music: {e}")
        return create_music_placeholder(duration, output_dir, music_type)


def get_youtube_url_for_type(music_type):
    """Get YouTube URL for different music types from royalty-free sources."""
    
    # Curated list of royalty-free/Creative Commons relaxing music
    # These are long-form tracks perfect for background music
    music_urls = {
        "ambient": [
            "https://www.youtube.com/watch?v=jfKfPfyJRdk",  # Lofi Girl - 24/7 relaxing beats
            "https://www.youtube.com/watch?v=5qap5aO4i9A",  # ChilledCow - lofi hip hop
            "https://www.youtube.com/watch?v=DWcJFNfaw9c",  # Peaceful ambient music
        ],
        "nature": [
            "https://www.youtube.com/watch?v=eKFTSSKCzWA",  # 8 hours of rain sounds
            "https://www.youtube.com/watch?v=wzjWIxXBs_s",  # Forest sounds for sleep
            "https://www.youtube.com/watch?v=nDq6TstdEi8",  # Ocean waves 10 hours
        ],
        "meditation": [
            "https://www.youtube.com/watch?v=1ZYbU82GVz4",  # 6 hours meditation music
            "https://www.youtube.com/watch?v=IP2l7OaArNc",  # Zen meditation music
            "https://www.youtube.com/watch?v=kHnFzEa_5y8",  # Calming Buddhist music
        ],
        "piano": [
            "https://www.youtube.com/watch?v=jgpJVI3tDbY",  # 4 hours peaceful piano
            "https://www.youtube.com/watch?v=1SoqcMeRqbY",  # Sleep piano music 8 hours
            "https://www.youtube.com/watch?v=YQaV2EQIed8",  # Relaxing piano for sleep
        ],
        "space": [
            "https://www.youtube.com/watch?v=4-7IOZUG4qw",  # Deep space journey music
            "https://www.youtube.com/watch?v=K_YXUWCuKCQ",  # 8 hours space ambient
            "https://www.youtube.com/watch?v=1EqOZkw7rq8",  # Cosmic meditation sounds
        ]
    }
    
    # Return a random URL from the selected type
    import random
    if music_type in music_urls:
        return random.choice(music_urls[music_type])
    else:
        # Default to ambient if type not found
        return random.choice(music_urls["ambient"])
    
    # Free relaxing music URLs (Creative Commons or royalty-free)
    music_urls = {
        "ambient": "https://www.youtube.com/watch?v=1ZYbU82GVz4",  # 8 Hours Relaxing Music
        "nature": "https://www.youtube.com/watch?v=eKFTSSKCzWA",   # Nature Sounds
        "drone": "https://www.youtube.com/watch?v=wzjWIxXBs_s",    # Deep Meditation
        "bells": "https://www.youtube.com/watch?v=M4QJ_VwAOHk",    # Tibetan Bells
        "rain": "https://www.youtube.com/watch?v=mPZkdNFkNps",     # Rain Sounds
        "ocean": "https://www.youtube.com/watch?v=WHPEKLQID4U",    # Ocean Waves
        "forest": "https://www.youtube.com/watch?v=xNN7iTA57jM",   # Forest Sounds
        "silence": None
    }
    
    return music_urls.get(music_type, music_urls["ambient"])


def download_youtube_audio(url, output_dir, duration):
    """Download audio from YouTube using yt-dlp."""
    try:
        import sys
        
        # Use the same Python executable to run yt-dlp module
        python_exe = sys.executable
        
        # Check if yt-dlp is available as a module
        result = subprocess.run([python_exe, '-m', 'yt_dlp', '--version'], 
                              capture_output=True, timeout=10)
        if result.returncode != 0:
            print("yt-dlp not found. Please install with: pip install yt-dlp")
            return None
        
        # Create temporary directory for download
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Download command with yt-dlp using Python module
            cmd = [
                python_exe, '-m', 'yt_dlp',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', '192K',
                '--max-downloads', '1',
                '--no-playlist',
                '--output', str(temp_path / '%(title)s.%(ext)s'),
                url
            ]
            
            # Add duration limit for shorter clips
            if duration < 600:  # If less than 10 minutes
                cmd.extend(['--postprocessor-args', f'ffmpeg:-t {int(duration + 60)}'])
            
            print(f"Downloading from: {url}")
            
            # Run download with timeout
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                print(f"Download failed: {result.stderr}")
                return None
            
            # Find the downloaded file
            downloaded_files = list(temp_path.glob('*.mp3'))
            if not downloaded_files:
                print("No audio file found after download")
                return None
            
            # Move to output directory
            source_file = downloaded_files[0]
            output_file = output_dir / 'background_music.mp3'
            
            # Copy file to output directory
            shutil.copy2(source_file, output_file)
            
            print(f"Downloaded: {output_file.name}")
            return str(output_file)
            
    except subprocess.TimeoutExpired:
        print("Download timed out - using fallback")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def create_music_placeholder(duration, output_dir, music_type):
    """
    Create a placeholder with instructions for adding background music.
    
    Args:
        duration (float): Duration in seconds
        output_dir (Path): Output directory
        music_type (str): Type of music requested
        
    Returns:
        None: No music file created
    """
    # Create instructions file
    instructions_path = output_dir / "ADD_BACKGROUND_MUSIC.txt"
    
    music_suggestions = {
        "ambient": [
            "Search YouTube for: 'royalty free ambient music for meditation'",
            "Search YouTube for: 'creative commons lofi music'",
            "Try: 'peaceful ambient soundscape no copyright'"
        ],
        "nature": [
            "Search YouTube for: 'free rain sounds for sleep'", 
            "Search YouTube for: 'royalty free forest sounds'",
            "Try: 'ocean waves no copyright'"
        ],
        "meditation": [
            "Search YouTube for: 'free meditation music'",
            "Search YouTube for: 'royalty free zen music'", 
            "Try: 'tibetan singing bowls no copyright'"
        ],
        "piano": [
            "Search YouTube for: 'royalty free piano music peaceful'",
            "Search YouTube for: 'creative commons calm piano'",
            "Try: 'no copyright relaxing piano'"
        ],
        "space": [
            "Search YouTube for: 'royalty free space ambient'",
            "Search YouTube for: 'creative commons cosmic sounds'",
            "Try: 'no copyright deep space music'"
        ]
    }
    
    with open(instructions_path, 'w') as f:
        f.write("BACKGROUND MUSIC INSTRUCTIONS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"You requested: {music_type} music\n")
        f.write(f"Duration needed: {duration:.1f} seconds\n\n")
        f.write("TO ADD BACKGROUND MUSIC:\n")
        f.write("1. Download a royalty-free music file\n")
        f.write("2. Save it as 'background_music.mp3' in this folder\n")
        f.write("3. Run the video generator again\n\n")
        f.write("SUGGESTED SEARCHES:\n")
        
        suggestions = music_suggestions.get(music_type, music_suggestions["ambient"])
        for i, suggestion in enumerate(suggestions, 1):
            f.write(f"{i}. {suggestion}\n")
        
        f.write("\nNOTE: Make sure the music is labeled as:\n")
        f.write("- 'Royalty Free'\n")
        f.write("- 'Creative Commons'\n") 
        f.write("- 'No Copyright'\n")
        f.write("- 'Free to Use'\n\n")
        f.write("Popular royalty-free music channels:\n")
        f.write("- Audio Library — Music for content creators\n")
        f.write("- NoCopyrightSounds\n")
        f.write("- Chillhop Music\n")
        f.write("- Lofi Girl\n")
    
    print(f"Created music instructions: {instructions_path.name}")
    print("Add your own background music as 'background_music.mp3' in the out/ folder")
    
    return None


def create_silence_file(duration, output_dir):
    """
    Create a silent audio file as fallback.
    
    Args:
        duration (float): Duration in seconds
        output_dir (Path): Output directory
        
    Returns:
        str: Path to silence file
    """
    try:
        # Use ffmpeg to create silence if available
        output_path = output_dir / "background_music.mp3"
        
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100",
            "-t", str(duration),
            "-c:a", "mp3",
            "-b:a", "128k",
            "-y",  # Overwrite output file
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and output_path.exists():
            print(f"Created silence file ({duration:.1f}s)")
            return str(output_path)
            
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    
    # Fallback: no music file
    print("No background music - video will have voiceover only")
    return None


def get_music_types():
    """Get available music types."""
    return {
        "ambient": "Lofi and ambient background music",
        "nature": "Nature sounds (rain, forest, ocean)", 
        "meditation": "Calm meditation and zen music",
        "piano": "Peaceful piano melodies",
        "space": "Deep space and cosmic ambient sounds",
        "silence": "No background music"
    }
def check_yt_dlp_available():
    """Check if yt-dlp is available."""
    try:
        result = subprocess.run(["yt-dlp", "--version"], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False


def install_yt_dlp():
    """Attempt to install yt-dlp."""
    try:
        import sys
        result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                              capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except Exception:
        return False