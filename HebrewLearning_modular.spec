# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Hebrew Learning App (Modular Version)
Creates standalone macOS .app bundle
"""

block_cipher = None

a = Analysis(
    ['hebrew_learning_app_modular.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('HebrewLearning.icns', '.'),
    ],
    hiddenimports=[
        'config',
        'data_manager',
        'audio_player',
        'session_manager',
        'ui_components'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='HebrewLearning',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    name='HebrewLearning',
)

app = BUNDLE(
    coll,
    name='HebrewLearning.app',
    icon='HebrewLearning.icns',
    bundle_identifier='com.hebrewlearning.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleName': 'Hebrew Learning',
        'CFBundleDisplayName': 'Hebrew Learning',
        'CFBundleShortVersionString': '2.5',
        'CFBundleVersion': '2.5.0',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
    },
)
