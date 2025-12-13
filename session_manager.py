"""
Session Manager
Handles study session logic and word selection
"""

import random
from datetime import date


class SessionManager:
    """Manages learning sessions with multiple study modes"""
    
    def __init__(self, vocabulary, progress, db=None):
        self.vocabulary = vocabulary
        self.progress = progress
        self.db = db
        self.current_words = []
        self.current_index = 0
        self.current_word = None
        self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
        self.session_mode = None
    
    # ==================== CORE SESSION STARTER ====================
    
    def _start_session(self, words, label, shuffle=True):
        """Start a session with given words"""
        self.session_mode = label
        self.current_words = words
        if shuffle:
            random.shuffle(self.current_words)
        self.current_index = 0
        self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
        return len(self.current_words)
    
    # ==================== GENERIC FILTERS ====================
    
    def start_by_field(self, field, value, label=None):
        """Generic: filter vocabulary by any field matching a value"""
        words = [w for w in self.vocabulary if w.get(field) == value]
        return self._start_session(words, label or f"{field}: {value}")
    
    def start_by_rank(self, max_rank=None, min_rank=1):
        """Filter by frequency rank range"""
        if max_rank:
            words = [w for w in self.vocabulary if min_rank <= int(w.get('rank', 999)) <= max_rank]
            label = f"Rank {min_rank}-{max_rank}" if min_rank > 1 else f"Top {max_rank}"
        else:
            words = self.vocabulary.copy()
            label = "All Words"
        return self._start_session(words, label)
    
    def start_by_familiarity(self, levels, limit=20, weakest_first=True, label="By Familiarity"):
        """Filter by familiarity levels, sorted by strength"""
        words = [w for w in self.vocabulary if w.get('familiarity') in levels]
        words.sort(
            key=lambda w: (w.get('familiarity', 0), w.get('easiness', 2.5)),
            reverse=not weakest_first
        )
        return self._start_session(words[:limit], label, shuffle=False)
    
    # ==================== CONVENIENCE METHODS ====================
    # These are thin wrappers that call the generic methods above
    
    def start_session(self, limit=None):
        """Quick start with rank limit"""
        return self.start_by_rank(max_rank=limit)
    
    def start_custom_session(self, start_rank, end_rank):
        """Custom rank range"""
        words = [w for w in self.vocabulary if start_rank <= int(w.get('rank', 999)) <= end_rank]
        return self._start_session(words, f"Custom Range: {start_rank}-{end_rank}")
    
    def start_register_session(self, register):
        """By register: modern, biblical, or both"""
        return self.start_by_field('register', register, f"Register: {register.title()}")
    
    def start_part_of_speech_session(self, pos):
        """By part of speech"""
        return self.start_by_field('part_of_speech', pos, f"{pos.title()}s")
    
    def start_root_family_session(self, root):
        """By Hebrew root"""
        return self.start_by_field('root', root, f"Root: {root}")
    
    def start_weak_words_session(self, limit=20):
        """Weakest words by familiarity"""
        return self.start_by_familiarity([1, 2, 3, 4], limit, weakest_first=True, label="Weakest Words")
    
    def start_strong_words_session(self, limit=20):
        """Strongest words by familiarity"""
        return self.start_by_familiarity([1, 2, 3, 4], limit, weakest_first=False, label="Strongest Words")
    
    def practice_difficult_words(self, top_n):
        """Words marked Hard/Again in top N"""
        words = [w for w in self.vocabulary 
                 if int(w.get('rank', 999)) <= top_n 
                 and w.get('familiarity') in [None, 0, 1, 2]]
        return self._start_session(words, f"Difficult (Top {top_n})")
    
    def start_random_session(self, count=10):
        """Random selection"""
        words = random.sample(self.vocabulary, min(count, len(self.vocabulary)))
        return self._start_session(words, f"Random {count}", shuffle=False)
    
    def start_new_words_session(self, limit=10):
        """Words never studied"""
        words = [w for w in self.vocabulary if not w.get('familiarity')]
        words.sort(key=lambda w: w.get('rank', 999))
        return self._start_session(words[:limit], f"New Words ({limit})", shuffle=False)
    
    def start_srs_session(self):
        """Words due for SRS review today"""
        today = date.today().isoformat()
        words = [w for w in self.vocabulary if w.get('next_review') and w.get('next_review') <= today]
        words.sort(key=lambda w: w.get('next_review', '9999-99-99'))
        return self._start_session(words, "SRS Review", shuffle=False)
    
    def start_category_session(self, category_name):
        """By category from database"""
        if not self.db:
            return 0
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT l.lemma_id FROM lemmas l
            JOIN lemma_categories lc ON l.lemma_id = lc.lemma_id
            JOIN categories c ON lc.category_id = c.category_id
            WHERE c.name = ?
        ''', (category_name,))
        ids = {row[0] for row in cursor.fetchall()}
        words = [w for w in self.vocabulary if w.get('lemma_id') in ids]
        return self._start_session(words, f"Category: {category_name}")
    
    # ==================== SESSION STATE ====================
    
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
        """Get progress description"""
        return f"Word {self.current_index + 1} of {len(self.current_words)}"
