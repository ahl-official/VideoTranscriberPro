# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller build specification for Video Transcriber Pro
This file configures how the application is packaged into a Windows executable
"""

from PyInstaller.utils.hooks import copy_metadata

block_cipher = None

# Collect metadata for packages that use importlib.metadata
app_datas = []
app_datas += copy_metadata('imageio')
app_datas += copy_metadata('imageio_ffmpeg')
app_datas += copy_metadata('moviepy')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=app_datas,
    hiddenimports=[
        'assemblyai',
        'moviepy',
        'moviepy.editor',
        'moviepy.video.io.VideoFileClip',
        'moviepy.audio.io.AudioFileClip',
        'imageio',
        'imageio_ffmpeg',
        'decorator',
        'numpy',
        'tkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VideoTranscriberPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VideoTranscriberPro'
)
