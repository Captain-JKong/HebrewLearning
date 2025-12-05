"""
Configuration and Constants
Manages file paths and app settings
NOTE: All UI configuration (colors, fonts, spacing) is now in ui_components.py
"""

import sys
from pathlib import Path

class Config:
    """Application configuration and paths"""
    
    # App metadata
    APP_NAME = "Hebrew Learning"
    APP_VERSION = "2.5"
    APP_IDENTIFIER = "com.hebrewlearning.app"
    
    # Window settings (basic window size only)
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 720
    
    # File names
    VOCAB_FILE = 'hebrew_vocabulary.csv'
    PROGRESS_FILE = 'learning_progress.json'
    ICON_FILE = 'HebrewLearning.icns'
    USER_DIR = '.hebrew_learning'
    
    @staticmethod
    def get_paths():
        """Get file paths based on runtime environment"""
        if getattr(sys, 'frozen', False):
            # Running in PyInstaller bundle
            base_path = Path(sys._MEIPASS)
            # Progress file goes in user's home directory (not bundled)
            progress_dir = Path.home() / Config.USER_DIR
            progress_dir.mkdir(exist_ok=True)
            progress_file = progress_dir / Config.PROGRESS_FILE
        else:
            # Running as script
            base_path = Path(__file__).parent
            # Check if running from manual app bundle
            if 'Contents/MacOS' in str(base_path):
                # In app bundle, resources are in ../Resources
                base_path = base_path.parent / 'Resources'
                progress_file = base_path / Config.PROGRESS_FILE
            else:
                # Running standalone in development
                progress_file = base_path / Config.PROGRESS_FILE
        
        return {
            'base': base_path,
            'vocab': base_path / Config.VOCAB_FILE,
            'csv': base_path / Config.VOCAB_FILE,
            'icon': base_path / Config.ICON_FILE,
            'progress': progress_file
        }
