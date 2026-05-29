# Video Transcriber Pro - Deployment Guide

## 🚀 For IT/System Administrators

This guide explains how to build and distribute the Video Transcriber Pro application to your company employees.

---

## 📋 Prerequisites

### For Building the Installer (One-time, on your machine):
- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **NSIS** (optional but recommended for installer) ([Download](https://nsis.sourceforge.io/Download))
  - Or install via: `choco install nsis -y`

### For Employee Machines (where app will run):
- **Windows 7 or newer** (x86 or x64)
- **Internet connection** (for AssemblyAI API)
- **~500MB free disk space** (for application + dependencies)
- **Sufficient QuickTime/audio codec support** (usually pre-installed)

---

## 🔧 Building the Installer

### Step 1: Prepare Build Environment
```bash
cd "C:\Users\admin\Desktop\YT_local"

# Install build dependencies
pip install -r requirements-build.txt
```

### Step 2: Run Build Script
Simply double-click or run:
```bash
build.bat
```

**What it does:**
- ✓ Cleans previous builds
- ✓ Installs dependencies
- ✓ Converts Python to executable with PyInstaller
- ✓ Creates Windows Installer with NSIS
- ✓ Generates final .exe installer

### Step 3: Output Files
After successful build, you'll have:

```
VideoTranscriberPro/
├── VideoTranscriberPro.exe          ← Standalone executable
├── *.dll / *.pyd files              ← Dependencies
└── [other files]

VideoTranscriberPro-Installer.exe    ← Installer for distribution
```

---

## 📦 Distribution Methods

### Method 1: Using Installer (Recommended for IT)
```
VideoTranscriberPro-Installer.exe
↓
Send to employees (via email, share drive, etc.)
↓
Employees double-click → Automatic installation
↓
Shortcuts created on Desktop + Start Menu
```

**Advantages:**
- ✓ Professional installer look
- ✓ Auto-handles installation path
- ✓ Creates shortcuts automatically
- ✓ Easy uninstall via Control Panel
- ✓ Only ~150MB total size

### Method 2: Standalone Executable
```
VideoTranscriberPro.exe
↓
Copy to network drive or email
↓
Employees run directly (no installation needed)
```

**Advantages:**
- ✓ Portable, no installation
- ✓ No admin rights needed
- ✓ Can run from any location
- ✓ Easy to update (just replace file)

**Disadvantages:**
- ✗ No shortcuts created
- ✗ Requires ~500MB in any folder

---

## 🔐 API Key Configuration

### First Launch (Employee Setup)
1. User opens Video Transcriber Pro
2. **First-time screen:** "AssemblyAI API Key (First Time Setup)"
3. User enters their API key once
4. ✓ Key is saved to: `C:\Users\[username]\.video_transcriber\settings.json`

### Subsequent Launches
- ✓ **No API Key Entry Needed!**
- Saved key automatically loads
- Shows: "✓ API Key Saved" button
- User can click "🔑 Change API Key" if needed

### Managing API Keys
- **Each employee's key** is stored locally in their user profile
- **Not shared** between employees
- **Secure location:** User's home directory (hidden folder)

### Change API Key Anytime
1. Click "🔑 Change API Key" button
2. Enter new API key
3. Start transcription to save new key

---

## 📊 System Requirements & Recommendations

### Minimum
- OS: Windows 7 SP1 or newer
- RAM: 4GB
- CPU: Dual-core 2.4GHz
- Disk: 1GB available (for OS) + 500MB for app

### Recommended
- OS: Windows 10 or Windows 11
- RAM: 8GB+
- CPU: Quad-core 3.0GHz+
- Disk: 2GB+ available
- Internet: 10+ Mbps (for large files)
- Network: Stable/fiber connection

### Video File Support
- Formats: MP4, MKV, MOV, AVI, FLV, WMV, WEBM
- Audio Formats: MP3, WAV, FLAC, M4A, OGG, AAC, WMA
- Max Size: Recommended ≤ 10GB (tested, works with compression)

---

## 🛠️ Installation for Employees

### With Installer:
1. **Double-click** `VideoTranscriberPro-Installer.exe`
2. **Click Next** through welcome screen
3. **Choose install location** (default: `C:\Program Files\VideoTranscriberPro`)
4. **Click Install**
5. ✓ Done! Shortcuts on Desktop + Start Menu

### Without Installer (Standalone):
1. **Copy** `VideoTranscriberPro.exe` to desired location
2. **Double-click** to run
3. ✓ Ready to use!

---

## 🎬 First Use Guide for Employees

### Step 1: Launch Application
- Double-click **Video Transcriber Pro** on Desktop
- Window opens: 550x550 pixels

### Step 2: Enter API Key (First Time Only)
- **Label:** "AssemblyAI API Key (First Time Setup)"
- **Action:** Paste your AssemblyAI API key
- **Saved:** Automatically stored for next time

### Step 3: Select Video or Audio File
- Click **📁 Browse Video**
- Select file: `.mp4`, `.wav`, `.flac`, etc.
- **Shows:** File name, size, compression recommendation

### Step 4: Choose Compression Quality
- **Dropdown:** Audio Compression Quality
- **Options:**
  - 64 kbps - Best Quality (Slow)
  - 48 kbps - Good Quality (Medium)  
  - 32 kbps - Balanced (Fast, **Recommended**)
- **Default:** 32 kbps (good quality, reasonable time)

### Step 5: Start Transcription
- Click **🚀 Start Transcription**
- **Progress bar** shows status
- **Status updates:** Compression → Upload → Transcribing

### Step 6: Get Results
- **Output folder:** `Downloads\[filename]\`
- **Files created:**
  - `transcript.txt` - Plain text transcript
  - `subtitles.srt` - SRT subtitle file
  - `*_audio.mp3` - Compressed audio used

---

## ⏱️ Estimated Processing Times

| File Size | Duration | Estimated Time | Quality |
|-----------|----------|----------------|---------|
| 100 MB (30 min video) | 30 min | 5-15 min | 64k best |
| 500 MB (2.5 hour video) | 2.5 hrs | 20-45 min | 32k balanced |
| 1 GB (5 hour video) | 5 hrs | 45 min - 2 hrs | 32k balanced |
| 2 GB (10 hour video) | 10 hrs | 2-4 hrs | 32k balanced |

**Note:** Times depend on:
- Internet speed
- AssemblyAI API load
- Compression bitrate chosen
- CPU speed (for local compression)

---

## 🐛 Troubleshooting

### Issue: "Invalid Format" Error
**Solution:** 
- Ensure file is one of supported formats
- File not corrupted - try another file

### Issue: "API Key Required" Error
**Solution:**
- Check API key is correct
- Ensure no extra spaces
- Try "Change API Key" button

### Issue: Slow Transcription
**Solutions:**
- ✓ Increase compression to 32 or 48kbps
- ✓ Use WAV/FLAC? → App will compress automatically
- ✓ Check internet speed (10+ Mbps recommended)
- ✓ Ensure AssemblyAI account has credits

### Issue: "Transcription cancelled" Message
**Solutions:**
- Don't close app during processing
- Keep stable internet connection
- For files >2GB, use 32kbps compression
- Check AssemblyAI API credits

### Issue: Application Won't Start
**Solutions:**
- Ensure Windows 7+ (check with `winver`)
- Run from C:\ (not network drive)
- Run as Administrator (right-click → "Run as administrator")
- Reinstall: Uninstall → Delete folder → Reinstall

---

## 🔄 Updating to New Version

### When Updates Available:

**Option 1 - Fresh Install:**
```
1. Download new VideoTranscriberPro-Installer.exe
2. Run installer
3. Old API key preserved!
```

**Option 2 - Standalone Update:**
```
1. Replace VideoTranscriberPro.exe
2. Settings remain unchanged
```

---

## 📝 Uninstallation

### Windows Installer:
1. **Settings** → **Apps & features**
2. Find **Video Transcriber Pro**
3. Click **Uninstall**
4. Settings automatically deleted

### Standalone:
1. **Delete** VideoTranscriberPro.exe file
2. ✓ Completely removed

---

## 🔒 Data & Privacy

### What Gets Saved Locally:
- **API Key** - `C:\Users\[username]\.video_transcriber\settings.json`
- **Application Files** - `C:\Program Files\VideoTranscriberPro\` (installer)
- **Output Files** - `Downloads\[filename]\` (user creates)

### What Gets Sent to AssemblyAI:
- **Audio file only** (compressed, uploaded securely)
- **Not stored** on AssemblyAI servers (standard plan)
- **Encrypted** during transmission (HTTPS)

### No Data Shared With:
- ✓ Not sent to Microsoft, Google, etc.
- ✓ Only AssemblyAI API (user's own API key)
- ✓ Company cannot see transcriptions

---

## 📞 Support & Resources

### Troubleshooting:
1. Check this guide first
2. Visit [AssemblyAI Docs](https://www.assemblyai.com/docs)
3. Verify API key has credits: [Dashboard](https://www.assemblyai.com/app)

### Getting Help:
- **For Python/Code Issues:** Check GitHub issues
- **For AssemblyAI Issues:** Contact AssemblyAI support
- **For Installation Issues:** See Troubleshooting section above

---

## 📊 Version Information

- **Application:** Video Transcriber Pro v1.0.0
- **Python:** 3.8+
- **AssemblyAI SDK:** 0.64.0
- **MoviePy:** 1.0.3
- **Last Updated:** May 2026

---

## ✅ Checklist for IT Deployment

- [ ] Python 3.8+ installed (build machine only)
- [ ] NSIS installed (optional, for installer)
- [ ] Build dependencies installed: `pip install -r requirements-build.txt`
- [ ] Build script run: `build.bat`
- [ ] Output files generated successfully
- [ ] Installer tested on clean Windows machine
- [ ] Employee distribution method chosen
- [ ] Instructions provided to employees
- [ ] Support contact info shared
- [ ] API key distribution handled separately

---

**Ready to deploy! Questions? Contact IT Support or check troubleshooting section above.**
