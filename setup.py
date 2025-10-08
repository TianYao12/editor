#!/usr/bin/env python3
"""
Installation and setup script for Sleep Video Generator.
Checks dependencies and environment setup.
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("FAIL: Python 3.7 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"PASS: Python version: {sys.version.split()[0]}")
    return True


def check_pip():
    """Check if pip is available."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("PASS: pip is available")
        return True
    except subprocess.CalledProcessError:
        print("FAIL: pip is not available")
        return False


def install_requirements():
    """Install required packages from requirements.txt."""
    try:
        print("\nInstalling requirements...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("PASS: Requirements installed successfully")
            return True
        else:
            print(f"FAIL: Error installing requirements: {result.stderr}")
            return False
    except Exception as e:
        print(f"FAIL: Error installing requirements: {e}")
        return False


def check_env_file():
    """Check if .env file exists and contains OpenAI API key."""
    env_path = Path(".env")
    if not env_path.exists():
        print("FAIL: .env file not found")
        print("   Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        return False
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        if 'OPENAI_API_KEY=' in content and len(content.split('OPENAI_API_KEY=')[1].split('\n')[0].strip()) > 10:
            print("PASS: .env file found with OpenAI API key")
            return True
        else:
            print("FAIL: OpenAI API key not found in .env file")
            print("   Please add your OpenAI API key to .env:")
            print("   OPENAI_API_KEY=your_api_key_here")
            return False
    except Exception as e:
        print(f"FAIL: Error reading .env file: {e}")
        return False


def check_dependencies():
    """Check if all required dependencies are importable."""
    dependencies = [
        ("openai", "OpenAI API client"),
        ("moviepy", "MoviePy video editor"),
        ("PIL", "Pillow image processing"),
        ("dotenv", "python-dotenv"),
        ("requests", "HTTP requests library")
    ]
    
    all_good = True
    print("\nChecking dependencies...")
    
    for module, description in dependencies:
        try:
            if module == "PIL":
                import PIL
            elif module == "dotenv":
                import dotenv
            else:
                __import__(module)
            print(f"PASS: {description}")
        except ImportError:
            print(f"FAIL: {description} - not installed")
            all_good = False
    
    return all_good


def create_sample_files():
    """Create sample files if they don't exist."""
    script_file = Path("script.txt")
    if not script_file.exists():
        sample_content = """Welcome to this peaceful sleep journey. Take a deep breath and relax.

Let go of the day's tensions as you settle into comfort.

Imagine a tranquil place under starlit skies, where gentle sounds create perfect calm.

Allow your thoughts to drift away like evening clouds.

Your body grows heavy with relaxation as sleep approaches naturally.

Rest well and wake refreshed."""
        
        with open(script_file, 'w') as f:
            f.write(sample_content)
        print("PASS: Created script.txt")
    else:
        print("PASS: script.txt already exists")


def main():
    """Main setup function."""
    print("Sleep Video Generator - Setup Check")
    print("=" * 50)
    
    # Check basic requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("FAIL: requirements.txt not found")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\nWARNING: Failed to install some requirements. You may need to install them manually:")
        print("   pip install -r requirements.txt")
    
    # Check dependencies
    if not check_dependencies():
        print("\nWARNING: Some dependencies are missing. Try installing them manually:")
        print("   pip install openai moviepy pillow python-dotenv requests")
    
    # Check environment
    env_ok = check_env_file()
    
    # Create sample files
    print("\nSetting up sample files...")
    create_sample_files()
    
    # Final status
    print("\n" + "=" * 50)
    if env_ok:
        print("Setup complete! You can now run:")
        print("   python start.py")
    else:
        print("Setup almost complete!")
        print("   Please add your OpenAI API key to .env file, then run:")
        print("   python start.py")
    
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()