"""
Configuration and Constants
Manages file paths, themes, and app settings
"""

import sys
from pathlib import Path

class Config:
    """Application configuration and paths"""
    
    # App metadata
    APP_NAME = "Hebrew Learning"
    APP_VERSION = "2.5"
    APP_IDENTIFIER = "com.hebrewlearning.app"
    
    # Window settings
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 550
    
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

class Themes:
    """UI theme definitions"""
    
    LIGHT = {
        'bg': '#f0f0f0',
        'card_bg': '#ffffff',
        'text_bg': '#f8f9fa',
        'text_fg': '#2c3e50',
        'trans_bg': '#e3f2fd',
        'trans_fg': '#1565c0',
        'english_bg': '#e8f5e9',
        'english_fg': '#2e7d32',
        'btn_audio': '#2196f3',
        'btn_answer': '#ff9800',
        'btn_again': '#f44336',
        'btn_hard': '#ff9800',
        'btn_good': '#8bc34a',
        'btn_easy': '#4caf50'
    }
    
    DARK = {
        'bg': '#1e1e1e',
        'card_bg': '#2d2d2d',
        'text_bg': '#3a3a3a',
        'text_fg': '#e0e0e0',
        'trans_bg': '#263238',
        'trans_fg': '#81d4fa',
        'english_bg': '#1b5e20',
        'english_fg': '#a5d6a7',
        'btn_audio': '#1976d2',
        'btn_answer': '#f57c00',
        'btn_again': '#d32f2f',
        'btn_hard': '#f57c00',
        'btn_good': '#689f38',
        'btn_easy': '#388e3c'
    }
    
    @staticmethod
    def get_theme(dark_mode=False):
        """Get theme colors based on mode"""
        return Themes.DARK if dark_mode else Themes.LIGHT
