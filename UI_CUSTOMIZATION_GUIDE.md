# UI Customization Guide

## Overview
All UI-related configuration has been centralized in `ui_components.py` for easy customization. You no longer need to search through multiple files to adjust colors, fonts, spacing, or sizes.

---

## Where to Find What

### 📍 **ui_components.py** - ALL UI Configuration (Lines 1-180)

This file now contains **EVERYTHING** related to the visual appearance:

#### 1. **UIConfig Class** (Lines ~15-120)
Contains all layout measurements, spacing, fonts, and dimensions.

**Common Adjustments:**

```python
# ===== TEXT BOXES =====
TEXT_BOX_VERTICAL_SPACING = 4        # Space between Hebrew/Trans/English boxes
TEXT_BOX_HORIZONTAL_PADDING = 12     # Side padding for text boxes
TEXT_BOX_BORDER_RADIUS = 12          # Corner roundness (0 = square, higher = rounder)
TEXT_BOX_REL_HEIGHT = 0.3            # Box height (0.1-1.0, smaller = shorter)

# ===== HEBREW TEXT =====
HEBREW_FONT_SIZE = 36                # Size of Hebrew text
HEBREW_FONT_WEIGHT = 'bold'          # 'normal', 'bold', or 'italic'

# ===== TRANSLITERATION =====
TRANS_FONT_SIZE = 18                 # Size of transliteration

# ===== ENGLISH TEXT =====
ENGLISH_FONT_SIZE = 20               # Size of English text

# ===== BUTTONS =====
CARD_BORDER_RADIUS = 20              # Main card corner roundness
BUTTON_BORDER_RADIUS = 8             # Button corner roundness
MAIN_BUTTON_PADX = 18                # Button width padding
MAIN_BUTTON_PADY = 8                 # Button height padding
```

#### 2. **Themes Class** (Lines ~122-158)
Contains all color definitions for light and dark modes.

**Color Scheme:**

```python
LIGHT = {
    'bg': '#f0f0f0',                 # Main window background
    'card_bg': '#ffffff',            # White card background
    'text_bg': '#f8f9fa',            # Hebrew box background
    'text_fg': '#2c3e50',            # Hebrew text color
    'trans_bg': '#e3f2fd',           # Transliteration box (blue tint)
    'trans_fg': '#1565c0',           # Transliteration text (blue)
    'english_bg': '#e8f5e9',         # English box (green tint)
    'english_fg': '#2e7d32',         # English text (green)
    'btn_audio': '#607d8b',          # Audio button (gray)
    'btn_answer': '#78909c',         # Show Answer button (lighter gray)
    'btn_again': '#e57373',          # Again button (red)
    'btn_hard': '#ffb74d',           # Hard button (orange)
    'btn_good': '#aed581',           # Good button (light green)
    'btn_easy': '#81c784'            # Easy button (green)
}
```

#### 3. **UIBuilder Class** (Lines ~160-600)
Contains the actual widget creation methods. You shouldn't need to modify this unless adding new features.

---

### 📍 **config.py** - App Settings Only
Now contains **ONLY** non-visual settings:
- App name and version
- Window width/height (basic size)
- File paths
- **NO colors, fonts, or spacing anymore!**

---

### 📍 **hebrew_learning_app_modular.py** - Business Logic Only
Contains **ONLY** application logic:
- Menu creation
- Session management
- Progress tracking
- **NO UI creation code anymore!**

The entire interface is created with one simple call:
```python
widgets = self.ui_builder.build_complete_interface(callbacks)
```

---

## How to Make Common Adjustments

### Make Text Boxes Shorter/Taller
**File:** `ui_components.py`
**Line:** ~30

```python
TEXT_BOX_REL_HEIGHT = 0.3  # Current: very compact
                            # Try: 0.2 (even shorter)
                            # Try: 0.5 (taller)
```

### Change Hebrew Font Size
**File:** `ui_components.py`
**Line:** ~44

```python
HEBREW_FONT_SIZE = 36  # Current size
                       # Try: 40 (bigger)
                       # Try: 30 (smaller)
```

### Adjust Spacing Between Boxes
**File:** `ui_components.py`
**Line:** ~27

```python
TEXT_BOX_VERTICAL_SPACING = 4  # Current: tight spacing
                                # Try: 8 (more space)
                                # Try: 2 (less space)
```

### Change Card Corner Roundness
**File:** `ui_components.py`
**Line:** ~59

```python
CARD_BORDER_RADIUS = 20       # Main card
TEXT_BOX_BORDER_RADIUS = 12   # Text boxes
BUTTON_BORDER_RADIUS = 8      # Buttons

# Try: 30 (very round)
# Try: 5 (slightly round)
# Try: 0 (sharp corners)
```

### Adjust Button Sizes
**File:** `ui_components.py`
**Lines:** ~62-65

```python
MAIN_BUTTON_PADX = 18         # Horizontal padding (width)
MAIN_BUTTON_PADY = 8          # Vertical padding (height)
MAIN_BUTTON_FONT_SIZE = 11    # Text size

# Bigger buttons:
MAIN_BUTTON_PADX = 25
MAIN_BUTTON_PADY = 12
MAIN_BUTTON_FONT_SIZE = 13
```

### Change Colors (Light Mode)
**File:** `ui_components.py`
**Lines:** ~125-140

Change any color by modifying the hex code:
```python
'text_bg': '#f8f9fa',      # Try: '#ffffff' (pure white)
'trans_bg': '#e3f2fd',     # Try: '#fff9c4' (yellow tint)
'english_bg': '#e8f5e9',   # Try: '#fce4ec' (pink tint)
```

### Change Colors (Dark Mode)
**File:** `ui_components.py`
**Lines:** ~142-157

Same structure as light mode but for dark theme.

---

## Quick Reference: File Structure

```
ui_components.py (ALL UI HERE!)
├── UIConfig (lines 15-120)
│   ├── Layout spacing
│   ├── Font definitions
│   └── Widget dimensions
├── Themes (lines 122-158)
│   ├── LIGHT theme colors
│   └── DARK theme colors
└── UIBuilder (lines 160-600)
    ├── Widget creation methods
    └── build_complete_interface() - builds everything

config.py (App settings only)
└── Window size, file paths, metadata

hebrew_learning_app_modular.py (Business logic)
└── No UI code, just calls ui_builder.build_complete_interface()
```

---

## Benefits of This Structure

✅ **Single source of truth** - All UI settings in one place
✅ **Easy to experiment** - Change one number, see the result
✅ **Clear organization** - Related settings grouped together
✅ **Better maintainability** - Don't need to hunt through files
✅ **Quick adjustments** - Most changes are 1-2 lines

---

## Tips

1. **Make small changes** - Adjust one value at a time to see its effect
2. **Use comments** - The file has helpful comments for each setting
3. **Keep backups** - Test changes before committing
4. **Restart the app** - Changes require restarting the application
5. **Check both themes** - Test in both light and dark mode

---

## Example: Making Hebrew Box Shorter

**Before:**
```python
TEXT_BOX_REL_HEIGHT = 0.5  # Box takes up 50% of container
```

**After:**
```python
TEXT_BOX_REL_HEIGHT = 0.3  # Box takes up 30% of container (shorter!)
```

That's it! Just one number change, and all three text boxes become more compact.

---

## Need More Help?

- All measurements use standard units (pixels for spacing, 0.0-1.0 for relative sizes)
- Font sizes are in points (typical range: 9-48)
- Colors are hex codes (#RRGGBB format)
- To add custom fonts, modify the font family strings (e.g., 'Arial Hebrew')

Happy customizing! 🎨
