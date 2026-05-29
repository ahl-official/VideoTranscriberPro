# Video Transcriber Pro

A Python GUI application that transcribes video files to text and generates SRT subtitle files using AssemblyAI's advanced speech-to-text API.

## Features

✨ **Core Functionality:**
- 🎬 Extract and compress audio from video files
- 🚀 Transcribe audio to text using AssemblyAI's Universal-3-Pro model
- 📝 Save transcriptions as plain text (.txt)
- 🎯 Generate SRT subtitle files (.srt)
- 🔄 Automatic retry system for failed uploads (3 attempts)
- ⏸️ Cancel transcription at any time

🛡️ **Input Validation:**
- Supports: MP4, MKV, MOV, AVI, FLV, WMV, WebM
- Validates video format before processing
- Checks for file existence before transcription

📂 **Smart File Organization:**
- Outputs saved to `Downloads/[video_name]/` folder
- Unique temp file naming to prevent conflicts
- Compressed audio, transcript, and subtitles in one folder

🔐 **Security:**
- No hardcoded API keys
- API key input via GUI
- Support for environment variables

## Project Structure

The application is organized into modular components for better maintainability:

```
YT_local/
├── main.py                 # Entry point - run this file
├── config.py              # Configuration and constants
├── ui.py                  # GUI components and UI logic
├── transcriber.py         # Transcription workflow logic
├── validators.py          # Input validation functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Module Descriptions

- **main.py** - Entry point of the application. Simply imports and runs the GUI.
- **config.py** - Centralized configuration including timeouts, retries, colors, fonts, paths.
- **ui.py** - Contains `TranscriberApp` class with all Tkinter GUI components and event handlers.
- **transcriber.py** - Contains `TranscriptionManager` class that handles the actual transcription workflow.
- **validators.py** - Reusable validation functions for video format, API key, and file checks.

## Installation

### For End Users / Employees
1. Go to the **[Releases Page](https://github.com/ahl-official/VideoTranscriberPro/releases/latest)**.
2. Download the `VideoTranscriberPro-Installer.exe` file.
3. Double-click the installer and follow the setup instructions.
4. Launch "Video Transcriber Pro" from your Desktop or Start Menu!

### For Developers (Build from Source)

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download this repository:**
   ```bash
   git clone <repository-url>
   cd YT_local
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your AssemblyAI API Key:**
   - Visit [AssemblyAI Dashboard](https://www.assemblyai.com/dashboard)
   - Sign up for a free account (if you don't have one)
   - Copy your API key from the dashboard

## Usage

### Running the Application

```bash
python main.py
```

### Step-by-Step Guide

1. **Enter API Key:**
   - Paste your AssemblyAI API key in the text field at the top
   - You can also set the `ASSEMBLYAI_API_KEY` environment variable to pre-populate it

2. **Select a Video:**
   - Click "📁 Browse Video" button
   - Choose your video file (MP4, MKV, MOV, AVI, FLV, WMV, or WebM)
   - Filename will appear below the button

3. **Start Transcription:**
   - Click "🚀 Start Transcription" button
   - Monitor progress through the status messages
   - Wait for completion (this may take several minutes depending on video length)

4. **Output Files:**
   - Files are automatically saved to: `Downloads/[video_name]/`
   - Three files will be created:
     - `[video_name]_compressed_audio.mp3` - Compressed audio (64kbps)
     - `[video_name]_transcript.txt` - Full transcription text
     - `[video_name]_subtitles.srt` - SRT subtitle file

5. **Cancel (Optional):**
   - Click "⛔ Cancel" to stop transcription at any time
   - Temporary files will be cleaned up

## Configuration

All configuration values are defined at the top of `app.py`:

```python
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv', '.webm'}
HTTP_TIMEOUT = 3600  # 1-hour timeout for huge files
MAX_RETRIES = 3      # Number of retry attempts
RETRY_DELAY = 5      # Seconds between retries
AUDIO_BITRATE = "64k" # Audio compression bitrate
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")
```

You can modify these values to customize the app's behavior.

## Environment Variables

Set the following environment variable to pre-populate your API key:

```bash
# Windows (PowerShell)
$env:ASSEMBLYAI_API_KEY = "your_api_key_here"

# Windows (CMD)
set ASSEMBLYAI_API_KEY=your_api_key_here

# Linux/Mac
export ASSEMBLYAI_API_KEY=your_api_key_here
```

## Supported Video Formats

- MP4 (.mp4)
- Matroska (.mkv)
- QuickTime (.mov)
- AVI (.avi)
- Flash Video (.flv)
- Windows Media (.wmv)
- WebM (.webm)

## Troubleshooting

### "Unsupported video format" Error
- Ensure your video file has one of the supported extensions
- Try converting your video to MP4 using a tool like FFmpeg

### "API Key Required" Error
- Make sure you've pasted your AssemblyAI API key in the text field
- Verify your API key is valid at the AssemblyAI dashboard

### Network Timeout
- The app will automatically retry up to 3 times
- Check your internet connection
- For very large files, increase `HTTP_TIMEOUT` in the code

### Files Not Being Created
- Check that your Downloads folder exists
- Ensure you have write permissions to your Downloads folder
- Verify the API key is valid and has available credits

### Temp Audio Files Not Cleaning Up
- If the app crashes, temp files may remain in your Downloads folder
- They're prefixed with `temp_compressed_audio_`
- Safe to delete manually

## Dependencies

- **assemblyai** - AssemblyAI API client
- **moviepy** - Video/audio processing
- **tkinter** - GUI (built-in with Python)

See `requirements.txt` for versions.

## Performance Tips

1. **For Large Files:**
   - Audio is compressed to 64kbps to reduce upload time
   - Expect transcription time proportional to video length

2. **For Better Accuracy:**
   - Ensure good audio quality in your source video
   - AssemblyAI's Universal-3-Pro model is optimized for various accents and backgrounds

3. **Batch Processing:**
   - Currently, the app handles one video at a time
   - Close the app and rerun it to process multiple videos

## License

This project is provided as-is for educational and personal use.

## Support

For issues with:
- **AssemblyAI API:** Visit [AssemblyAI Support](https://support.assemblyai.com)
- **This Application:** Check the troubleshooting section above

## API Costs

Please note that transcription usage is based on your AssemblyAI plan. Free tier includes a certain amount of minutes per month. Check your usage on the AssemblyAI dashboard to avoid unexpected charges.

---

Happy transcribing! 🎬✨
