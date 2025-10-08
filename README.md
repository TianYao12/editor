# Sleep Video Generator

A Python CLI tool that creates YouTube-ready sleep and relaxation videos using OpenAI's TTS and image generation APIs, combined with MoviePy for video creation.

## Features

- **AI-Powered Narration**: Uses OpenAI's TTS API to generate calm, natural-sounding voiceovers
- **Custom Background Images**: Generates beautiful, calming background images using OpenAI's DALL-E
- **Professional Video Creation**: Creates 1920x1080 videos with fade effects and text overlays
- **YouTube Thumbnail Generation**: Creates eye-catching 1280x720 thumbnails for your videos
- **Metadata Management**: Saves all video information and metadata for easy YouTube uploading
- **Interactive CLI**: Guides you through the entire process step-by-step

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**:
   - Ensure your `.env` file contains your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Create your script**:
   - Put your content in `script.txt` (in the project directory)

4. **Run the Generator**:
   ```bash
   python start.py
   ```

5. **Follow the Interactive Prompts**:
   - Describe the visual theme for your background
   - Review and approve the generated video
   - Add YouTube metadata
   - Generate thumbnails

## Project Structure

```
clipper/
├── start.py                 # Main CLI entry point
├── requirements.txt         # Python dependencies
├── script.txt              # Your script content (required)
├── .env                    # Environment variables (OpenAI API key)
├── client_secret.json      # YouTube API credentials
├── src/                    # Source modules
│   ├── __init__.py
│   ├── utils.py            # Utility functions
│   ├── background_generator.py    # Background image generation
│   ├── tts_generator.py    # Text-to-speech generation
│   ├── video_creator.py    # Video creation and editing
│   ├── thumbnail_generator.py     # YouTube thumbnail generation
│   └── metadata_handler.py        # Metadata management
└── out/                    # Generated files (created automatically)
    ├── background.png      # Generated background image
    ├── voiceover.mp3       # Generated audio narration
    ├── output.mp4          # Final video file
    ├── thumbnail_1.png     # Generated thumbnail
    └── metadata.json       # Video metadata
```

## Module Documentation

### src/utils.py
- **Purpose**: Common utility functions used across the application
- **Key Functions**:
  - `create_output_folder()`: Creates the output directory
  - `open_video()`: Opens video with system default player
  - `validate_openai_key()`: Validates OpenAI API key availability

### src/background_generator.py
- **Purpose**: Generates background images using OpenAI's DALL-E API
- **Key Functions**:
  - `generate_background()`: Creates 1920x1080 background images
  - `create_fallback_background()`: Creates simple gradient background if API fails

### src/tts_generator.py
- **Purpose**: Converts text to speech using OpenAI's TTS API
- **Key Functions**:
  - `generate_tts()`: Converts script text to natural-sounding narration
  - `generate_tts_with_voice()`: Allows voice selection for TTS

### src/video_creator.py
- **Purpose**: Creates the final video using MoviePy
- **Key Functions**:
  - `create_video()`: Combines background, audio, and effects into final video
  - Implements fade-to-black effect and text overlays

### src/thumbnail_generator.py
- **Purpose**: Generates YouTube thumbnails using OpenAI's image generation
- **Key Functions**:
  - `generate_thumbnail()`: Creates 1280x720 YouTube thumbnails
  - `create_fallback_thumbnail()`: Creates simple text-based thumbnails

### src/metadata_handler.py
- **Purpose**: Manages video metadata and YouTube information
- **Key Functions**:
  - `save_metadata()`: Saves all video information to JSON
  - `create_youtube_description_template()`: Creates formatted descriptions

## Usage Example

```bash
$ python start.py

Welcome to the Sleep Video Generator.
This tool will turn your script into a YouTube-ready video with AI voiceover and background.

Loaded 889 characters from script.txt.

Describe the visual theme for your video background: peaceful starry night sky with gentle waves
Generating background image...
Background image generated and saved as background.png.

Generating voiceover...
Voiceover generated and saved as voiceover.mp3.

Creating video...
Video exported successfully to output.mp4.

Would you like to view the video now? (y/n): y
Opening output.mp4 with default media player...

Enter a YouTube title for your video: Peaceful Sleep Journey - Starry Night Relaxation
Enter a YouTube description (press Enter twice to finish):
A calming sleep meditation to help you drift off peacefully.

Would you like to generate a YouTube thumbnail? (y/n): y
Describe your desired thumbnail: calm night sky with soft glowing stars and relaxing text
Generating thumbnail...
Thumbnail saved as thumbnail_1.png.
Do you like it? (accept / regenerate / edit prompt): accept

Video generation complete.
Video: output.mp4
Voiceover: voiceover.mp3
Background: background.png
Thumbnail: thumbnail_1.png
Title and description saved to metadata.json.
Ready for YouTube upload.
```

## Configuration

### OpenAI API Key
Make sure your `.env` file contains your OpenAI API key:
```
OPENAI_API_KEY=sk-proj-your-api-key-here
```

### YouTube API (Optional)
The `client_secret.json` file is included for future YouTube upload functionality.

## Requirements

- Python 3.7+
- OpenAI API key with credits
- FFmpeg (usually installed automatically with MoviePy)

## Dependencies

- `openai>=1.0.0` - OpenAI API client
- `moviepy>=1.0.3` - Video editing and creation
- `pillow>=9.0.0` - Image processing
- `python-dotenv>=1.0.0` - Environment variable management
- `requests>=2.28.0` - HTTP requests for image downloads

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure all dependencies are installed with `pip install -r requirements.txt`

2. **OpenAI API Error**: Verify your API key is correct and you have sufficient credits

3. **FFmpeg Error**: MoviePy requires FFmpeg. It usually installs automatically, but you may need to install it manually on some systems

4. **Font Errors**: The thumbnail generator tries to use system fonts. Fallback fonts are used if system fonts aren't available

### Performance Tips

- Use shorter scripts for faster processing
- The video creation process can take several minutes for longer content
- Background image generation may take 10-30 seconds depending on OpenAI API response time

## Future Enhancements

- Direct YouTube upload integration
- Multiple voice options selection
- Custom video effects and transitions
- Batch processing for multiple scripts
- Advanced thumbnail customization
- Background music integration