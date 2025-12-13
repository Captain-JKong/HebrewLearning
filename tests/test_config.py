"""
Tests for Config
Tests configuration and path resolution
"""

import pytest
from pathlib import Path


class TestConfigConstants:
    """Test configuration constants"""
    
    def test_app_name(self):
        """Test app name is set"""
        from config import Config
        assert Config.APP_NAME == "Hebrew Learning"
    
    def test_app_version(self):
        """Test app version is set"""
        from config import Config
        assert Config.APP_VERSION is not None
        assert len(Config.APP_VERSION) > 0
    
    def test_window_dimensions(self):
        """Test window dimensions are reasonable"""
        from config import Config
        
        assert Config.WINDOW_WIDTH > 0
        assert Config.WINDOW_HEIGHT > 0
        assert Config.WINDOW_WIDTH >= 400  # Minimum reasonable width
        assert Config.WINDOW_HEIGHT >= 400  # Minimum reasonable height


class TestConfigPaths:
    """Test path configuration"""
    
    def test_get_paths_returns_dict(self):
        """Test that get_paths returns a dictionary"""
        from config import Config
        
        paths = Config.get_paths()
        assert isinstance(paths, dict)
    
    def test_get_paths_has_required_keys(self):
        """Test that paths dict has all required keys"""
        from config import Config
        
        paths = Config.get_paths()
        
        required_keys = ['base', 'vocab', 'csv', 'icon', 'progress']
        for key in required_keys:
            assert key in paths, f"Missing path key: {key}"
    
    def test_paths_are_path_objects(self):
        """Test that path values are Path objects"""
        from config import Config
        
        paths = Config.get_paths()
        
        for key, value in paths.items():
            assert isinstance(value, Path), f"{key} is not a Path object"
    
    def test_vocab_file_name(self):
        """Test vocabulary file name constant"""
        from config import Config
        
        assert Config.VOCAB_FILE == 'hebrew_vocabulary.csv'
    
    def test_progress_file_name(self):
        """Test progress file name constant"""
        from config import Config
        
        assert Config.PROGRESS_FILE == 'learning_progress.json'
