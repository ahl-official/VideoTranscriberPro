"""
UI module for Video Transcriber Pro.
Contains all GUI components and user interface logic.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from settings import get_settings
from config import (
    SUPPORTED_VIDEO_FORMATS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    TITLE_FONT,
    LABEL_FONT,
    BUTTON_FONT,
    BUTTON_BOLD_FONT,
    COLOR_BROWSE_BTN,
    COLOR_START_BTN,
    COLOR_CANCEL_BTN,
    TEXT_WHITE,
    TEXT_BLACK,
    TEXT_GRAY,
    TEXT_RED,
    AUDIO_BITRATE_OPTIONS,
    AUDIO_BITRATE_DEFAULT,
    FILE_SIZE_WARNING,
    FILE_SIZE_LARGE
)
from validators import (
    validate_video_format,
    validate_api_key,
    get_supported_formats_display,
    get_file_size_display,
    estimate_audio_size,
    should_compress_audio
)
from transcriber import TranscriptionManager
import os


class TranscriberApp:
    """Main application class for Video Transcriber Pro."""
    
    def __init__(self, root):
        """
        Initialize the transcriber application.
        
        Args:
            root (tk.Tk): Root window
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x550")  # Increased height for bitrate selector
        self.root.resizable(False, False)
        
        # Load settings
        self.settings = get_settings()
        
        self.video_path = ""
        self.is_transcribing = False
        self.api_key = self.settings.get_api_key()  # Load from settings or environment
        self.selected_bitrate = AUDIO_BITRATE_DEFAULT
        self.file_type = "video"  # Default to video, will be updated when file is selected
        self.api_key_input_visible = False  # Track if API key input field is visible
        
        # Build UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup all UI components."""
        # Title
        title_label = tk.Label(
            self.root,
            text="AssemblyAI Video Transcriber",
            font=TITLE_FONT
        )
        title_label.pack(pady=15)
        
        # API Key Section
        self.create_api_key_section()
        
        # File Browse Section
        self.create_file_browse_section()
        
        # Bitrate Selection Section
        self.create_bitrate_section()
        
        # Buttons Section
        self.create_buttons_section()
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=400,
            mode="indeterminate"
        )
        
        # Status Label
        self.status_label = tk.Label(self.root, text="Ready.", font=LABEL_FONT)
        self.status_label.pack(pady=5)
    
    def create_api_key_section(self):
        """Create API key input section."""
        api_frame = tk.Frame(self.root)
        api_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Check if API key is already saved
        if self.settings.has_api_key():
            # Show status label and change button
            api_label = tk.Label(
                api_frame, 
                text="✓ API Key Saved", 
                font=LABEL_FONT,
                fg="green"
            )
            api_label.pack(anchor=tk.W, pady=5)
            
            # Add a "Change API Key" button
            button_subframe = tk.Frame(api_frame)
            button_subframe.pack(anchor=tk.W, pady=5)
            
            self.change_api_key_btn = tk.Button(
                button_subframe,
                text="🔑 Change API Key",
                command=self.show_api_key_input,
                font=LABEL_FONT,
                bg="#FF9500",
                fg=TEXT_WHITE
            )
            self.change_api_key_btn.pack(side=tk.LEFT, padx=5)
            
            # Hidden API key entry (initially hidden)
            self.api_key_entry = tk.Entry(api_frame, font=LABEL_FONT, show="*", width=50)
            self.api_key_entry.pack(fill=tk.X, pady=5)
            self.api_key_entry.pack_forget()  # Hide initially
            
            self.api_key_entry.insert(0, "Paste your new API key here")
            self.api_key_entry.config(fg=TEXT_GRAY)
            
            self.api_key_entry.bind("<FocusIn>", self.on_api_key_focus_in)
            self.api_key_entry.bind("<FocusOut>", self.on_api_key_focus_out)
            
            # Store reference to indicate API key was pre-loaded
            self.api_key_input_visible = False
        else:
            # Show API key entry field (first time)
            api_label = tk.Label(api_frame, text="AssemblyAI API Key (First Time Setup):", font=LABEL_FONT)
            api_label.pack(anchor=tk.W)
            
            self.api_key_entry = tk.Entry(api_frame, font=LABEL_FONT, show="*", width=50)
            self.api_key_entry.pack(fill=tk.X, pady=5)
            
            self.api_key_entry.insert(0, "Paste your API key here")
            self.api_key_entry.config(fg=TEXT_GRAY)
            
            self.api_key_entry.bind("<FocusIn>", self.on_api_key_focus_in)
            self.api_key_entry.bind("<FocusOut>", self.on_api_key_focus_out)
            
            self.api_key_input_visible = True
    
    def create_file_browse_section(self):
        """Create file browse section."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        self.browse_btn = tk.Button(
            frame,
            text="📁 Browse Video",
            command=self.browse_file,
            font=BUTTON_FONT,
            bg=COLOR_BROWSE_BTN
        )
        self.browse_btn.grid(row=0, column=0, padx=10)
        
        self.file_label = tk.Label(
            frame,
            text="No video selected",
            fg=TEXT_GRAY,
            font=LABEL_FONT,
            wraplength=350
        )
        self.file_label.grid(row=0, column=1)
    
    def create_bitrate_section(self):
        """Create bitrate selection section."""
        bitrate_frame = tk.Frame(self.root)
        bitrate_frame.pack(pady=8, padx=20, fill=tk.X)
        
        bitrate_label = tk.Label(
            bitrate_frame,
            text="Audio Compression Quality:",
            font=LABEL_FONT
        )
        bitrate_label.pack(anchor=tk.W)
        
        # Create list of display options and their corresponding bitrate values
        self.bitrate_options = AUDIO_BITRATE_OPTIONS
        display_options = [option[0] for option in self.bitrate_options]
        
        self.bitrate_combo = ttk.Combobox(
            bitrate_frame,
            values=display_options,
            state="readonly",
            width=47,
            font=LABEL_FONT
        )
        # Set default selection
        default_index = next(
            (i for i, opt in enumerate(self.bitrate_options) if opt[1] == AUDIO_BITRATE_DEFAULT),
            1  # Default to index 1 if not found
        )
        self.bitrate_combo.current(default_index)
        self.bitrate_combo.pack(fill=tk.X, pady=3)
        
        # Bind change event to update selected bitrate
        self.bitrate_combo.bind("<<ComboboxSelected>>", self.on_bitrate_selected)
        
        # Info label
        info_label = tk.Label(
            bitrate_frame,
            text="💡 64k=best quality (slower), 32k=balanced (recommended), 48k=good quality (medium)",
            font=("Arial", 8),
            fg=TEXT_GRAY
        )
        info_label.pack(anchor=tk.W)
    
    def on_bitrate_selected(self, event):
        """Handle bitrate selection change."""
        index = self.bitrate_combo.current()
        if 0 <= index < len(self.bitrate_options):
            self.selected_bitrate = self.bitrate_options[index][1]
    
    def show_api_key_input(self):
        """Show the API key input field to change API key."""
        self.api_key_entry.pack(fill=tk.X, pady=5)
        self.change_api_key_btn.config(state=tk.DISABLED, text="🔑 Enter New Key")
        self.api_key_input_visible = True
    
    def create_buttons_section(self):
        """Create control buttons section."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)
        
        self.start_btn = tk.Button(
            button_frame,
            text="🚀 Start Transcription",
            command=self.start_process,
            font=BUTTON_BOLD_FONT,
            bg=COLOR_START_BTN,
            fg=TEXT_WHITE,
            state=tk.DISABLED
        )
        self.start_btn.grid(row=0, column=0, padx=10)
        
        self.cancel_btn = tk.Button(
            button_frame,
            text="⛔ Cancel",
            command=self.cancel_process,
            font=BUTTON_BOLD_FONT,
            bg=COLOR_CANCEL_BTN,
            fg=TEXT_WHITE,
            state=tk.DISABLED
        )
        self.cancel_btn.grid(row=0, column=1, padx=10)
    
    # ==========================================
    # EVENT HANDLERS
    # ==========================================
    
    def on_api_key_focus_in(self, event):
        """Clear placeholder text when user focuses on API key field."""
        current_text = self.api_key_entry.get()
        if current_text in ("Paste your API key here", "Paste your new API key here"):
            self.api_key_entry.delete(0, tk.END)
            self.api_key_entry.config(fg=TEXT_BLACK)
    
    def on_api_key_focus_out(self, event):
        """Show placeholder if field is empty."""
        if self.api_key_entry.get() == "":
            placeholder = "Paste your new API key here" if self.api_key_input_visible else "Paste your API key here"
            self.api_key_entry.insert(0, placeholder)
            self.api_key_entry.config(fg=TEXT_GRAY)
    
    def browse_file(self):
        """Handle browse file button click."""
        filetypes = (
            ('Video & Audio files', '*.mp4 *.mkv *.mov *.avi *.flv *.wmv *.webm *.mp3 *.wav *.m4a *.flac *.ogg *.aac *.wma'),
            ('Video files', '*.mp4 *.mkv *.mov *.avi *.flv *.wmv *.webm'),
            ('Audio files', '*.mp3 *.wav *.m4a *.flac *.ogg *.aac *.wma'),
            ('All files', '*.*')
        )
        filepath = filedialog.askopenfilename(
            title='Select a video or audio file',
            filetypes=filetypes
        )
        
        if filepath:
            is_valid, file_ext, file_type = validate_video_format(filepath)
            
            if not is_valid:
                messagebox.showerror(
                    "Invalid Format",
                    f"Unsupported file format: {file_ext}\n\n"
                    f"Supported formats: {get_supported_formats_display()}"
                )
                self.file_label.config(text="Invalid format - try another file", fg=TEXT_RED)
                return
            
            self.video_path = filepath
            self.file_type = file_type  # Store file type
            filename = os.path.basename(filepath)
            
            # Get file size and show it
            file_size = os.path.getsize(filepath)
            file_size_display = get_file_size_display(file_size)
            
            # For audio files, check if compression is needed
            if file_type == "audio":
                display_text = f"{filename} ({file_size_display}) [AUDIO]"
                
                # Check if audio file needs compression
                needs_compression, reason = should_compress_audio(filepath, file_ext)
                
                if needs_compression:
                    # Enable bitrate selector for audio compression
                    self.bitrate_combo.config(state="readonly")
                    
                    messagebox.showwarning(
                        "Large Audio File - Compression Recommended",
                        f"⚠️ {reason}\n\n"
                        f"File size: {file_size_display}\n\n"
                        f"AssemblyAI has a 450MB upload limit.\n\n"
                        f"✓ Select compression quality above to compress before upload\n\n"
                        f"Recommended: 32 kbps (balanced)\n"
                        f"Bitrate: Higher = better quality but slower\n"
                        f"Bitrate: Lower = faster but lower quality"
                    )
                else:
                    # Audio file is already optimized, disable bitrate selector
                    self.bitrate_combo.config(state="disabled")
                    
                    messagebox.showinfo(
                        "Audio File Selected",
                        f"✓ Audio file selected: {filename}\n\n"
                        f"Size: {file_size_display}\n\n"
                        f"File is already optimized - no compression needed!\n"
                        f"Transcription will start immediately."
                    )
            else:
                # For video files, show estimation
                estimated_audio = estimate_audio_size(file_size)
                estimated_audio_display = get_file_size_display(estimated_audio)
                display_text = f"{filename} ({file_size_display})"
                
                # Show warning if file is large
                if file_size > FILE_SIZE_LARGE:
                    messagebox.showwarning(
                        "Very Large File",
                        f"⚠️ This is a very large video ({file_size_display}).\n\n"
                        f"Estimated audio size: {estimated_audio_display}\n\n"
                        f"⏱️ Transcription may take 2-4 hours.\n\n"
                        f"Make sure:\n"
                        f"• You have a stable internet connection\n"
                        f"• Don't close the application during processing\n"
                        f"• Your API account has enough credits"
                    )
                elif file_size > FILE_SIZE_WARNING:
                    messagebox.showinfo(
                        "Large File",
                        f"ℹ️ This is a large video ({file_size_display}).\n\n"
                        f"Estimated audio size: {estimated_audio_display}\n\n"
                        f"⏱️ Transcription may take 1-2 hours."
                    )
            
            self.file_label.config(text=display_text, fg=TEXT_BLACK)
            self.start_btn.config(state=tk.NORMAL)
    
    def start_process(self):
        """Handle start transcription button click."""
        # Get API Key (from input or saved)
        api_key = self.api_key_entry.get().strip()

        # If entry contains placeholder or is empty, and we have a saved key, use saved key
        placeholders = ("Paste your API key here", "Paste your new API key here")
        if (not api_key or api_key in placeholders) and self.settings.has_api_key():
            api_key = self.settings.get_api_key()

        # Validate API Key
        if not validate_api_key(api_key):
            messagebox.showerror(
                "API Key Required",
                "Please enter your AssemblyAI API key."
            )
            return
        
        self.api_key = api_key
        
        # Save API key to settings if it's new or changed
        if not self.settings.has_api_key() or self.api_key_input_visible:
            self.settings.set_api_key(api_key)
        
        # Update UI state
        self.is_transcribing = True
        self.start_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.browse_btn.config(state=tk.DISABLED)
        self.api_key_entry.config(state=tk.DISABLED)
        self.progress.pack(pady=5)
        self.progress.start(15)
        
        # Run transcription in background thread
        thread = threading.Thread(target=self.run_transcription, daemon=True)
        thread.start()
    
    def cancel_process(self):
        """Handle cancel button click."""
        self.is_transcribing = False
        self.update_status("❌ Transcription cancelled by user.")
    
    def run_transcription(self):
        """Execute transcription workflow in background."""
        try:
            # Create transcription manager
            manager = TranscriptionManager(
                api_key=self.api_key,
                video_path=self.video_path,
                status_callback=self.update_status,
                cancel_check=lambda: not self.is_transcribing,
                bitrate=self.selected_bitrate,
                file_type=self.file_type
            )
            
            # Run transcription
            result = manager.run()
            
            if not result["success"]:
                self.update_status("❌ Transcription cancelled by user.")
                return
            
            # Show success message
            self.update_status("🎉 Done! Files saved successfully.")
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Transcription complete!\n\n"
                f"Saved in:\n{result['output_folder']}\n\n"
                f"Files:\n"
                f"• {result['video_name']}_compressed_audio.mp3\n"
                f"• {result['video_name']}_transcript.txt\n"
                f"• {result['video_name']}_subtitles.srt"
            ))
        
        except Exception as e:
            self.update_status("❌ Error occurred!")
            self.root.after(0, lambda: messagebox.showerror(
                "Error",
                f"An error occurred:\n{str(e)}"
            ))
        
        finally:
            self.root.after(0, self.reset_ui)
    
    def update_status(self, text):
        """
        Update status label text (thread-safe).
        
        Args:
            text (str): Status message
        """
        self.root.after(0, lambda: self.status_label.config(text=text))
    
    def reset_ui(self):
        """Reset UI to initial state."""
        self.progress.stop()
        self.progress.pack_forget()
        self.start_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.browse_btn.config(state=tk.NORMAL)
        self.api_key_entry.config(state=tk.NORMAL)
        self.is_transcribing = False
