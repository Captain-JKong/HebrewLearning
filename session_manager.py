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
    
    def _start_filtered_session(self, filter_func, session_label, shuffle=True):
        """Unified session starter with filter function"""
        self.session_mode = session_label
        self.current_words = filter_func(self.vocabulary)
        if shuffle:
            random.shuffle(self.current_words)
        self._reset_session()
        return len(self.current_words)
    
    def start_session(self, limit=None):
        """Start a new study session by frequency rank"""
        label = f"Top {limit}" if limit else "All Words"
        filter_func = (lambda v: [w for w in v if int(w.get('rank', 999)) <= limit]) if limit else (lambda v: v.copy())
        return self._start_filtered_session(filter_func, label)
    
    def start_custom_session(self, start_rank, end_rank):
        """Start session with custom rank range"""
        filter_func = lambda v: [w for w in v if start_rank <= int(w['rank']) <= end_rank]
        return self._start_filtered_session(filter_func, f"Custom Range: {start_rank}-{end_rank}")
    
    def practice_difficult_words(self, top_n):
        """Practice words marked as Hard or Again within top N"""
        def filter_func(v):
            range_words = [w for w in v if int(w.get('rank', 999)) <= top_n]
            return [w for w in range_words if w.get('familiarity') in [1, 2, None, 0]]
        return self._start_filtered_session(filter_func, f"Review Difficult (Top {top_n})")
    
    # ========== NEW STUDY MODES ==========
    
    def start_srs_session(self):
        """SRS Mode: Study words due for review today"""
        today = date.today().isoformat()
        def filter_func(v):
            due = [w for w in v if w.get('next_review') and w.get('next_review') <= today]
            due.sort(key=lambda w: w.get('next_review', '9999-99-99'))
            return due
        return self._start_filtered_session(filter_func, "SRS Review", shuffle=False)
    
    def start_new_words_session(self, limit=10):
        """Learning Mode: Study words never reviewed before"""
        def filter_func(v):
            new_words = [w for w in v if not w.get('familiarity') or w.get('familiarity') == 0]
            new_words.sort(key=lambda w: w.get('rank', 999))
            return new_words[:limit]
        return self._start_filtered_session(filter_func, f"New Words (up to {limit})", shuffle=False)
    
    def start_category_session(self, category_name):
        """Study by Category: Verbs, Nouns, Biblical, etc."""
        from database_manager import DatabaseManager
        from pathlib import Path
        db = DatabaseManager(Path(__file__).parent / 'hebrew_vocabulary.db')
        cursor = db.connection.cursor()
        cursor.execute('''
            SELECT l.lemma_id FROM lemmas l
            JOIN lemma_categories lc ON l.lemma_id = lc.lemma_id
            JOIN categories c ON lc.category_id = c.category_id
            WHERE c.name = ?
        ''', (category_name,))
        category_ids = {row[0] for row in cursor.fetchall()}
        filter_func = lambda v: [w for w in v if w.get('lemma_id') in category_ids]
        return self._start_filtered_session(filter_func, f"Category: {category_name}")
    
    def start_register_session(self, register):
        """Study by Register: modern, biblical, or both"""
        filter_func = lambda v: [w for w in v if w.get('register') == register]
        return self._start_filtered_session(filter_func, f"Register: {register.title()}")
    
    def start_part_of_speech_session(self, pos):
        """Study by Part of Speech: verb, noun, adjective, etc."""
        filter_func = lambda v: [w for w in v if w.get('part_of_speech') == pos]
        return self._start_filtered_session(filter_func, f"Part of Speech: {pos.title()}")
    
    def start_weak_words_session(self, limit=20):
        """Study weakest words (lowest familiarity/easiness)"""
        def filter_func(v):
            weak = [w for w in v if w.get('familiarity')]
            weak.sort(key=lambda w: (w.get('familiarity', 0), w.get('easiness', 2.5)))
            return weak[:limit]
        return self._start_filtered_session(filter_func, "Weakest Words", shuffle=False)
    
    def start_strong_words_session(self, limit=20):
        """Study strongest words (highest familiarity/easiness)"""
        def filter_func(v):
            strong = [w for w in v if w.get('familiarity')]
            strong.sort(key=lambda w: (w.get('familiarity', 0), w.get('easiness', 2.5)), reverse=True)
            return strong[:limit]
        return self._start_filtered_session(filter_func, "Strongest Words", shuffle=False)
    
    def start_root_family_session(self, root):
        """Study all words from the same root"""
        filter_func = lambda v: [w for w in v if w.get('root') == root]
        return self._start_filtered_session(filter_func, f"Root Family: {root}", shuffle=False)
    
    def start_random_session(self, count=10):
        """Random selection of words"""
        def filter_func(v):
            available = v.copy()
            random.shuffle(available)
            return available[:count]
        return self._start_filtered_session(filter_func, f"Random ({count} words)", shuffle=False)
    
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
