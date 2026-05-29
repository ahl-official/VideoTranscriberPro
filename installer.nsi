; NSIS Installer Script for Video Transcriber Pro
; This script creates a professional Windows installer (.exe)

;================================
; INCLUDES & SETTINGS
;================================

!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"

;================================
; APPLICATION INFO
;================================

Name "Video Transcriber Pro"
OutFile "VideoTranscriberPro-Installer.exe"
InstallDir "$PROGRAMFILES\VideoTranscriberPro"

; Request admin privileges
RequestExecutionLevel admin

;================================
; MUI SETTINGS
;================================

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

;================================
; INSTALLER SECTION
;================================

Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Copy application files
    File /r "dist\VideoTranscriberPro\*.*"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Create Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\VideoTranscriberPro"
    CreateShortcut "$SMPROGRAMS\VideoTranscriberPro\Video Transcriber Pro.lnk" "$INSTDIR\VideoTranscriberPro.exe"
    CreateShortcut "$SMPROGRAMS\VideoTranscriberPro\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    
    ; Create Desktop shortcut
    CreateShortcut "$DESKTOP\Video Transcriber Pro.lnk" "$INSTDIR\VideoTranscriberPro.exe"
    
    ; Write registry entries for uninstall
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoTranscriberPro" \
                 "DisplayName" "Video Transcriber Pro"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoTranscriberPro" \
                 "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoTranscriberPro" \
                 "DisplayVersion" "1.0.0"
    
    MessageBox MB_OK "Video Transcriber Pro installed successfully!$\n$\nYou'll find shortcuts on your Desktop and Start Menu."
SectionEnd

;================================
; UNINSTALLER SECTION
;================================

Section "Uninstall"
    ; Remove application directory
    RMDir /r "$INSTDIR"
    
    ; Remove Start Menu shortcuts
    RMDir /r "$SMPROGRAMS\VideoTranscriberPro"
    
    ; Remove Desktop shortcut
    Delete "$DESKTOP\Video Transcriber Pro.lnk"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoTranscriberPro"
    
    MessageBox MB_OK "Video Transcriber Pro uninstalled successfully!"
SectionEnd
