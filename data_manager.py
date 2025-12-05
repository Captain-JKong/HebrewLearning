"""
Data Management
Handles vocabulary and progress data using SQLite database
"""

from pathlib import Path
from database_manager import DatabaseManager

class VocabularyManager:
    """Manages vocabulary data using SQLite database"""
    
    def __init__(self, vocab_file):
        db_path = Path(vocab_file).parent / 'hebrew_vocabulary.db'
        self.db = DatabaseManager(db_path)
        self.vocabulary = []
    
    def load(self):
        """Load vocabulary from SQLite database"""
        self.vocabulary = self.db.get_all_vocabulary()
        if not self.vocabulary:
            print("Database is empty. Populating with sample data...")
            self.db.populate_sample_data()
            self.vocabulary = self.db.get_all_vocabulary()
        print(f"✓ Loaded {len(self.vocabulary)} vocabulary entries from database")
        return self.vocabulary

class ProgressManager:
    """Manages learning progress data using SQLite database"""
    
    def __init__(self, progress_file):
        db_path = Path(progress_file).parent / 'hebrew_vocabulary.db'
        self.db = DatabaseManager(db_path)
    
    def load(self):
        """Load progress stats from database"""
        return self.db.get_vocabulary_stats()
    
    def save(self, progress):
        """Save progress - no-op since database auto-commits"""
        pass
    
    def mark_word(self, progress, word_key, confidence_level):
        """Mark a word with confidence level in database"""
        confidence_values = {'again': 1, 'hard': 2, 'good': 3, 'easy': 4}
        familiarity = confidence_values[confidence_level]
        
        try:
            # Parse lemma_id from word_key
            if isinstance(word_key, int):
                lemma_id = word_key
            elif '_' in str(word_key):
                rank = int(str(word_key).split('_')[0])
                vocab = self.db.get_all_vocabulary()
                matching = [v for v in vocab if v.get('rank') == rank]
                lemma_id = matching[0]['lemma_id'] if matching else None
            else:
                lemma_id = int(word_key)
            
            if lemma_id:
                return self.db.update_progress(lemma_id, familiarity)
            return 2.5
        except Exception as e:
            print(f"Error marking word: {e}")
            return 2.5
