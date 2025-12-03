# Hebrew Learning App - Developer Guide 🔧

Complete technical documentation for developers, maintainers, and contributors.

---

## 📋 Table of Contents

1. [Project Architecture](#project-architecture)
2. [UI Customization](#ui-customization)
3. [Database Structure](#database-structure)
4. [Building & Distribution](#building--distribution)
5. [Development Setup](#development-setup)
6. [Adding Features](#adding-features)

---

## 🏗️ Project Architecture

### Modular Design Philosophy

The app is organized into clean, single-responsibility modules (each under 200 lines):

```
hebrew/
├── hebrew_learning_app_modular.py  # Main orchestrator (400 lines)
├── config.py                       # App metadata & file paths
├── database_manager.py             # SQLite operations (450 lines)
├── data_manager.py                 # Vocabulary & progress (140 lines)
├── audio_player.py                 # TTS audio (25 lines)
├── session_manager.py              # Study session logic (250 lines)
├── ui_components.py                # UI widgets & themes (800 lines)
├── inspect_database.py             # Database explorer utility
├── hebrew_vocabulary.db            # SQLite database (40 KB)
├── hebrew_vocabulary.csv           # Legacy data (kept for reference)
├── learning_progress.json          # Legacy progress (kept for backup)
└── HebrewLearning.icns            # App icon
```

### Why Modular?
✅ Each file has one clear responsibility  
✅ Easy to locate and fix bugs  
✅ Simple to add new features  
✅ Fits in AI context windows  
✅ Better testability  
✅ Scalable architecture

---

## 🎨 UI Customization

### All UI Configuration in One Place

**File:** `ui_components.py` (lines 1-180)

Everything visual is centralized:
- Layout spacing and padding
- Font families, sizes, weights
- Color schemes (light/dark themes)
- Border radius, dimensions
- Widget sizing

### UIConfig Class (Lines ~15-120)

All layout measurements in one place:

```python
class UIConfig:
    # ===== TEXT BOXES =====
    TEXT_BOX_VERTICAL_SPACING = 4        # Space between boxes
    TEXT_BOX_HORIZONTAL_PADDING = 12     # Side padding
    TEXT_BOX_BORDER_RADIUS = 12          # Corner roundness
    TEXT_BOX_REL_HEIGHT = 0.3            # Box height (0.0-1.0)
    
    # ===== FONTS =====
    HEBREW_FONT_SIZE = 36
    TRANS_FONT_SIZE = 18
    ENGLISH_FONT_SIZE = 20
    
    # ===== BUTTONS =====
    MAIN_BUTTON_PADX = 18
    MAIN_BUTTON_PADY = 8
    BUTTON_BORDER_RADIUS = 8
```

### Themes Class (Lines ~122-158)

All colors for light and dark modes:

```python
class Themes:
    LIGHT = {
        'bg': '#f0f0f0',                 # Main background
        'card_bg': '#ffffff',            # Card background
        'text_bg': '#f8f9fa',            # Hebrew box
        'text_fg': '#2c3e50',            # Hebrew text
        'trans_bg': '#e3f2fd',           # Trans box (blue)
        'english_bg': '#e8f5e9',         # English box (green)
        'btn_again': '#e57373',          # Again button (red)
        'btn_easy': '#81c784',           # Easy button (green)
        # ... more colors
    }
    
    DARK = {
        # Dark theme colors
    }
```

### Quick Customizations

#### Make Text Boxes Shorter
```python
TEXT_BOX_REL_HEIGHT = 0.3  # Try: 0.2 (shorter) or 0.5 (taller)
```

#### Change Hebrew Font Size
```python
HEBREW_FONT_SIZE = 36  # Try: 40 (bigger) or 30 (smaller)
```

#### Adjust Box Spacing
```python
TEXT_BOX_VERTICAL_SPACING = 4  # Try: 8 (more space) or 2 (less)
```

#### Change Colors (Light Mode)
```python
'text_bg': '#f8f9fa',      # Try: '#ffffff' (pure white)
'trans_bg': '#e3f2fd',     # Try: '#fff9c4' (yellow)
```

#### Adjust Corner Roundness
```python
CARD_BORDER_RADIUS = 20       # Main card corners
TEXT_BOX_BORDER_RADIUS = 12   # Text box corners
BUTTON_BORDER_RADIUS = 8      # Button corners

# Try: 30 (very round), 5 (slightly round), 0 (sharp corners)
```

### No More Scattered UI Code!

**Before:** UI settings spread across multiple files  
**After:** Everything in `ui_components.py` UIConfig and Themes classes

---

## 🗄️ Database Structure

### SQLite Database Schema

**File:** `hebrew_vocabulary.db` (40 KB)

#### Table 1: lemmas
Core vocabulary entries
```sql
CREATE TABLE lemmas (
    lemma_id INTEGER PRIMARY KEY,
    lemma TEXT NOT NULL,              -- Hebrew word
    part_of_speech TEXT,              -- noun, verb, adjective, etc.
    transliteration TEXT,             -- Romanized pronunciation
    english TEXT,                     -- English meaning
    register TEXT,                    -- "biblical", "modern", "both"
    notes TEXT,                       -- Optional notes
    root TEXT,                        -- 3-letter Hebrew root
    audio_path TEXT,                  -- Future: audio file path
    frequency_rank INTEGER            -- Frequency sorting
);
```

#### Table 2: variants
Word forms (plurals, conjugations, gender)
```sql
CREATE TABLE variants (
    variant_id INTEGER PRIMARY KEY,
    lemma_id INTEGER NOT NULL,
    form TEXT NOT NULL,               -- The variant form
    description TEXT,                 -- "plural", "fem singular", etc.
    FOREIGN KEY (lemma_id) REFERENCES lemmas
);
```

#### Table 3: categories
Thematic groupings
```sql
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE                  -- "Verbs", "Biblical", etc.
);
```

#### Table 4: lemma_categories
Many-to-many link between lemmas and categories
```sql
CREATE TABLE lemma_categories (
    lemma_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (lemma_id, category_id),
    FOREIGN KEY (lemma_id) REFERENCES lemmas,
    FOREIGN KEY (category_id) REFERENCES categories
);
```

#### Table 5: translations
Cross-language translations
```sql
CREATE TABLE translations (
    translation_id INTEGER PRIMARY KEY,
    lemma_id INTEGER NOT NULL,
    language TEXT NOT NULL,           -- "Greek", "Arabic", etc.
    translation TEXT NOT NULL,
    FOREIGN KEY (lemma_id) REFERENCES lemmas
);
```

#### Table 6: user_progress
Learning progress with SRS
```sql
CREATE TABLE user_progress (
    lemma_id INTEGER PRIMARY KEY,
    familiarity INTEGER,              -- 1-4 (Again/Hard/Good/Easy)
    easiness REAL,                    -- SRS factor (1.3-3.0)
    interval INTEGER,                 -- Days until next review
    last_reviewed DATE,
    next_review DATE,
    streak INTEGER,                   -- Consecutive successes
    FOREIGN KEY (lemma_id) REFERENCES lemmas
);
```

### Database Manager API

**File:** `database_manager.py`

Key methods:

```python
class DatabaseManager:
    def __init__(self, db_path):
        # Initializes connection, creates tables
        
    def populate_sample_data(self):
        # Inserts 30 sample words (first run only)
        
    def get_all_vocabulary(self):
        # Returns all vocabulary as list of dicts
        
    def get_lemma_variants(self, lemma_id):
        # Get all forms of a word
        
    def get_lemma_categories(self, lemma_id):
        # Get categories for a word
        
    def update_progress(self, lemma_id, familiarity, easiness, interval):
        # Update user progress with SRS
        
    def get_vocabulary_stats(self):
        # Get statistics (count by familiarity level)
```

### Querying the Database

Use the included `inspect_database.py` script:

```bash
python3 inspect_database.py
```

Or query directly:

```bash
sqlite3 hebrew_vocabulary.db

# List tables
.tables

# See table structure
.schema lemmas

# Query data
SELECT * FROM lemmas WHERE register = 'biblical';
SELECT l.lemma, c.name FROM lemmas l 
  JOIN lemma_categories lc ON l.lemma_id = lc.lemma_id
  JOIN categories c ON lc.category_id = c.category_id;
```

---

## 📦 Building & Distribution

### Creating Standalone App

The app uses PyInstaller to create a macOS `.app` bundle.

#### Build Script

**File:** `build_app.sh` (or run commands manually)

```bash
# Clean previous builds
rm -rf build dist

# Build with PyInstaller
pyinstaller --clean \
    --name="HebrewLearning" \
    --windowed \
    --icon=HebrewLearning.icns \
    --add-data="hebrew_vocabulary.db:." \
    --add-data="HebrewLearning.icns:." \
    --osx-bundle-identifier="com.hebrewlearning.app" \
    hebrew_learning_app_modular.py

# Result: dist/HebrewLearning.app
```

#### What Gets Bundled
- Python interpreter
- All dependencies (tkinter, sqlite3)
- Vocabulary database
- App icon
- All Python modules

#### Distribution Options

**Option 1: DMG Installer** (Recommended)
```bash
hdiutil create -volname "Hebrew Learning" \
    -srcfolder dist/HebrewLearning.app \
    -ov -format UDZO \
    dist/HebrewLearning.dmg
```

**Option 2: Zip Archive**
```bash
cd dist
zip -r HebrewLearning.zip HebrewLearning.app
```

**Option 3: Direct App**
Just share `dist/HebrewLearning.app` folder

### First-Run Security

Users need to bypass Gatekeeper (first time only):
1. Right-click → Open
2. Click "Open" in security dialog
3. Or: System Preferences → Security & Privacy → Allow

### Code Signing (Optional)

For proper distribution without security warnings:

```bash
# Requires Apple Developer account
codesign --deep --force --sign "Developer ID Application: Your Name" \
    dist/HebrewLearning.app

# Verify
codesign --verify --verbose dist/HebrewLearning.app
```

---

## 💻 Development Setup

### Requirements
- macOS 10.13+
- Python 3.8+
- Conda (recommended) or venv

### Installation

```bash
# Clone repository
git clone https://github.com/Captain-JKong/HebrewLearning.git
cd HebrewLearning

# Create conda environment
conda create -n hebrew python=3.9
conda activate hebrew

# No additional packages needed (uses standard library)
# tkinter, sqlite3 come with Python

# Run app
pythonw hebrew_learning_app_modular.py
```

### Development vs. Production

**Development Mode:**
- Run with `pythonw` (enables GUI on macOS)
- Database and progress in same directory
- Easy debugging and testing

**Production Mode (Bundled):**
- Runs as standalone .app
- Database bundled inside .app
- Progress saved to user's home directory

### File Paths Logic

**File:** `config.py`

```python
@staticmethod
def get_paths():
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        base_path = Path(sys._MEIPASS)
        progress_dir = Path.home() / '.hebrew_learning'
    else:
        # Running as script
        base_path = Path(__file__).parent
        progress_file = base_path / 'learning_progress.json'
    
    return {
        'vocab': base_path / 'hebrew_vocabulary.db',
        'progress': progress_file,
        'icon': base_path / 'HebrewLearning.icns'
    }
```

---

## 🔧 Adding Features

### Adding a New Study Mode

1. **Add session method** in `session_manager.py`:

```python
def start_my_new_mode(self, params):
    """My new study mode description"""
    self.session_mode = "My New Mode"
    
    # Filter vocabulary based on criteria
    self.current_words = [w for w in self.vocabulary if ...]
    
    # Optional: sort, shuffle
    random.shuffle(self.current_words)
    
    self._reset_session()
    return len(self.current_words)
```

2. **Add menu item** in `hebrew_learning_app_modular.py`:

```python
def create_menu(self):
    # ... existing code ...
    study_menu.add_command(
        label="My New Mode",
        command=self.start_my_new_mode
    )
```

3. **Add handler** in `hebrew_learning_app_modular.py`:

```python
def start_my_new_mode(self):
    """Start my new mode session"""
    count = self.session.start_my_new_mode(params)
    if count == 0:
        messagebox.showinfo("My Mode", "No words found!")
        return
    self.progress_label.config(text=f"My New Mode: {count} words")
    self.show_next_word()
```

### Adding New Database Fields

1. **Modify schema** in `database_manager.py`:

```python
cursor.execute('''
    ALTER TABLE lemmas ADD COLUMN my_field TEXT
''')
```

2. **Update data population**:

```python
lemmas_data = [
    (1, 'שלום', ..., 'my_value'),  # Add to tuple
    ...
]
```

3. **Update queries** to include new field:

```python
SELECT lemma, my_field FROM lemmas WHERE ...
```

### Adding UI Elements

1. **Define in UIConfig** (`ui_components.py`):

```python
class UIConfig:
    MY_WIDGET_PADDING = 10
    MY_WIDGET_FONT_SIZE = 14
```

2. **Add to build_complete_interface**:

```python
def build_complete_interface(self, callbacks):
    # ... existing widgets ...
    
    widgets['my_widget'] = self.create_button(
        parent,
        "My Widget",
        callbacks['my_action'],
        self.theme['my_color'],
        padx=UIConfig.MY_WIDGET_PADDING
    )
    
    return widgets
```

3. **Add callback**:

```python
callbacks = {
    'my_action': self.my_action_handler,
    # ... existing callbacks
}
```

### Adding Themes

1. **Define colors** in `ui_components.py`:

```python
class Themes:
    MY_THEME = {
        'bg': '#color1',
        'card_bg': '#color2',
        # ... all required colors
    }
```

2. **Add to get_theme**:

```python
@staticmethod
def get_theme(mode='light'):
    if mode == 'my_theme':
        return Themes.MY_THEME
    # ... existing logic
```

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] All study modes work
- [ ] Progress saves correctly
- [ ] Audio plays on macOS
- [ ] Keyboard shortcuts respond
- [ ] Theme toggle works
- [ ] Statistics display correctly
- [ ] Database queries succeed
- [ ] Import vocabulary works

### Database Integrity

```bash
# Check database integrity
sqlite3 hebrew_vocabulary.db "PRAGMA integrity_check;"

# View all data
python3 inspect_database.py

# Test specific queries
sqlite3 hebrew_vocabulary.db "SELECT COUNT(*) FROM lemmas;"
```

### PyInstaller Testing

```bash
# Build
pyinstaller hebrew_learning_app_modular.spec

# Test bundle
open dist/HebrewLearning.app

# Check for errors
dist/HebrewLearning.app/Contents/MacOS/HebrewLearning
```

---

## 📊 Performance Considerations

### Database
- SQLite handles thousands of words efficiently
- Indexes on frequently queried fields (frequency_rank, register)
- Connection pooling for multiple queries

### UI
- Canvas-based rounded buttons for modern look
- Minimal redraws - only changed elements
- Theme switching without restart

### Memory
- Vocabulary loaded once at startup
- Progress updated incrementally
- No heavy libraries (pure Python + tkinter)

---

## 🔐 Data Privacy

### What's Stored
- Vocabulary database (read-only for users)
- User progress (local SQLite)
- No network requests
- No telemetry
- No cloud sync

### Data Location
- **Development:** Same directory as script
- **Production:** `~/.hebrew_learning/`

### Backup & Export
- Copy `hebrew_vocabulary.db` for full backup
- Contains all vocabulary + progress
- Import/export functionality available

---

## 🐛 Debugging

### Enable Debug Output

```python
# Add to main()
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

**Import Errors:**
- Check Python path
- Verify module structure
- Ensure `__init__.py` if using packages

**Database Errors:**
- Check file permissions
- Verify schema matches code
- Use `PRAGMA integrity_check`

**UI Not Appearing:**
- Use `pythonw` not `python` on macOS
- Check tkinter installation: `python -m tkinter`

**Audio Not Working:**
- Verify macOS TTS voices installed
- Check Accessibility settings
- Test with: `say -v Carmit "שלום"`

---

## 📝 Code Style

### Python Conventions
- PEP 8 style guide
- Type hints where helpful
- Docstrings for public methods
- Clear variable names

### Module Organization
```python
"""
Module docstring explaining purpose
"""

# Imports (stdlib, third-party, local)
import standard_library
from third_party import module
from local import module

# Constants
CONSTANT_NAME = value

# Classes
class MyClass:
    """Class docstring"""
    pass

# Functions
def my_function():
    """Function docstring"""
    pass

# Main execution
if __name__ == '__main__':
    main()
```

---

## 🚀 Future Enhancements

### Potential Features
- [ ] Root family study mode
- [ ] Custom SRS interval tuning
- [ ] Statistics by category
- [ ] Export progress reports
- [ ] Import from various formats
- [ ] Audio file support (Windows)
- [ ] Multi-language UI
- [ ] Cloud sync (optional)
- [ ] Mobile companion app
- [ ] Anki deck export

### Scalability
- Database handles 10,000+ words easily
- UI optimized for large vocabularies
- Paginated results for huge datasets
- Lazy loading for better performance

---

## 📚 Resources

### Documentation
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)

### Spaced Repetition
- [SuperMemo Algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2)
- [Anki SRS Implementation](https://faqs.ankiweb.net/what-spaced-repetition-algorithm.html)

### Hebrew Resources
- [Hebrew Root System](https://en.wikipedia.org/wiki/Hebrew_root)
- [Modern vs Biblical Hebrew](https://en.wikipedia.org/wiki/Modern_Hebrew)

---

## 🤝 Contributing

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Make changes with clear commits
4. Test thoroughly
5. Submit PR with description

### Coding Standards
- Follow existing code style
- Add docstrings to new functions
- Update relevant documentation
- Test on macOS before submitting

---

## 📄 License

See LICENSE file in repository.

---

## ✅ Developer Checklist

Before committing:
- [ ] Code follows style guide
- [ ] All functions documented
- [ ] UI customizations in UIConfig
- [ ] Database changes documented
- [ ] Tested manually
- [ ] No debug print statements
- [ ] Updated relevant docs
- [ ] Git commit message clear

Before release:
- [ ] Version number updated
- [ ] Changelog updated
- [ ] PyInstaller build succeeds
- [ ] App bundle tested
- [ ] User guide updated
- [ ] Sample data verified

---

**Happy coding! 🚀**

If you improve the app, consider sharing your enhancements with the community!
