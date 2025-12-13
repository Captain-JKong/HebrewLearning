"""
Tests for Data Manager
Tests VocabularyManager and ProgressManager
"""

import pytest
from pathlib import Path


class TestVocabularyManager:
    """Test VocabularyManager functionality"""
    
    def test_load_vocabulary(self, vocab_manager):
        """Test loading vocabulary from database"""
        vocab = vocab_manager.load()
        
        assert len(vocab) == 50
        assert vocab_manager.vocabulary == vocab
    
    def test_vocabulary_word_structure(self, vocab_manager):
        """Test that loaded vocabulary has correct structure"""
        vocab = vocab_manager.load()
        word = vocab[0]
        
        # Check required fields
        assert 'hebrew' in word
        assert 'english' in word
        assert 'transliteration' in word
        assert 'part_of_speech' in word


class TestProgressManager:
    """Test ProgressManager functionality"""
    
    def test_load_progress(self, progress_manager):
        """Test loading progress stats"""
        progress = progress_manager.load()
        
        # Should have all stat categories
        assert 'easy' in progress
        assert 'good' in progress
        assert 'hard' in progress
        assert 'again' in progress
        assert 'not_studied' in progress
    
    def test_mark_word_easy(self, progress_manager):
        """Test marking a word as easy"""
        easiness = progress_manager.mark_word({}, 1, 'easy')
        
        assert easiness is not None
        assert isinstance(easiness, float)
    
    def test_mark_word_good(self, progress_manager):
        """Test marking a word as good"""
        easiness = progress_manager.mark_word({}, 1, 'good')
        assert easiness is not None
    
    def test_mark_word_hard(self, progress_manager):
        """Test marking a word as hard"""
        easiness = progress_manager.mark_word({}, 1, 'hard')
        assert easiness is not None
    
    def test_mark_word_again(self, progress_manager):
        """Test marking a word as again"""
        easiness = progress_manager.mark_word({}, 1, 'again')
        assert easiness is not None
    
    def test_mark_word_updates_stats(self, progress_manager, database):
        """Test that marking a word updates database stats"""
        # Mark word as easy
        progress_manager.mark_word({}, 1, 'easy')
        
        # Check that progress was recorded
        stats = database.get_vocabulary_stats()
        assert stats['easy'] >= 1


class TestGetDatabasePath:
    """Test database path utility function"""
    
    def test_get_database_path_from_csv(self):
        """Test deriving database path from CSV path"""
        from data_manager import get_database_path
        
        csv_path = Path('/some/path/hebrew_vocabulary.csv')
        db_path = get_database_path(csv_path)
        
        assert db_path == Path('/some/path/hebrew_vocabulary.db')
    
    def test_get_database_path_preserves_directory(self):
        """Test that directory is preserved"""
        from data_manager import get_database_path
        
        csv_path = Path('/users/test/data/vocab.csv')
        db_path = get_database_path(csv_path)
        
        assert db_path.parent == Path('/users/test/data')
        assert db_path.name == 'hebrew_vocabulary.db'
