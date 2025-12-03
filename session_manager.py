"""
Session Manager
Handles study session logic and word selection
Now supports multiple study modes using rich database structure
"""

import random
from datetime import datetime, date

class SessionManager:
    """Manages learning sessions with multiple study modes"""
    
    def __init__(self, vocabulary, progress):
        self.vocabulary = vocabulary
        self.progress = progress
        self.current_words = []
        self.current_index = 0
        self.current_word = None
        self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
        self.session_mode = None  # Track what mode is active
    
    def start_session(self, limit=None):
        """Start a new study session by frequency rank"""
        self.session_mode = f"Top {limit}" if limit else "All Words"
        if limit:
            self.current_words = [w for w in self.vocabulary if int(w.get('rank', 999)) <= limit]
        else:
            self.current_words = self.vocabulary.copy()
        
        random.shuffle(self.current_words)
        self._reset_session()
        return len(self.current_words)
    
    def start_custom_session(self, start_rank, end_rank):
        """Start session with custom rank range"""
        self.current_words = [
            w for w in self.vocabulary 
            if start_rank <= int(w['rank']) <= end_rank
        ]
        random.shuffle(self.current_words)
        self.current_index = 0
        self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
        return len(self.current_words)
    
    def practice_difficult_words(self, top_n):
        """Practice words marked as Hard or Again within top N"""
        self.session_mode = f"Review Difficult (Top {top_n})"
        # Get words in range with familiarity 1 or 2 (Again/Hard)
        range_words = [w for w in self.vocabulary if int(w.get('rank', 999)) <= top_n]
        needs_practice = [w for w in range_words if w.get('familiarity') in [1, 2, None, 0]]
        
        if needs_practice:
            self.current_words = needs_practice
            random.shuffle(self.current_words)
            self._reset_session()
        
        return len(needs_practice)
    
    # ========== NEW STUDY MODES ==========
    
    def start_srs_session(self):
        """SRS Mode: Study words due for review today"""
        self.session_mode = "SRS Review"
        today = date.today().isoformat()
        
        # Get words where next_review is today or earlier
        due_words = [
            w for w in self.vocabulary 
            if w.get('next_review') and w.get('next_review') <= today
        ]
        
        # Sort by next_review (most overdue first)
        due_words.sort(key=lambda w: w.get('next_review', '9999-99-99'))
        
        self.current_words = due_words
        self._reset_session()
        return len(self.current_words)
    
    def start_new_words_session(self, limit=10):
        """Learning Mode: Study words never reviewed before"""
        self.session_mode = f"New Words (up to {limit})"
        
        # Get words with no familiarity or familiarity = 0
        new_words = [w for w in self.vocabulary if not w.get('familiarity') or w.get('familiarity') == 0]
        
        # Sort by rank and take first N
        new_words.sort(key=lambda w: w.get('rank', 999))
        self.current_words = new_words[:limit]
        self._reset_session()
        return len(self.current_words)
    
    def start_category_session(self, category_name):
        """Study by Category: Verbs, Nouns, Biblical, etc."""
        self.session_mode = f"Category: {category_name}"
        from database_manager import DatabaseManager
        from pathlib import Path
        
        # Get database manager
        db_path = Path(__file__).parent / 'hebrew_vocabulary.db'
        db = DatabaseManager(db_path)
        
        # Get lemma IDs for this category
        cursor = db.connection.cursor()
        cursor.execute('''
            SELECT l.lemma_id
            FROM lemmas l
            JOIN lemma_categories lc ON l.lemma_id = lc.lemma_id
            JOIN categories c ON lc.category_id = c.category_id
            WHERE c.name = ?
        ''', (category_name,))
        
        category_ids = {row[0] for row in cursor.fetchall()}
        
        # Filter vocabulary by these IDs
        self.current_words = [w for w in self.vocabulary if w.get('lemma_id') in category_ids]
        random.shuffle(self.current_words)
        self._reset_session()
        return len(self.current_words)
    
    def start_register_session(self, register):
        """Study by Register: modern, biblical, or both"""
        self.session_mode = f"Register: {register.title()}"
        
        if register == 'both':
            self.current_words = [w for w in self.vocabulary if w.get('register') == 'both']
        else:
            self.current_words = [w for w in self.vocabulary if w.get('register') == register]
        
        random.shuffle(self.current_words)
        self._reset_session()
        return len(self.current_words)
    
    def start_part_of_speech_session(self, pos):
        """Study by Part of Speech: verb, noun, adjective, etc."""
        self.session_mode = f"Part of Speech: {pos.title()}"
        
        self.current_words = [w for w in self.vocabulary if w.get('part_of_speech') == pos]
        random.shuffle(self.current_words)
        self._reset_session()
        return len(self.current_words)
    
    def start_weak_words_session(self, limit=20):
        """Study weakest words (lowest familiarity/easiness)"""
        self.session_mode = "Weakest Words"
        
        # Sort by familiarity (ascending), then by easiness (ascending)
        weak_words = [w for w in self.vocabulary if w.get('familiarity')]
        weak_words.sort(key=lambda w: (w.get('familiarity', 0), w.get('easiness', 2.5)))
        
        self.current_words = weak_words[:limit]
        self._reset_session()
        return len(self.current_words)
    
    def start_strong_words_session(self, limit=20):
        """Study strongest words (highest familiarity/easiness)"""
        self.session_mode = "Strongest Words"
        
        # Sort by familiarity (descending), then by easiness (descending)
        strong_words = [w for w in self.vocabulary if w.get('familiarity')]
        strong_words.sort(key=lambda w: (w.get('familiarity', 0), w.get('easiness', 2.5)), reverse=True)
        
        self.current_words = strong_words[:limit]
        self._reset_session()
        return len(self.current_words)
    
    def start_root_family_session(self, root):
        """Study all words from the same root"""
        self.session_mode = f"Root Family: {root}"
        
        self.current_words = [w for w in self.vocabulary if w.get('root') == root]
        # Don't shuffle - keep them together to see relationships
        self._reset_session()
        return len(self.current_words)
    
    def start_random_session(self, count=10):
        """Random selection of words"""
        self.session_mode = f"Random ({count} words)"
        
        available = self.vocabulary.copy()
        random.shuffle(available)
        self.current_words = available[:count]
        self._reset_session()
        return len(self.current_words)
    
    # ========== HELPER METHODS ==========
    
    def _reset_session(self):
        """Reset session counters"""
        self.current_index = 0
        self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
    
    def get_next_word(self):
        """Get next word in session"""
        if self.current_index < len(self.current_words):
            self.current_word = self.current_words[self.current_index]
            return self.current_word
        return None
    
    def record_answer(self, confidence_level):
        """Record answer and update stats"""
        if confidence_level in ['good', 'easy']:
            self.session_stats['correct'] += 1
        else:
            self.session_stats['incorrect'] += 1
        self.session_stats['total'] += 1
    
    def advance(self):
        """Move to next word"""
        self.current_index += 1
    
    def is_complete(self):
        """Check if session is complete"""
        return self.current_index >= len(self.current_words)
    
    def get_progress_text(self):
        """Get progress description text"""
        return f"Word {self.current_index + 1} of {len(self.current_words)}"
