"""
Tests for DatabaseManager
Tests database creation, data operations, and queries
"""

import pytest
from datetime import date, timedelta


class TestDatabaseInitialization:
    """Test database creation and table setup"""
    
    def test_database_creates_file(self, temp_db_path, empty_database):
        """Test that database file is created"""
        from pathlib import Path
        assert Path(temp_db_path).exists()
    
    def test_database_creates_tables(self, empty_database):
        """Test that all required tables are created"""
        cursor = empty_database.connection.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        
        expected_tables = {
            'lemmas', 'variants', 'categories', 
            'lemma_categories', 'translations', 
            'user_progress', 'user_settings'
        }
        
        assert expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}"


class TestSampleData:
    """Test sample data population"""
    
    def test_populate_sample_data(self, database):
        """Test that sample data is populated correctly"""
        cursor = database.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM lemmas")
        count = cursor.fetchone()[0]
        assert count == 50, f"Expected 50 lemmas, got {count}"
    
    def test_sample_data_has_variants(self, database):
        """Test that variants are populated"""
        cursor = database.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM variants")
        count = cursor.fetchone()[0]
        assert count > 0, "No variants were created"
    
    def test_sample_data_has_categories(self, database):
        """Test that categories are populated"""
        cursor = database.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        assert count > 0, "No categories were created"


class TestVocabularyQueries:
    """Test vocabulary retrieval functions"""
    
    def test_get_all_vocabulary(self, database):
        """Test getting all vocabulary"""
        vocab = database.get_all_vocabulary()
        assert len(vocab) == 50
        
        # Check that required fields exist
        first_word = vocab[0]
        assert 'hebrew' in first_word
        assert 'english' in first_word
        assert 'transliteration' in first_word
    
    def test_vocabulary_has_correct_structure(self, database):
        """Test vocabulary word structure"""
        vocab = database.get_all_vocabulary()
        word = vocab[0]
        
        # Test expected keys
        expected_keys = ['lemma_id', 'hebrew', 'part_of_speech', 
                        'transliteration', 'english', 'rank']
        for key in expected_keys:
            assert key in word, f"Missing key: {key}"
    
    def test_get_lemma_id_by_rank(self, database):
        """Test finding lemma by rank"""
        # Rank 1 should be 'shalom'
        lemma_id = database.get_lemma_id_by_rank(1)
        assert lemma_id is not None
        assert lemma_id == 1


class TestUserProgress:
    """Test user progress tracking"""
    
    def test_update_progress(self, database):
        """Test updating word progress"""
        # Update progress for lemma_id 1
        easiness = database.update_progress(1, familiarity=3)
        
        assert easiness is not None
        assert isinstance(easiness, float)
    
    def test_get_vocabulary_stats(self, database):
        """Test getting vocabulary statistics"""
        stats = database.get_vocabulary_stats()
        
        assert 'easy' in stats
        assert 'good' in stats
        assert 'hard' in stats
        assert 'again' in stats
        assert 'not_studied' in stats
    
    def test_progress_updates_next_review(self, database):
        """Test that updating progress sets next_review date"""
        database.update_progress(1, familiarity=4)  # Mark as easy
        
        cursor = database.connection.cursor()
        cursor.execute("SELECT next_review FROM user_progress WHERE lemma_id = 1")
        row = cursor.fetchone()
        
        assert row is not None
        assert row[0] is not None  # next_review should be set


class TestUserSettings:
    """Test user settings storage"""
    
    def test_save_and_get_setting(self, database):
        """Test saving and retrieving settings"""
        database.save_setting('test_key', True)
        value = database.get_setting('test_key', False)
        assert value == True
    
    def test_get_default_setting(self, database):
        """Test getting default value for non-existent setting"""
        value = database.get_setting('nonexistent_key', 'default_value')
        assert value == 'default_value'
    
    def test_update_existing_setting(self, database):
        """Test updating an existing setting"""
        database.save_setting('update_test', 'first')
        database.save_setting('update_test', 'second')
        value = database.get_setting('update_test', None)
        assert value == 'second'


class TestVariantsAndCategories:
    """Test variants and category queries"""
    
    def test_get_variants_for_lemma(self, database):
        """Test getting variants for a lemma"""
        # Lemma 6 (בית) should have variants
        cursor = database.connection.cursor()
        cursor.execute("SELECT * FROM variants WHERE lemma_id = 6")
        variants = cursor.fetchall()
        
        assert len(variants) > 0, "Expected variants for lemma_id 6"
    
    def test_get_categories(self, database):
        """Test getting category list"""
        cursor = database.connection.cursor()
        cursor.execute("SELECT name FROM categories")
        categories = [row[0] for row in cursor.fetchall()]
        
        assert 'Verbs' in categories
        assert 'Nouns' in categories
        assert 'Biblical Hebrew' in categories
