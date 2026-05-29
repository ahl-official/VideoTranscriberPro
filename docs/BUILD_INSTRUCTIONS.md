# 🚀 Quick Build Instructions for IT

## For Building the Windows Installer in 3 Minutes

### Prerequisites (One-time Setup)
1. **Install Python 3.8+**: https://www.python.org/downloads/
2. **Install NSIS** (optional but recommended):
   - Download: https://nsis.sourceforge.io/Download
   - Or run: `choco install nsis -y`

### Build Steps

#### Step 1: Open Command Prompt
- Go to: `C:\Users\admin\Desktop\YT_local`
- Right-click → "Open Command Prompt here"

#### Step 2: Run Build Script
```bash
build.bat
```

That's it! The script will:
- ✅ Install dependencies
- ✅ Convert Python to executable
- ✅ Create Windows installer
- ✅ Show final output location

### Output Files
**After build completes:**
- `dist\VideoTranscriberPro\VideoTranscriberPro.exe` ← Standalone executable
- `VideoTranscriberPro-Installer.exe` ← Professional installer

### Distribution
**Option 1: Installer (Professional)**
- Send `VideoTranscriberPro-Installer.exe` to employees
- They run it → Automatic installation
- ~150MB total

**Option 2: Standalone Executable**
- Copy `VideoTranscriberPro.exe`
- Share via email/network
- No installation needed
- Run from anywhere

---

## 🐛 Troubleshooting Build

### Issue: "Python not found"
```bash
# Verify Python installed
python --version

# If not in PATH, use full path to Python
C:\Python39\python.exe -m py_compile main.py
```

### Issue: "PyInstaller error"
```bash
# Reinstall dependencies
pip install --upgrade pyinstaller==6.1.0
```

### Issue: "NSIS not found"
- Installer creation skipped but exe works fine
- Standalone `VideoTranscriberPro.exe` is still generated
- Install NSIS if you need professional installer

### Issue: "Permission denied" / "Access denied"
- Run Command Prompt **as Administrator**
- Right-click → "Run as Administrator"

---

## ✅ Testing the Build

### Test Standalone Executable
```bash
# Test it runs
dist\VideoTranscriberPro\VideoTranscriberPro.exe
```

### Test Installer
```bash
# Run installer
VideoTranscriberPro-Installer.exe

# Follow prompts
# Check Desktop for shortcut
```

---

## 📦 Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] NSIS installed (optional)
- [ ] run `build.bat` successfully
- [ ] Standalone exe generated and tested
- [ ] Installer generated (if NSIS installed)
- [ ] Files ready for distribution
- [ ] Employees have API keys ready
- [ ] Distributed via email/network/intranet
- [ ] Employees completed setup
- [ ] First transcription tested

---

## 📊 Build Output Summary

```
Project Structure After Build:
├── build/                          ← Build artifacts (can delete)
├── dist/
│   └── VideoTranscriberPro/
│       ├── VideoTranscriberPro.exe ← Main executable ✓
│       ├── *.dll / *.pyd           ← Dependencies
│       └── [other files]
├── VideoTranscriberPro-Installer.exe ← Windows installer ✓
│
├── [Source Files]
├── build.bat                        ← Run this to build
├── build.spec                       ← PyInstaller config
└── installer.nsi                    ← NSIS installer config
```

---

## 🔄 Rebuild/Update Process

To create a new version:
1. Make code changes (if needed)
2. Run `build.bat` again
3. New installer generated automatically
4. Distribute new `.exe` files
5. API keys automatically preserved on employee machines!

---

## 💡 Pro Tips

✅ **First build takes ~5 minutes** (subsequent builds are faster)  
✅ **Can safely delete** `build/` folder after completion  
✅ **Keep** `dist/` folder for distribution  
✅ **Installer size:** ~150MB (standalone can be copied anywhere)  
✅ **No installation needed** if distributing just the `.exe`  

---

**Questions? See DEPLOYMENT_GUIDE.md for complete guide**
