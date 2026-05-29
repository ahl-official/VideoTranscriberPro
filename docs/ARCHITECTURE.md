# Project Architecture

## Module Dependency Graph

```
main.py (Entry Point)
    └── ui.py (GUI Application)
        ├── config.py (Settings & Constants)
        ├── validators.py (Input Validation)
        │   └── config.py
        └── transcriber.py (Transcription Logic)
            ├── config.py
            └── External: assemblyai, moviepy
```

## File Breakdown

### 1. **main.py** (Entry Point)
**Purpose:** Launches the application  
**Size:** ~20 lines  
**Dependencies:** tkinter, ui.py

```python
from ui import TranscriberApp
# Creates root window and runs the app
```

---

### 2. **config.py** (Configuration)
**Purpose:** Centralized configuration and constants  
**Size:** ~50 lines  
**Dependencies:** pathlib

**Contains:**
- Video format support (`SUPPORTED_VIDEO_FORMATS`)
- API settings (`HTTP_TIMEOUT`, `SPEECH_MODELS`)
- Retry configuration (`MAX_RETRIES`, `RETRY_DELAY`)
- File paths (`DOWNLOADS_FOLDER`)
- UI configuration (colors, fonts, dimensions)

**Benefits:**
- Single source of truth for all settings
- Easy to customize (change one place, affects entire app)
- No hardcoded values scattered throughout code

---

### 3. **validators.py** (Input Validation)
**Purpose:** Reusable validation functions  
**Size:** ~55 lines  
**Dependencies:** os, config.py

**Functions:**
- `validate_video_format()` - Check if file is supported
- `get_supported_formats_display()` - Get formatted format list
- `validate_api_key()` - Validate API key input
- `validate_file_exists()` - Check if file exists

**Benefits:**
- Separation of concerns (validation logic separate from UI)
- Reusable across modules
- Easy to test independently
- Single responsibility principle

---

### 4. **transcriber.py** (Transcription Logic)
**Purpose:** Handles the transcription workflow  
**Size:** ~200 lines  
**Dependencies:** os, time, uuid, assemblyai, moviepy, config.py

**Class: TranscriptionManager**
- `__init__()` - Initialize with API key and paths
- `get_output_paths()` - Create folder structure
- `extract_audio()` - Extract and compress audio
- `transcribe_audio()` - Upload to AssemblyAI (with retries)
- `save_files()` - Save results (txt, srt, audio)
- `run()` - Execute full workflow
- `cleanup()` - Clean up temp files

**Benefits:**
- Business logic separated from UI
- Can be tested independently
- Reusable in other applications
- Clean workflow organization

---

### 5. **ui.py** (User Interface)
**Purpose:** GUI components and event handling  
**Size:** ~290 lines  
**Dependencies:** tkinter, config.py, validators.py, transcriber.py

**Class: TranscriberApp**
- UI setup methods
- Event handlers (browse, start, cancel)
- Status updates
- Error handling

**Benefits:**
- Clean separation: UI logic from business logic
- Maintainable UI code
- Easy to redesign (change ui.py only)
- Thread-safe updates using `root.after()`

---

## Data Flow

```
User Input (UI)
    ↓
validators.py (Validate Input)
    ↓
transcriber.py (Process)
    ├→ Extract Audio (moviepy)
    ├→ Transcribe (assemblyai)
    └→ Save Results
    ↓
ui.py (Display Results)
```

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **File Count** | 1 (monolithic) | 5 (modular) |
| **Lines per File** | ~280 | 20-290 (organized) |
| **Code Reusability** | Low | High |
| **Testing** | Difficult | Easy |
| **Maintainability** | Hard | Easy |
| **Configuration** | Scattered | Centralized |
| **Separation of Concerns** | No | Yes |

## Running the Application

```bash
python main.py
```

That's it! Python will automatically import and run the modular structure.

## Adding New Features

### Example: Add a new validator
1. Open `validators.py`
2. Add your validation function
3. Import in `ui.py` or `transcriber.py`

### Example: Change colors
1. Open `config.py`
2. Update color constants
3. All UI colors change automatically

### Example: Change retry behavior
1. Open `config.py`
2. Update `MAX_RETRIES` or `RETRY_DELAY`
3. Entire retry system uses new values

### Example: Add logging
1. Create `logger.py` with logging setup
2. Import in modules that need it
3. No other files affected

## Benefits of Modular Architecture

✅ **Maintainability** - Easy to find and fix code  
✅ **Scalability** - Add features without touching existing code  
✅ **Testability** - Each module can be tested independently  
✅ **Reusability** - Use modules in other projects  
✅ **Readability** - Clear purpose for each file  
✅ **Flexibility** - Easy to swap implementations  
✅ **Collaboration** - Multiple developers can work on different modules  

