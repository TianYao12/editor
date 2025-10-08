# Sleep Video Generator - Usage Guide

## Quick Start

1. Make sure `script.txt` contains your sleep script content
2. Run: `python start.py`
3. Follow the prompts to create your video

## What the System Does

The Sleep Video Generator automatically:

1. **Reads script.txt** - No need to specify a file path
2. **Generates background image** - AI-created based on your description
3. **Creates voiceover** - Natural-sounding narration from your script
4. **Builds video** - Professional 1920x1080 video with audio
5. **Generates thumbnail** - YouTube-ready thumbnail (optional)
6. **Saves metadata** - All information for YouTube upload

## Output Files

All files are saved in the `out/` directory:

- `background.png` - Generated background image
- `voiceover.mp3` - AI-generated narration
- `output.mp4` - Final video file (YouTube-ready)
- `thumbnail_1.png` - YouTube thumbnail (if generated)
- `metadata.json` - Video metadata and information

## System Requirements

- Python 3.7+
- OpenAI API key (in .env file)
- Internet connection for API calls
- About 1-5 minutes processing time per video

## Workflow

1. **Start**: `python start.py`
2. **Background prompt**: Describe your desired background theme
3. **Processing**: System generates background, voiceover, and video
4. **Review**: Option to preview the generated video
5. **Metadata**: Enter YouTube title and description
6. **Thumbnail**: Optional thumbnail generation with retry options
7. **Complete**: All files ready for YouTube upload

## Example Session

```
$ python start.py

Welcome to the Sleep Video Generator.
This tool will turn your script into a YouTube-ready video with AI voiceover and background.

Loaded 889 characters from script.txt.

Describe the visual theme for your video background: peaceful starry night sky
Generating background image...
Background image generated and saved as background.png.

Generating voiceover...
Voiceover generated and saved as voiceover.mp3.

Creating video...
Video exported successfully to output.mp4.

Would you like to view the video now? (y/n): n

Enter a YouTube title for your video: Peaceful Sleep Journey
Enter a YouTube description (press Enter twice to finish):
A calming sleep meditation under the stars.
Perfect for bedtime relaxation.

Would you like to generate a YouTube thumbnail? (y/n): y
Describe your desired thumbnail: starry night with peaceful sleep text
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

## Tips

- Keep your script.txt content between 1-10 minutes when read aloud
- Use descriptive background prompts for better AI-generated images
- The system automatically creates calm, sleep-appropriate content
- All files are organized and ready for immediate YouTube upload
- Check the `metadata.json` file for complete video information

## Testing

- Run `python test_setup.py` to verify system setup
- Run `python demo.py` for a quick demonstration
- Check that `script.txt` exists and contains your content

The system is now fully operational and emoji-free!