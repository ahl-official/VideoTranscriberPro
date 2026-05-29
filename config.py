"""
Configuration module for Video Transcriber Pro.
Contains all global settings and constants.
"""

from pathlib import Path

# ==========================================
# VIDEO & AUDIO CONFIGURATION
# ==========================================
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv', '.webm'}
SUPPORTED_AUDIO_FORMATS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma'}
ALL_SUPPORTED_FORMATS = SUPPORTED_VIDEO_FORMATS | SUPPORTED_AUDIO_FORMATS

# Audio bitrate options for user selection
AUDIO_BITRATE_OPTIONS = [
    ("64 kbps - Best Quality (Slow)", "64k"),
    ("48 kbps - Good Quality (Medium)", "48k"),
    ("32 kbps - Balanced (Fast)", "32k"),
]
AUDIO_BITRATE_DEFAULT = "32k"  # Default selection

# ==========================================
# API CONFIGURATION
# ==========================================
HTTP_TIMEOUT_DEFAULT = 3600  # 1-hour timeout
HTTP_TIMEOUT_LARGE_FILE = 7200  # 2-hour timeout for files > 500MB
HTTP_TIMEOUT_VERY_LARGE = 14400  # 4-hour timeout for files > 1GB
SPEECH_MODELS = ["universal-3-pro", "universal-2"]

# ==========================================
# LARGE FILE HANDLING
# ==========================================
CHUNK_SIZE = 50 * 1024 * 1024  # 50MB chunks for upload
FILE_SIZE_WARNING = 500 * 1024 * 1024  # 500MB - show warning
FILE_SIZE_LARGE = 1 * 1024 * 1024 * 1024  # 1GB - use extended timeout
MIN_BITRATE = "16k"  # Minimum bitrate for very large files

# Audio compression settings
AUDIO_NEEDS_COMPRESSION_THRESHOLD = 450 * 1024 * 1024  # 450MB - AssemblyAI limit
UNCOMPRESSED_FORMATS = {'.wav', '.flac'}  # Formats that should usually be compressed
ALREADY_COMPRESSED_FORMATS = {'.mp3', '.aac', '.m4a', '.ogg', '.wma'}  # Already compressed

# ==========================================
# RETRY CONFIGURATION
# ==========================================
MAX_RETRIES = 5  # Increased for large files
RETRY_DELAY = 5  # seconds
RETRY_BACKOFF = 1.5  # Exponential backoff multiplier

# ==========================================
# FILE PATHS
# ==========================================
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")

# ==========================================
# UI CONFIGURATION
# ==========================================
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 450
WINDOW_TITLE = "Video Transcriber Pro"

# Font configurations
TITLE_FONT = ("Arial", 16, "bold")
LABEL_FONT = ("Arial", 10)
BUTTON_FONT = ("Arial", 11)
BUTTON_BOLD_FONT = ("Arial", 11, "bold")

# Colors
COLOR_BROWSE_BTN = "#e0e0e0"
COLOR_START_BTN = "#4CAF50"
COLOR_CANCEL_BTN = "#f44336"
TEXT_WHITE = "white"
TEXT_BLACK = "black"
TEXT_GRAY = "gray"
TEXT_RED = "red"
