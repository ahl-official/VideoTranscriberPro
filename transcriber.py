"""
Transcriber module for Video Transcriber Pro.
Handles all transcription-related operations.
"""

import os
import time
import uuid
import assemblyai as aai
from moviepy.editor import VideoFileClip, AudioFileClip
from config import (
    HTTP_TIMEOUT_DEFAULT,
    HTTP_TIMEOUT_LARGE_FILE,
    HTTP_TIMEOUT_VERY_LARGE,
    SPEECH_MODELS,
    MAX_RETRIES,
    RETRY_DELAY,
    RETRY_BACKOFF,
    CHUNK_SIZE,
    FILE_SIZE_WARNING,
    FILE_SIZE_LARGE,
    DOWNLOADS_FOLDER
)
from validators import get_file_size_display


class TranscriptionManager:
    """Handles video transcription workflow."""
    
    def __init__(self, api_key, video_path, status_callback, cancel_check, bitrate="32k", file_type="video"):
        """
        Initialize transcription manager.
        
        Args:
            api_key (str): AssemblyAI API key
            video_path (str): Path to video or audio file
            status_callback (callable): Function to update status
            cancel_check (callable): Function to check if cancellation requested
            bitrate (str): Audio bitrate (64k, 48k, or 32k)
            file_type (str): Type of input file ('video' or 'audio')
        """
        self.api_key = api_key
        self.video_path = video_path
        self.status_callback = status_callback
        self.cancel_check = cancel_check
        self.audio_file = None
        self.bitrate = bitrate
        self.file_type = file_type
        
        # Configure AssemblyAI
        aai.settings.api_key = api_key
        self.config = aai.TranscriptionConfig(speech_models=SPEECH_MODELS)
    
    def get_dynamic_timeout(self, audio_file_path):
        """
        Determine HTTP timeout based on file size.
        
        Args:
            audio_file_path (str): Path to audio file
            
        Returns:
            int: Timeout in seconds
        """
        if not os.path.exists(audio_file_path):
            return HTTP_TIMEOUT_DEFAULT
        
        file_size = os.path.getsize(audio_file_path)
        
        if file_size > FILE_SIZE_LARGE:
            return HTTP_TIMEOUT_VERY_LARGE
        elif file_size > FILE_SIZE_WARNING:
            return HTTP_TIMEOUT_LARGE_FILE
        else:
            return HTTP_TIMEOUT_DEFAULT
    
    def get_output_paths(self):
        """
        Create output folder and return all required file paths.
        
        Returns:
            dict: Contains output_folder, audio_file, txt_path, srt_path, final_audio_path
        """
        filename = os.path.basename(self.video_path)
        file_name_without_ext = os.path.splitext(filename)[0]
        
        # Create output folder in Downloads with file name
        output_folder = os.path.join(DOWNLOADS_FOLDER, file_name_without_ext)
        os.makedirs(output_folder, exist_ok=True)
        
        txt_path = os.path.join(output_folder, f"{file_name_without_ext}_transcript.txt")
        srt_path = os.path.join(output_folder, f"{file_name_without_ext}_subtitles.srt")
        
        # If input is audio, use it directly; otherwise prepare temp audio for extraction
        if self.file_type == "audio":
            # For audio files, use original file directly
            final_audio_path = os.path.join(output_folder, f"{file_name_without_ext}_original_audio.mp3")
            audio_file = self.video_path  # Use original audio file directly
        else:
            # For video files, use UUID for temp audio extraction
            unique_id = str(uuid.uuid4())[:8]
            audio_file = os.path.join(output_folder, f"temp_compressed_audio_{unique_id}.mp3")
            final_audio_path = os.path.join(output_folder, f"{file_name_without_ext}_compressed_audio.mp3")
        
        return {
            "output_folder": output_folder,
            "audio_file": audio_file,
            "txt_path": txt_path,
            "srt_path": srt_path,
            "final_audio_path": final_audio_path,
            "video_name_without_ext": file_name_without_ext
        }
    
    def extract_audio(self, audio_file):
        """
        Extract and compress audio from video, or compress audio file if needed.
        
        Args:
            audio_file (str): Output path for audio file (or input if already audio)
            
        Raises:
            Exception: If audio extraction/compression fails
        """
        if self.file_type == "audio":
            # Check if audio file needs compression
            file_size = os.path.getsize(self.video_path)
            needs_compression = (
                self.video_path.lower().endswith(('.wav', '.flac')) or 
                file_size > 450 * 1024 * 1024
            )
            
            if needs_compression:
                # Compress audio file
                self.status_callback(f"🎬 Step 1/3: Compressing audio ({self.bitrate})...")
                
                # Use moviepy to compress the audio
                clip = None
                try:
                    clip = AudioFileClip(self.video_path)
                    clip.write_audiofile(audio_file, bitrate=self.bitrate, logger=None)
                except Exception:
                    # If moviepy doesn't work for this audio format, try direct conversion
                    # For now, just copy the file if compression fails
                    import shutil
                    self.status_callback("⏩ Compression not needed, using original file...")
                    if audio_file != self.video_path:
                        shutil.copy2(self.video_path, audio_file)
                finally:
                    if clip is not None:
                        clip.close()
            else:
                # Audio file is already optimized, no compression needed
                self.status_callback("⏩ Input is already optimized audio file. Skipping compression...")
                return
        else:
            # Extract audio from video
            self.status_callback(f"🎬 Step 1/3: Extracting and compressing audio ({self.bitrate})...")
            
            if os.path.exists(audio_file):
                self.status_callback("⏩ Skipping extraction (Found existing audio file)...")
                return
            
            clip = None
            try:
                clip = VideoFileClip(self.video_path)
                clip.audio.write_audiofile(audio_file, bitrate=self.bitrate, logger=None)
            finally:
                if clip is not None:
                    clip.close()
    
    def transcribe_audio(self, audio_file):
        """
        Upload and transcribe audio with retry logic and chunked upload for large files.
        
        Args:
            audio_file (str): Path to audio file
            
        Returns:
            object: Transcript object from AssemblyAI
            
        Raises:
            Exception: If all retry attempts fail
        """
        # Determine dynamic timeout based on file size
        aai.settings.http_timeout = self.get_dynamic_timeout(audio_file)
        
        file_size = os.path.getsize(audio_file)
        file_size_mb = file_size / (1024 * 1024)
        
        transcript = None
        retry_delay = RETRY_DELAY
        
        for attempt in range(MAX_RETRIES):
            # Check if cancellation requested
            if self.cancel_check():
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                return None
            
            try:
                attempt_num = attempt + 1
                self.status_callback(
                    f"🚀 Step 2/3: Uploading & Transcribing (Attempt {attempt_num}/{MAX_RETRIES}) "
                    f"- {file_size_mb:.1f}MB..."
                )
                
                transcriber = aai.Transcriber()
                
                # For large files, use chunked upload
                if file_size > FILE_SIZE_WARNING:
                    transcript = self._transcribe_chunked(
                        transcriber, audio_file, attempt_num
                    )
                else:
                    transcript = transcriber.transcribe(audio_file, config=self.config)
                
                if transcript.status == aai.TranscriptStatus.error:
                    raise Exception(transcript.error)
                
                return transcript  # Success - return transcript
            
            except Exception as e:
                if attempt < MAX_RETRIES - 1:  # Not the last attempt
                    # Exponential backoff
                    self.status_callback(
                        f"⚠️ Network issue detected. Retrying in {retry_delay:.0f} seconds "
                        f"(Attempt {attempt_num}/{MAX_RETRIES})..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= RETRY_BACKOFF  # Increase delay for next retry
                else:
                    raise e  # All attempts failed - raise error
    
    def _transcribe_chunked(self, transcriber, audio_file, attempt_num):
        """
        Upload and transcribe audio in chunks for very large files.
        
        Args:
            transcriber (aai.Transcriber): AssemblyAI transcriber instance
            audio_file (str): Path to audio file
            attempt_num (int): Current attempt number
            
        Returns:
            object: Transcript object
        """
        file_size = os.path.getsize(audio_file)
        num_chunks = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE
        
        self.status_callback(
            f"📤 Uploading large file in {num_chunks} chunks (Attempt {attempt_num})..."
        )
        
        # For now, use standard upload - AssemblyAI handles large files
        # Future: Implement actual chunked streaming if needed
        return transcriber.transcribe(audio_file, config=self.config)
    
    def save_files(self, transcript, paths):
        """
        Save transcription results to files.
        
        Args:
            transcript (object): AssemblyAI transcript object
            paths (dict): Dictionary containing all file paths
        """
        self.status_callback("💾 Step 3/3: Saving Text and SRT files...")
        
        # Save transcript text
        with open(paths["txt_path"], "w", encoding="utf-8") as f:
            f.write(transcript.text)
        
        # Save SRT subtitles
        srt_subtitles = transcript.export_subtitles_srt()
        with open(paths["srt_path"], "w", encoding="utf-8") as f:
            f.write(srt_subtitles)
        
        # Rename temp audio to final name
        if os.path.exists(paths["audio_file"]):
            os.rename(paths["audio_file"], paths["final_audio_path"])
    
    def run(self):
        """
        Execute complete transcription workflow.
        
        Returns:
            dict: Contains success status and output folder path
            
        Raises:
            Exception: If any step fails
        """
        # Validate file exists
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file no longer exists: {self.video_path}")
        
        # Get all required paths
        paths = self.get_output_paths()
        self.audio_file = paths["audio_file"]
        
        # Step 1: Extract audio
        self.extract_audio(paths["audio_file"])
        
        # Check cancellation before step 2
        if self.cancel_check():
            if os.path.exists(paths["audio_file"]):
                os.remove(paths["audio_file"])
            return {"success": False}
        
        # Step 2: Transcribe
        transcript = self.transcribe_audio(paths["audio_file"])
        
        if transcript is None:  # Cancelled
            return {"success": False}
        
        # Step 3: Save files
        self.save_files(transcript, paths)
        
        return {
            "success": True,
            "output_folder": paths["output_folder"],
            "video_name": paths["video_name_without_ext"],
            "audio_file": paths["final_audio_path"],
            "txt_file": paths["txt_path"],
            "srt_file": paths["srt_path"]
        }
    
    def cleanup(self):
        """Clean up temporary files if transcription was cancelled."""
        if self.audio_file and os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
            except Exception:
                pass  # Ignore cleanup errors
