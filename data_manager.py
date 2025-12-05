"""
Data Management
Handles vocabulary and progress data loading/saving
Now uses SQLite database instead of CSV
"""

import csv
import json
import sys
from pathlib import Path
from datetime import datetime
from database_manager import DatabaseManager

class VocabularyManager:
    """Manages vocabulary data - now using SQLite database"""
    
    def __init__(self, vocab_file):
        self.vocab_file = vocab_file  # Keep for legacy CSV export
        self.vocabulary = []
        # Initialize database connection
        db_path = Path(vocab_file).parent / 'hebrew_vocabulary.db'
        self.db = DatabaseManager(db_path)
    
    def load(self):
        """Load vocabulary from SQLite database"""
        try:
            # Check if database has data, if not populate it
            self.vocabulary = self.db.get_all_vocabulary()
            
            if not self.vocabulary:
                print("Database is empty. Populating with sample data...")
                self.db.populate_sample_data()
                self.vocabulary = self.db.get_all_vocabulary()
            
            print(f"✓ Loaded {len(self.vocabulary)} vocabulary entries from SQLite database")
            return self.vocabulary
        except Exception as e:
            raise Exception(f"Error loading vocabulary from database: {e}")
    
    def save(self, vocabulary, csv_file):
        """Save vocabulary list to CSV file (legacy backup only - main data is in SQLite)"""
        # Skip CSV save since SQLite is the primary data store
        # CSV export can be added as a separate feature if needed
        pass

class ProgressManager:
    """Manages learning progress data - now uses SQLite database"""
    
    def __init__(self, progress_file):
        self.progress_file = progress_file  # Keep for legacy JSON backup
        # Use the same database as VocabularyManager
        db_path = Path(progress_file).parent / 'hebrew_vocabulary.db'
        self.db = DatabaseManager(db_path)
    
    def load(self):
        """Load progress - now returns stats from database"""
        # Return legacy-compatible structure for backward compatibility
        stats = self.db.get_vocabulary_stats()
        return {
            'easy': stats.get('easy', 0),
            'good': stats.get('good', 0),
            'hard': stats.get('hard', 0),
            'again': stats.get('again', 0),
            'not_studied': stats.get('not_studied', 0),
            'last_session': datetime.now().isoformat()
        }
    
    def save(self, progress):
        """Save progress - now just updates timestamp (actual progress saved via mark_word)"""
        # Keep legacy JSON for backup/reference
        progress['last_session'] = datetime.now().isoformat()
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, indent=2, fp=f)
        except:
            pass  # Ignore errors, database is primary now
    
    def _create_empty_progress(self):
        """Create empty progress structure"""
        return {
            'easy': [],      # Mastered - very confident
            'good': [],      # Know well - confident
            'hard': [],      # Struggling - need more practice
            'again': [],     # Don't know - need to review
            'confidence_scores': {},  # Track average confidence per word
            'last_session': None
        }
    
    def mark_word(self, progress, word_key, confidence_level):
        """Mark a word with confidence level - now updates SQLite database"""
        # Map confidence level to numeric familiarity
        confidence_values = {'again': 1, 'hard': 2, 'good': 3, 'easy': 4}
        familiarity = confidence_values[confidence_level]
        
        # Extract lemma_id from word_key (format: "rank_hebrew" or just use lemma_id if available)
        # For now, assume word_key contains lemma_id or can be derived
        try:
            # Try to parse lemma_id from word_key
            if isinstance(word_key, int):
                lemma_id = word_key
            elif '_' in str(word_key):
                # Old format: "rank_hebrew" - need to look up by rank
                rank = int(str(word_key).split('_')[0])
                # Find lemma by rank
                vocab = self.db.get_all_vocabulary()
                matching = [v for v in vocab if v.get('rank') == rank]
                if matching:
                    lemma_id = matching[0]['lemma_id']
                else:
                    return 0  # Can't find word
            else:
                lemma_id = int(word_key)
            
            # Update in database
            easiness = self.db.update_progress(lemma_id, familiarity)
            
            # Also update legacy progress structure for compatibility
            # Convert word_key to string for consistency in progress tracking
            word_key_str = str(word_key)
            for category in ['easy', 'good', 'hard', 'again']:
                # Ensure we always get a list, not None or other type
                category_value = progress.get(category, [])
                if not isinstance(category_value, list):
                    category_value = []
                    progress[category] = category_value
                
                # Remove any existing entry (convert all to strings for comparison)
                progress[category] = [item for item in category_value if str(item) != word_key_str]
            
            # Add to new category
            if confidence_level not in progress:
                progress[confidence_level] = []
            if not isinstance(progress[confidence_level], list):
                progress[confidence_level] = []
            progress[confidence_level].append(word_key_str)
            
            return easiness
        except Exception as e:
            print(f"Error marking word: {e}")
            return 2.5
