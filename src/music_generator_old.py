"""
Background music downloader for sleep videos.
Downloads free relaxing music from YouTube for background audio.
"""

import os
import subprocess
import tempfile
from pathlib import Path
import json


def generate_calming_music(duration, output_dir, music_type="ambient"):
    """
    Generate calming background music for sleep videos.
    
    Args:
        duration (float): Duration of music in seconds
        output_dir (Path): Directory to save the generated music
        music_type (str): Type of music to generate
        
    Returns:
        str: Path to the generated music file
    """
    try:
        # Try different music generation approaches
        music_path = None
        
        # First try to generate with scipy/numpy
        music_path = generate_synthetic_ambient(duration, output_dir, music_type)
        
        if music_path:
            return music_path
        else:
            # Fallback to creating silence (user can add their own music later)
            return generate_silence(duration, output_dir)
            
    except Exception as e:
        print(f"Error generating music: {e}")
        # Create silence as fallback
        return generate_silence(duration, output_dir)


def generate_synthetic_ambient(duration, output_dir, music_type):
    """Generate synthetic ambient music using numpy and scipy."""
    try:
        import scipy.io.wavfile as wavfile
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        
        # Generate different types of calming sounds
        if music_type == "nature":
            audio = generate_nature_sounds(samples, sample_rate)
        elif music_type == "drone":
            audio = generate_ambient_drone(samples, sample_rate)
        elif music_type == "bells":
            audio = generate_soft_bells(samples, sample_rate)
        else:  # ambient
            audio = generate_ambient_mix(samples, sample_rate)
        
        # Normalize audio
        audio = np.clip(audio, -1.0, 1.0)
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Save as WAV file
        music_path = output_dir / "background_music.wav"
        wavfile.write(str(music_path), sample_rate, audio_int16)
        
        print(f"Generated {music_type} background music ({duration:.1f}s)")
        return str(music_path)
        
    except ImportError:
        print("scipy not available for music generation")
        return None
    except Exception as e:
        print(f"Error in synthetic music generation: {e}")
        return None


def generate_nature_sounds(samples, sample_rate):
    """Generate nature-like ambient sounds."""
    t = np.linspace(0, samples / sample_rate, samples, False)
    
    # Create layered nature sounds
    # Gentle wind-like noise
    wind = np.random.normal(0, 0.1, samples)
    wind = apply_lowpass_filter(wind, 800, sample_rate)
    
    # Soft water-like sounds
    water = np.random.normal(0, 0.05, samples)
    water = apply_lowpass_filter(water, 400, sample_rate)
    
    # Very subtle bird-like tones
    birds = 0
    for freq in [220, 330, 440]:
        phase = np.random.random() * 2 * np.pi
        envelope = np.sin(2 * np.pi * 0.1 * t + phase) * 0.02
        envelope = np.maximum(0, envelope)
        birds += np.sin(2 * np.pi * freq * t + phase) * envelope
    
    # Combine with different weights
    audio = wind * 0.6 + water * 0.3 + birds * 0.1
    
    # Apply gentle fade in/out
    audio = apply_fade(audio, sample_rate)
    
    return audio


def generate_ambient_drone(samples, sample_rate):
    """Generate ambient drone music."""
    t = np.linspace(0, samples / sample_rate, samples, False)
    
    # Create harmonic drone
    fundamentals = [55, 82.5, 110]  # Low frequencies
    audio = np.zeros(samples)
    
    for i, freq in enumerate(fundamentals):
        # Add fundamental and harmonics
        for harmonic in range(1, 4):
            amplitude = 0.3 / harmonic * (0.8 ** i)
            phase = np.random.random() * 2 * np.pi
            
            # Slight frequency modulation for organic feel
            freq_mod = freq * harmonic * (1 + 0.001 * np.sin(2 * np.pi * 0.1 * t))
            audio += amplitude * np.sin(2 * np.pi * freq_mod * t + phase)
    
    # Add subtle noise texture
    texture = np.random.normal(0, 0.02, samples)
    texture = apply_lowpass_filter(texture, 1000, sample_rate)
    audio += texture
    
    # Apply gentle fade in/out
    audio = apply_fade(audio, sample_rate)
    
    return audio


def generate_soft_bells(samples, sample_rate):
    """Generate soft bell-like tones."""
    t = np.linspace(0, samples / sample_rate, samples, False)
    audio = np.zeros(samples)
    
    # Bell frequencies (pentatonic scale)
    bell_freqs = [220, 247, 294, 330, 392]
    
    # Generate random bell strikes throughout the duration
    num_bells = int(samples / sample_rate / 8)  # One bell every 8 seconds average
    
    for _ in range(num_bells):
        bell_time = np.random.random() * samples / sample_rate
        bell_freq = np.random.choice(bell_freqs)
        
        # Create bell envelope (exponential decay)
        bell_start = int(bell_time * sample_rate)
        bell_duration = int(4 * sample_rate)  # 4 second decay
        
        if bell_start + bell_duration < samples:
            bell_t = np.arange(bell_duration) / sample_rate
            envelope = np.exp(-bell_t * 0.5)  # Exponential decay
            
            # Bell harmonics
            bell_tone = (np.sin(2 * np.pi * bell_freq * bell_t) * 0.6 +
                        np.sin(2 * np.pi * bell_freq * 2 * bell_t) * 0.3 +
                        np.sin(2 * np.pi * bell_freq * 3 * bell_t) * 0.1)
            
            bell_sound = bell_tone * envelope * 0.2
            audio[bell_start:bell_start + bell_duration] += bell_sound
    
    # Add subtle ambient pad
    for freq in [110, 165, 220]:
        amplitude = 0.05
        audio += amplitude * np.sin(2 * np.pi * freq * t)
    
    # Apply gentle fade in/out
    audio = apply_fade(audio, sample_rate)
    
    return audio


def generate_ambient_mix(samples, sample_rate):
    """Generate mixed ambient soundscape."""
    # Combine different elements
    nature = generate_nature_sounds(samples, sample_rate) * 0.4
    drone = generate_ambient_drone(samples, sample_rate) * 0.3
    bells = generate_soft_bells(samples, sample_rate) * 0.3
    
    return nature + drone + bells


def apply_lowpass_filter(audio, cutoff_freq, sample_rate):
    """Apply simple lowpass filter."""
    try:
        from scipy.signal import butter, filtfilt
        nyquist = sample_rate / 2
        normal_cutoff = cutoff_freq / nyquist
        b, a = butter(2, normal_cutoff, btype='low', analog=False)
        return filtfilt(b, a, audio)
    except ImportError:
        # Simple approximation without scipy
        alpha = cutoff_freq / (cutoff_freq + sample_rate)
        filtered = np.zeros_like(audio)
        filtered[0] = audio[0]
        for i in range(1, len(audio)):
            filtered[i] = alpha * audio[i] + (1 - alpha) * filtered[i-1]
        return filtered


def apply_fade(audio, sample_rate, fade_duration=2.0):
    """Apply fade in and fade out."""
    fade_samples = int(fade_duration * sample_rate)
    
    # Fade in
    if len(audio) > fade_samples:
        fade_in = np.linspace(0, 1, fade_samples)
        audio[:fade_samples] *= fade_in
    
    # Fade out
    if len(audio) > fade_samples:
        fade_out = np.linspace(1, 0, fade_samples)
        audio[-fade_samples:] *= fade_out
    
    return audio


def generate_silence(duration, output_dir):
    """Generate silence as fallback."""
    try:
        import scipy.io.wavfile as wavfile
        
        sample_rate = 44100
        samples = int(duration * sample_rate)
        silence = np.zeros(samples, dtype=np.int16)
        
        music_path = output_dir / "background_music.wav"
        wavfile.write(str(music_path), sample_rate, silence)
        
        print(f"Generated silence track ({duration:.1f}s) - you can replace with your own music")
        return str(music_path)
        
    except ImportError:
        # Create empty file as placeholder
        music_path = output_dir / "background_music.txt"
        with open(music_path, 'w') as f:
            f.write("Add your own background music file here\n")
        print("Created placeholder for background music")
        return None


def get_music_types():
    """Get available music types."""
    return {
        "ambient": "Mixed ambient soundscape with nature and drone elements",
        "nature": "Nature sounds with wind and water",
        "drone": "Deep harmonic drone tones",
        "bells": "Soft bell tones with ambient pad",
        "silence": "Silent track (add your own music later)"
    }