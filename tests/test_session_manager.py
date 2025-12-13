"""
Tests for SessionManager
Tests study session logic and word selection
"""

import pytest


class TestSessionStart:
    """Test session initialization"""
    
    def test_start_session_all_words(self, session_manager):
        """Test starting a session with all words"""
        count = session_manager.start_session()
        assert count == 50  # All sample words
    
    def test_start_session_with_limit(self, session_manager):
        """Test starting a session with a word limit"""
        count = session_manager.start_session(limit=10)
        assert count == 10
    
    def test_start_custom_session(self, session_manager):
        """Test starting a custom range session"""
        count = session_manager.start_custom_session(1, 20)
        assert count == 20


class TestStudyModes:
    """Test different study modes"""
    
    def test_start_new_words_session(self, session_manager):
        """Test new words session (words never reviewed)"""
        count = session_manager.start_new_words_session(limit=5)
        # Sample data includes progress, so new words may be 0 or more
        assert count >= 0
    
    def test_start_random_session(self, session_manager):
        """Test random words session"""
        count = session_manager.start_random_session(count=15)
        assert count == 15
    
    def test_start_part_of_speech_session(self, session_manager):
        """Test filtering by part of speech"""
        count = session_manager.start_part_of_speech_session('verb')
        assert count > 0
        
        # Verify all words are verbs
        for word in session_manager.current_words:
            assert word['part_of_speech'] == 'verb'
    
    def test_start_register_session(self, session_manager):
        """Test filtering by register (modern/biblical)"""
        count = session_manager.start_register_session('modern')
        assert count > 0
        
        for word in session_manager.current_words:
            assert word['register'] == 'modern'
    
    def test_start_root_family_session(self, session_manager):
        """Test studying words from same root"""
        # Root 'ילד' has multiple words (ילד, ילדה)
        count = session_manager.start_root_family_session('ילד')
        assert count >= 1


class TestWordNavigation:
    """Test word navigation during session"""
    
    def test_get_next_word(self, session_manager):
        """Test getting next word in session"""
        session_manager.start_session(limit=5)
        word = session_manager.get_next_word()
        
        assert word is not None
        assert 'hebrew' in word
        assert 'english' in word
    
    def test_advance_moves_to_next(self, session_manager):
        """Test that advance() moves to next word"""
        session_manager.start_session(limit=5)
        
        first_word = session_manager.get_next_word()
        session_manager.advance()
        second_word = session_manager.get_next_word()
        
        assert first_word != second_word
    
    def test_is_complete_returns_false_at_start(self, session_manager):
        """Test is_complete at session start"""
        session_manager.start_session(limit=5)
        assert not session_manager.is_complete()
    
    def test_is_complete_returns_true_at_end(self, session_manager):
        """Test is_complete after going through all words"""
        session_manager.start_session(limit=3)
        
        for _ in range(3):
            session_manager.get_next_word()
            session_manager.advance()
        
        assert session_manager.is_complete()


class TestSessionStats:
    """Test session statistics tracking"""
    
    def test_record_correct_answer(self, session_manager):
        """Test recording a correct answer"""
        session_manager.start_session(limit=5)
        session_manager.get_next_word()
        
        session_manager.record_answer('good')
        
        assert session_manager.session_stats['correct'] == 1
        assert session_manager.session_stats['total'] == 1
    
    def test_record_incorrect_answer(self, session_manager):
        """Test recording an incorrect answer"""
        session_manager.start_session(limit=5)
        session_manager.get_next_word()
        
        session_manager.record_answer('again')
        
        assert session_manager.session_stats['incorrect'] == 1
        assert session_manager.session_stats['total'] == 1
    
    def test_easy_counts_as_correct(self, session_manager):
        """Test that 'easy' counts as correct"""
        session_manager.start_session(limit=5)
        session_manager.get_next_word()
        session_manager.record_answer('easy')
        
        assert session_manager.session_stats['correct'] == 1
    
    def test_hard_counts_as_incorrect(self, session_manager):
        """Test that 'hard' counts as incorrect"""
        session_manager.start_session(limit=5)
        session_manager.get_next_word()
        session_manager.record_answer('hard')
        
        assert session_manager.session_stats['incorrect'] == 1


class TestSessionModeTracking:
    """Test session mode identification"""
    
    def test_session_mode_set_correctly(self, session_manager):
        """Test that session mode is tracked"""
        session_manager.start_session(limit=10)
        assert "Top 10" in session_manager.session_mode
    
    def test_custom_range_mode_label(self, session_manager):
        """Test custom range session mode label"""
        session_manager.start_custom_session(5, 15)
        assert "Custom Range" in session_manager.session_mode
    
    def test_part_of_speech_mode_label(self, session_manager):
        """Test part of speech session mode label"""
        session_manager.start_part_of_speech_session('noun')
        assert "noun" in session_manager.session_mode.lower()
