# Hebrew Learning App 🇮🇱

A desktop application for learning Hebrew vocabulary with confidence-based flashcards, audio pronunciation, and progress tracking.

## ✨ Features

### Learning System
- **300 Hebrew words** ranked by frequency (most common first)
- **4-level confidence rating** - Again/Hard/Good/Easy (inspired by spaced repetition)
- **Smart progress tracking** - Weighted confidence scores (70% old + 30% new)
- **Multiple study modes** - Top 50/100/200, all words, or custom ranges
- **Practice difficult words** - Review only Hard/Again words
- **Session statistics** - Track your improvement over time

### Audio & Interface
- **Native Hebrew audio** - macOS text-to-speech with Carmit voice
- **Dark mode** - Easy on the eyes for evening study
- **Keyboard shortcuts** - Numbers 1-4 or letters A/H/G/E for fast rating
- **Modern flat design** - Clean, distraction-free interface
- **Visible shortcuts** - On-screen hints for keyboard controls

### Data Management
- **Import vocabulary** - Add your own words from text files
- **Sort options** - By frequency, confidence, Hebrew/English alphabetically
- **Statistics view** - See confidence levels and top words
- **Auto-save progress** - Never lose your learning data

## 🚀 Quick Start

### For Development
```bash
cd /Users/josephkong/hebrew
conda activate test
pythonw hebrew_learning_app_modular.py
```

### For Distribution
See [SHARING.md](SHARING.md) for creating standalone app bundles.

## 📖 Using the App

### Study Session
1. **Menu: Study** → Choose difficulty (Top 50, 100, 200, All, or Custom Range)
2. Hebrew word + transliteration appears
3. Audio plays automatically (toggle in Settings if desired)
4. Try to recall the meaning
5. Press **Space** or click "Show Answer"
6. Rate your confidence: **1** (Again), **2** (Hard), **3** (Good), or **4** (Easy)

### Confidence Levels
- **Again (1)** 🔴 - Complete failure, couldn't recall at all
- **Hard (2)** 🟠 - Difficult, barely recalled with struggle  
- **Good (3)** 🟢 - Recalled with some effort, satisfactory
- **Easy (4)** ✅ - Perfect recall, very confident

### Keyboard Shortcuts
| Action | Keys |
|--------|------|
| Show Answer | Space |
| Again | 1 or A |
| Hard | 2 or H |
| Good | 3 or G |
| Easy | 4 or E |
| Play Audio | P |

### Vocabulary Management
- **Vocabulary → Add New Words** - Import from tab-separated text files
- **Vocabulary → View Statistics** - See your progress breakdown
- **Vocabulary → Sort by...** - Organize by frequency, confidence, or alphabetically

### Settings
- **Auto-play Audio** - Toggle automatic pronunciation
- **Dark Mode** - Switch theme for comfortable viewing
- **Reset Progress** - Start fresh (cannot be undone)

## 📁 Project Structure (Modular Design)

The app is organized into clean, maintainable modules:

```
hebrew/
├── hebrew_learning_app_modular.py  # Main orchestrator (400 lines)
├── config.py                       # Settings & themes (95 lines)
├── data_manager.py                 # Data I/O (140 lines)
├── audio_player.py                 # TTS audio (25 lines)
├── session_manager.py              # Session logic (95 lines)
├── ui_components.py                # UI helpers (200 lines)
├── hebrew_vocabulary.csv           # Vocabulary database
├── learning_progress.json          # Your progress
└── HebrewLearning.icns            # App icon
```

### Why Modular?
✅ Each file has one clear responsibility  
✅ Easy to find and fix bugs  
✅ Simple to add new features  
✅ Fits in AI context windows  
✅ Better code organization  

### Module Overview
- **config.py** - Paths, themes, constants
- **data_manager.py** - Load/save vocabulary & progress
- **audio_player.py** - Hebrew text-to-speech
- **session_manager.py** - Study session flow & statistics
- **ui_components.py** - Widget creation & dialogs
- **Main app** - Coordinates everything, handles UI events

## 💾 Data Storage

### Progress Tracking
- **Location:** `learning_progress.json` (development) or `~/.hebrew_learning/` (standalone app)
- **Auto-saved** after each word rating
- **Contains:** 
  - Easy/Good/Hard/Again word lists
  - Confidence scores (1.0-4.0 weighted averages)
  - Last session timestamp

### Vocabulary Database
- **File:** `hebrew_vocabulary.csv`
- **Format:** rank, english, transliteration, hebrew
- **Expandable:** Import additional words via Vocabulary menu

## 🔧 Development

### Requirements
- macOS 10.13+
- Python 3.11+ (conda recommended)
- Tkinter with pythonw support

### Running from Source
```bash
conda activate test
pythonw hebrew_learning_app_modular.py
```

### Building Standalone App
```bash
python -m PyInstaller HebrewLearning_modular.spec --clean --noconfirm
# Output: dist/HebrewLearning.app (~28 MB)
```

See [SHARING.md](SHARING.md) for distribution details.

## 💡 Tips for Learning

1. **Rate honestly** - Confidence system works best with truthful self-assessment
2. **Start with Top 50** - Most common words for fastest progress
3. **Use keyboard shortcuts** - Numbers 1-4 are faster than clicking
4. **Practice Hard/Again words** - Target your weak areas
5. **Check statistics regularly** - Track confidence score improvements
6. **Study daily** - Short consistent sessions beat cramming

## 🐛 Troubleshooting

**No audio pronunciation?**
- Check: System Settings → Accessibility → Spoken Content
- Ensure Carmit (Hebrew) voice is available
- May need to download Hebrew language pack

**Text not displaying?**
- Must use `pythonw` (not `python3`) on macOS
- Requires conda Python with python.app + tk packages
- System Python on macOS 15+ has deprecated Tkinter

**Standalone app won't open?**
- First time: Right-click → Open (not double-click)
- Or: System Settings → Privacy & Security → "Open Anyway"
- Fix Gatekeeper: `xattr -cr /path/to/HebrewLearning.app`

## 📚 Version History

**v2.5** (Current - Modular)
- ✅ Refactored into 6 clean modules
- ✅ 4-level confidence rating (Again/Hard/Good/Easy)
- ✅ Dark mode support
- ✅ Visible keyboard shortcuts in UI
- ✅ Custom range selection
- ✅ Confidence score tracking with weighted averages
- ✅ Enhanced statistics view

---

**Happy Learning! 📚✨**
