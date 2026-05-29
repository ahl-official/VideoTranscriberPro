@echo off
REM =====================================================
REM Video Transcriber Pro - Build Script
REM Converts Python app to Windows Installer
REM =====================================================

echo.
echo ========================================
echo Video Transcriber Pro - Build System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo [1/5] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo ✓ Cleaned old build files

echo.
echo [2/5] Installing build dependencies...
pip install -r requirements-build.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [3/5] Building executable with PyInstaller...
python -m PyInstaller build.spec --distpath dist --workpath build
if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)
echo ✓ Executable created

echo.
echo [4/5] Creating Windows Installer...
REM Check if NSIS is installed
where makensis >nul 2>&1
if errorlevel 1 (
    echo WARNING: NSIS not found. Installer creation skipped.
    echo Install NSIS from: https://nsis.sourceforge.io/Download
    echo Or run: choco install nsis -y
    echo Executable is ready in: dist\VideoTranscriberPro\VideoTranscriberPro.exe
    goto :skip_nsis
)

makensis installer.nsi
if errorlevel 1 (
    echo ERROR: NSIS installer creation failed
    pause
    exit /b 1
)
echo ✓ Windows Installer created

:skip_nsis

echo.
echo ========================================
echo ✓ BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo OUTPUT FILES:
echo [Executable] dist\VideoTranscriberPro\VideoTranscriberPro.exe
if exist "VideoTranscriberPro-Installer.exe" (
    echo [Installer] VideoTranscriberPro-Installer.exe
)
echo.
echo NEXT STEPS:
echo 1. Test the application: dist\VideoTranscriberPro\VideoTranscriberPro.exe
if exist "VideoTranscriberPro-Installer.exe" (
    echo 2. Distribute installer: VideoTranscriberPro-Installer.exe
) else (
    echo 2. Install NSIS to create installer
)
echo 3. Share with employees!
echo.
pause
