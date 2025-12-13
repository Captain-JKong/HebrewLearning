"""
Data Management
Handles vocabulary and progress data using SQLite database
"""

from pathlib import Path
from database_manager import DatabaseManager


def get_database_path(file_path):
    """Get database path from any related file path"""
    return Path(file_path).parent / 'hebrew_vocabulary.db'


class VocabularyManager:
    """Manages vocabulary data using SQLite database"""
    
    def __init__(self, db):
        self.db = db
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
    
    def __init__(self, db):
        self.db = db
    
    def load(self):
        """Load progress stats from database"""
        return self.db.get_vocabulary_stats()
    
    def save(self, progress):
        """Save progress - no-op since database auto-commits"""
        pass
    
    def _create_empty_progress(self):
        """Create empty progress structure"""
        return {'easy': 0, 'good': 0, 'hard': 0, 'again': 0, 'not_studied': 0}
    
    def mark_word(self, progress, word_key, confidence_level):
        """Mark a word with confidence level in database"""
        confidence_values = {'again': 1, 'hard': 2, 'good': 3, 'easy': 4}
        familiarity = confidence_values[confidence_level]
        
        try:
            # Parse lemma_id from word_key
            if isinstance(word_key, int):
                lemma_id = word_key
            elif '_' in str(word_key):
                # Old format: "rank_hebrew" - extract rank and lookup
                rank = int(str(word_key).split('_')[0])
                lemma_id = self.db.get_lemma_id_by_rank(rank)
            else:
                lemma_id = int(word_key)
            
            if lemma_id:
                return self.db.update_progress(lemma_id, familiarity)
            return 2.5
        except Exception as e:
            import traceback
            print(f"Error marking word: {e}")
            traceback.print_exc()
            return 2.5
