# 📝 Hebrew Learning App - Version History

## Version 2.5 - Modular Architecture (Current)

### 🏗️ Major Refactoring
**Refactored from 946-line monolith into 6 clean modules:**
- `config.py` (95 lines) - Configuration, paths, themes
- `data_manager.py` (140 lines) - File I/O, vocabulary & progress management
- `audio_player.py` (25 lines) - Hebrew text-to-speech via macOS
- `session_manager.py` (95 lines) - Study session logic, statistics
- `ui_components.py` (200 lines) - Reusable widgets, dialogs, themes
- `hebrew_learning_app_modular.py` (400 lines) - Main orchestrator

**Benefits:**
- ✅ Each module under 200 lines for better maintainability
- ✅ Clear separation of concerns (config/data/audio/session/UI)
- ✅ Easier to debug and extend
- ✅ Fits in AI context windows for better assistance
- ✅ Standalone PyInstaller build support

### 🎯 4-Level Confidence System
Upgraded from binary (knew/didn't know) to confidence-based ratings:

1. **Again (1)** 🔴 - Complete failure, couldn't recall
2. **Hard (2)** 🟠 - Difficult, barely recalled with struggle  
3. **Good (3)** 🟢 - Recalled with some effort
4. **Easy (4)** ✅ - Perfect recall, very confident

**Smart Scoring:**
- Weighted averages: 70% previous score + 30% new rating
- Smooths out occasional mistakes while tracking improvement
- Confidence score range: 1.0-4.0 for each word

### ⌨️ Enhanced Keyboard Shortcuts
**Visible in UI with dual input methods:**

| Action | Number Key | Letter Key | Description |
|--------|------------|------------|-------------|
| Again | `1` | `A` | Didn't know at all |
| Hard | `2` | `H` | Struggled to recall |
| Good | `3` | `G` | Recalled successfully |
| Easy | `4` | `E` | Perfect confidence |
| Show Answer | `Space` | - | Reveal translation |
| Play Audio | `P` | - | Replay pronunciation |

### 🎨 Visual Improvements
- **Dark Mode** - Toggle via Settings menu
- **Rounded corners** - Clean, modern design
- **Flat interface** - Removed gray borders and separators
- **App icon** - Custom .icns icon for professional appearance

### 📊 Enhanced Statistics
- Confidence score tracking and visualization
- Easy/Good/Hard/Again word counts
- Most practiced words list
- Session time tracking
- Progress percentage by confidence level

### 📖 Vocabulary Features
**Sorting Options:**
- Frequency (most common first)
- Confidence (highest scores first)
- Hebrew alphabetically
- English alphabetically

**Session Types:**
- Top 50/100/150/200/300
- Custom range selection
- Practice Hard/Again words only
- Practice specific confidence levels

**Import Custom Words:**
- Vocabulary → Add New Words from File
- Tab-separated format: `rank\tenglish\ttransliteration\thebrew`

### 💾 Data Storage
**Development mode:**
- `learning_progress.json` (in project directory)
- `hebrew_vocabulary.csv` (in project directory)

**Standalone app:**
- `~/.hebrew_learning/learning_progress.json`
- `~/.hebrew_learning/hebrew_vocabulary.csv` (if custom words imported)

**Progress file structure:**
```json
{
  "easy": [...],
  "good": [...],
  "hard": [...],
  "again": [...],
  "confidence_scores": {"word": 3.5, ...}
}
```

---

## Version 2.0 - Progress Tracking

### Features Added
- ✅ 3-level tracking system (Knew/Seen/Didn't Know)
- ✅ Binary knew/didn't-know marking
- ✅ Familiarity counting (how many times marked as "known")
- ✅ Statistics view showing progress breakdown
- ✅ Sort by familiarity

### Progress Structure
```json
{
  "known": [...],
  "partial": [...],
  "unknown": [...],
  "familiarity_counts": {"word": 3, ...}
}
```

---

## Version 1.0 - Initial Release

### Core Features
- ✅ 300 Hebrew words ranked by frequency
- ✅ Hebrew text-to-speech audio (Carmit voice)
- ✅ Session-based study modes (Top 50, 100, etc.)
- ✅ CSV vocabulary database
- ✅ Tkinter GUI with pythonw
- ✅ Show/hide answer functionality
- ✅ Basic keyboard shortcuts (Y/N)

### Initial Structure
- Single `hebrew_learning_app.py` file (~946 lines)
- `hebrew_vocabulary.csv` database
- Manual .app bundle creation script
- Basic light mode interface

---

## Comparison Matrix

| Feature | v1.0 | v2.0 | v2.5 |
|---------|------|------|------|
| Architecture | Monolith (946 lines) | Monolith | Modular (6 files) |
| Progress System | None | 3-level | 4-level confidence |
| Scoring | None | Binary | Weighted averages |
| Keyboard Shortcuts | Y/N | Y/N | 1-4 + A/H/G/E (visible) |
| Dark Mode | ❌ | ❌ | ✅ |
| Custom Vocabulary | ❌ | ❌ | ✅ |
| Statistics | ❌ | Basic | Detailed confidence |
| Standalone Build | Manual bundle | Manual bundle | PyInstaller .spec |
| File Structure | Project dir | Project dir | ~/.hebrew_learning/ |
| Sorting Options | 1 (frequency) | 2 (freq + familiarity) | 4 (freq/conf/alpha) |

---

## Migration Notes

### From v2.0 to v2.5
**Progress file auto-migrates:**
- Old `known/partial/unknown` → New `easy/good/hard/again`
- Familiarity counts → Confidence scores (converted)
- No manual migration needed

**File structure changes:**
- Development: No change (still in project dir)
- Standalone app: Moves to `~/.hebrew_learning/`

**Interface changes:**
- Y/N shortcuts → 1-4 number keys
- New dark mode option in Settings
- Confidence scores visible in statistics

### From v1.0 to v2.0
**No progress file:**
- Fresh start with `learning_progress.json` auto-created
- All words start as "unknown"

---

## Roadmap Ideas (Future)

**Potential v3.0 features:**
- 🔄 Spaced repetition scheduling (Anki-style intervals)
- 📱 Mobile app version (React Native/Flutter)
- 🔊 Record and compare pronunciation
- 📚 Multiple vocabulary decks
- 🌐 Web-based version
- 👥 Multi-user profiles
- 📈 Learning analytics dashboard
- 🎯 Custom study goals and streaks
- 🔗 Sync across devices (cloud storage)

---

**Current version: 2.5** | Last updated: 2024
