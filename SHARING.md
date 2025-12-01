# 📦 Sharing the Hebrew Learning App

## ✅ Ready to Distribute!

The app is fully standalone and can be shared with other Mac users. No Python, conda, or technical setup required by recipients!

---

## 🎯 What to Share

Choose **ONE** of these options:

### Option 1: DMG Installer ⭐ **RECOMMENDED**
- **File:** `HebrewLearning.dmg` (~14 MB compressed)
- **Create:** `hdiutil create -volname "Hebrew Learning" -srcfolder dist/HebrewLearning.app -ov -format UDZO dist/HebrewLearning.dmg`
- **Best for:** Professional distribution, download links
- **User experience:** Double-click → Drag to Applications

### Option 2: Standalone App Bundle
- **File:** `HebrewLearning.app` (~28 MB)
- **Location:** `/Users/josephkong/hebrew/dist/HebrewLearning.app`
- **Best for:** AirDrop, USB drives, cloud storage
- **User experience:** Copy anywhere → Double-click to run

### Option 3: Compressed Zip
- **Create:** `cd dist && zip -r HebrewLearning.zip HebrewLearning.app`
- **Size:** ~15-20 MB compressed
- **Best for:** Email attachments, web downloads
- **User experience:** Unzip → Run .app file

---

## 📋 Instructions for Recipients

Copy and paste these instructions to share with users:

```
🎓 Hebrew Learning App - Installation Guide

REQUIREMENTS:
✅ macOS 10.13 (High Sierra) or later
✅ 50 MB free disk space
✅ No Python installation needed!

INSTALLATION:
1. Download HebrewLearning.dmg (or unzip HebrewLearning.zip)
2. Drag HebrewLearning.app to Applications folder (or anywhere)
3. Double-click to launch

⚠️ FIRST TIME ONLY - Security Warning:
If you see "can't be opened because it is from an unidentified developer":
  → Right-click the app → Select "Open"
  → Click "Open" in the confirmation dialog
  → App will now open normally in the future

Or fix via terminal:
  xattr -cr /Applications/HebrewLearning.app

FEATURES:
• 300 Hebrew words ranked by frequency
• Audio pronunciation (built-in Hebrew TTS)
• 4-level confidence rating system (Again/Hard/Good/Easy)
• Dark mode support
• Auto-saved progress to ~/.hebrew_learning/
• Keyboard shortcuts: 1-4 for rating, Space for answer

USAGE:
1. Choose session type from Study Mode menu
2. Rate your confidence for each word (1-4)
3. Progress saves automatically
4. View statistics: Session → Show Statistics
```

---

## 🔧 Building the App Yourself

If you need to rebuild the standalone app:

### Prerequisites
```bash
# Ensure Python 3.11+ with conda
conda activate test

# Install PyInstaller
pip install pyinstaller==6.17.0
```

### Build Command
```bash
cd /Users/josephkong/hebrew
python -m PyInstaller HebrewLearning_modular.spec --clean --noconfirm
```

**Output:** `dist/HebrewLearning.app` (~28 MB)

### What Gets Bundled
- ✅ Python 3.11 interpreter
- ✅ Tkinter + tcl/tk libraries
- ✅ All Python modules (config, data_manager, audio_player, session_manager, ui_components)
- ✅ Hebrew vocabulary CSV (300 words)
- ✅ App icon (.icns)

---

## 💾 How User Data Works

### Standalone App Behavior
Each user's data is stored independently in their home directory:

**Progress File:**
```
~/.hebrew_learning/learning_progress.json
```

**Custom Vocabulary (if imported):**
```
~/.hebrew_learning/hebrew_vocabulary.csv
```

### Multi-User Support
- ✅ Each macOS user has separate progress
- ✅ No data conflicts if multiple users on same Mac
- ✅ Progress syncs if user signs in on different Mac (via iCloud Drive if enabled)

---

## 🎵 Audio Pronunciation

Uses macOS built-in text-to-speech with **Carmit (Hebrew)** voice.

### Requirements
- macOS with Hebrew language support (included by default on modern macOS)
- System Settings → Accessibility → Spoken Content → Voices

### Troubleshooting
**No audio playing?**
1. Check: System Settings → Accessibility → Spoken Content
2. Ensure "Carmit" voice is available
3. May need to download: System Settings → General → Language & Region → Add Hebrew

**Audio works in development but not standalone app?**
- This should not happen - PyInstaller bundles everything
- If it does, check macOS Gatekeeper isn't blocking: `xattr -cr HebrewLearning.app`

---

## 🔒 Security & Trust

### Gatekeeper Warning (First Launch)
macOS protects users from unsigned apps. Recipients will see:

> "HebrewLearning.app can't be opened because it is from an unidentified developer"

**Why?** The app isn't signed with an Apple Developer Certificate ($99/year).

**Solutions for Users:**

**Method 1: Right-Click Open** (Recommended)
1. Right-click (or Control+click) → Open
2. Click "Open" in confirmation dialog
3. macOS remembers this choice forever

**Method 2: System Settings**
1. Try to open normally
2. System Settings → Privacy & Security
3. Click "Open Anyway" next to security message

**Method 3: Terminal Command** (Advanced)
```bash
xattr -cr /Applications/HebrewLearning.app
```

### Code Signing (Optional)
If you have an Apple Developer account:
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/HebrewLearning.app
```

Then notarize:
```bash
xcrun notarytool submit dist/HebrewLearning.app --keychain-profile "notary-profile" --wait
xcrun stapler staple dist/HebrewLearning.app
```

---

## 📊 Distribution Methods

### Cloud Storage
- **Google Drive:** Share link, ~14 MB DMG
- **Dropbox:** Public link, right-click → Copy Dropbox Link
- **iCloud Drive:** Share folder or link
- **OneDrive/Box:** Similar sharing options

### Direct Transfer
- **AirDrop:** Select .app or .dmg → Share → AirDrop
- **USB Drive:** Copy HebrewLearning.app directly
- **Network Share:** SMB/AFP file sharing

### Email
- **Attach .zip** (~15-20 MB)
- **Or share cloud link** (recommended for DMG)

### Website/GitHub
- Upload DMG to Releases
- Link directly for download
- Include README with instructions

---

## 🐛 Common Issues & Solutions

### "App is damaged and can't be opened"
**Cause:** Gatekeeper quarantine attribute from download
**Fix:** `xattr -cr /Applications/HebrewLearning.app`

### "App can't be opened because Apple cannot check it for malicious software"
**Cause:** Unsigned app, macOS Big Sur+
**Fix:** Right-click → Open (first time only)

### App won't launch (no error)
**Cause:** Missing Python dependencies or corrupt bundle
**Fix:** Rebuild app with `--clean` flag: `python -m PyInstaller HebrewLearning_modular.spec --clean --noconfirm`

### App crashes immediately
**Cause:** Corrupted .app during copy/transfer
**Fix:** Re-download or re-copy the app

### Progress not saving
**Cause:** Permissions issue creating ~/.hebrew_learning/
**Fix:** Manually create: `mkdir -p ~/.hebrew_learning && chmod 755 ~/.hebrew_learning`

---

## 📈 File Sizes Reference

| File | Size | Notes |
|------|------|-------|
| HebrewLearning.app | ~28 MB | Full uncompressed bundle |
| HebrewLearning.dmg | ~14 MB | Compressed installer |
| HebrewLearning.zip | ~15-20 MB | Compressed archive |
| Source code | <100 KB | All .py files combined |

---

**Ready to share! 🎉**
