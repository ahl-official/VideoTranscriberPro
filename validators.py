"""
Validators module for Video Transcriber Pro.
Contains all input validation functions.
"""

import os
from config import SUPPORTED_VIDEO_FORMATS, SUPPORTED_AUDIO_FORMATS


def validate_video_format(filepath):
    """
    Validate if file has a supported video or audio format.
    
    Args:
        filepath (str): Path to the video or audio file
        
    Returns:
        tuple: (is_valid: bool, file_extension: str, file_type: str)
               file_type is 'video' or 'audio'
    """
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext in SUPPORTED_VIDEO_FORMATS:
        return True, file_ext, 'video'
    elif file_ext in SUPPORTED_AUDIO_FORMATS:
        return True, file_ext, 'audio'
    else:
        return False, file_ext, None


def get_supported_formats_display():
    """
    Get formatted list of supported formats for display.
    
    Returns:
        str: Comma-separated supported formats
    """
    all_formats = SUPPORTED_VIDEO_FORMATS | SUPPORTED_AUDIO_FORMATS
    return ", ".join(sorted(all_formats))


def validate_api_key(api_key):
    """
    Validate API key input.
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        bool: True if API key is valid, False otherwise
    """
    api_key = api_key.strip()
    # Reject placeholder texts used in the UI
    invalid_placeholders = {"Paste your API key here", "Paste your new API key here"}
    is_valid = bool(api_key) and api_key not in invalid_placeholders
    return is_valid


def validate_file_exists(filepath):
    """
    Check if video file exists.
    
    Args:
        filepath (str): Path to the video file
        
    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.exists(filepath)


def get_file_size_mb(filepath):
    """
    Get file size in MB.
    
    Args:
        filepath (str): Path to the file
        
    Returns:
        float: File size in MB
    """
    if not os.path.exists(filepath):
        return 0
    return os.path.getsize(filepath) / (1024 * 1024)


def get_file_size_display(size_bytes):
    """
    Get human-readable file size.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string (e.g., "2.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def estimate_audio_size(video_size_bytes, bitrate_kbps=32):
    """
    Estimate compressed audio file size.
    
    Args:
        video_size_bytes (int): Video file size in bytes
        bitrate_kbps (int): Audio bitrate in kbps
        
    Returns:
        int: Estimated audio file size in bytes
    """
    # Rough estimate: audio is typically 5-10% of video size
    # Then apply bitrate compression
    return int((video_size_bytes * 0.07) * (bitrate_kbps / 128))


def should_compress_audio(filepath, file_ext):
    """
    Determine if audio file should be compressed based on format and size.
    
    Args:
        filepath (str): Path to the audio file
        file_ext (str): File extension (e.g., '.wav')
        
    Returns:
        tuple: (should_compress: bool, reason: str)
    """
    if not os.path.exists(filepath):
        return False, "File not found"
    
    file_size = os.path.getsize(filepath)
    
    # Uncompressed formats should always be considered for compression
    if file_ext in {'.wav', '.flac'}:
        return True, "Uncompressed format - compression recommended"
    
    # Already compressed formats - only compress if file is very large
    if file_size > 450 * 1024 * 1024:  # 450MB
        return True, "File size exceeds 450MB - compression needed"
    
    return False, "File is already optimized"
    
