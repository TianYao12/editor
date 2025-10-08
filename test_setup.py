#!/usr/bin/env python3
"""
Quick test script to verify the Sleep Video Generator setup.
Tests basic functionality without generating full videos.
"""

import os
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test if all modules can be imported."""
    print("Testing module imports...")
    
    try:
        from src import utils, background_generator, tts_generator
        from src import video_creator, thumbnail_generator, metadata_handler
        print("PASS: All modules imported successfully")
        return True
    except ImportError as e:
        print(f"FAIL: Import error: {e}")
        return False


def test_environment():
    """Test environment setup."""
    print("\nTesting environment...")
    
    # Test .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and len(api_key) > 10:
        print("PASS: OpenAI API key found")
        return True
    else:
        print("FAIL: OpenAI API key not found or invalid")
        return False


def test_dependencies():
    """Test external dependencies."""
    print("\nTesting external dependencies...")
    
    try:
        import openai
        print("PASS: OpenAI library available")
    except ImportError:
        print("FAIL: OpenAI library not available")
        return False
    
    try:
        import moviepy
        print("PASS: MoviePy library available")
    except ImportError:
        print("FAIL: MoviePy library not available")
        return False
    
    try:
        from PIL import Image
        print("PASS: Pillow (PIL) library available")
    except ImportError:
        print("FAIL: Pillow (PIL) library not available")
        return False
    
    return True


def test_output_directory():
    """Test output directory creation."""
    print("\nTesting output directory creation...")
    
    try:
        from src.utils import create_output_folder
        output_dir = create_output_folder()
        if output_dir.exists():
            print("PASS: Output directory created successfully")
            return True
        else:
            print("FAIL: Failed to create output directory")
            return False
    except Exception as e:
        print(f"FAIL: Error creating output directory: {e}")
        return False


def test_sample_script():
    """Test sample script file."""
    print("\nTesting script.txt file...")
    
    script_path = Path("script.txt")
    if script_path.exists():
        try:
            with open(script_path, 'r') as f:
                content = f.read()
            if len(content.strip()) > 0:
                print(f"PASS: script.txt found ({len(content)} characters)")
                return True
            else:
                print("FAIL: script.txt is empty")
                return False
        except Exception as e:
            print(f"FAIL: Error reading script.txt: {e}")
            return False
    else:
        print("FAIL: script.txt not found")
        return False


def main():
    """Run all tests."""
    print("Sleep Video Generator - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_environment,
        test_dependencies,
        test_output_directory,
        test_sample_script
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The system is ready to use.")
        print("\nYou can now run: python start.py")
    else:
        print(f"{total - passed} tests failed. Please check the setup.")
        print("\nTry running: python setup.py")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)