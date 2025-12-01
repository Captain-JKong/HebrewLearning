"""
Session Manager
Handles study session logic and word selection
"""

import random

class SessionManager:
    """Manages learning sessions"""
    
    def __init__(self, vocabulary, progress):
        self.vocabulary = vocabulary
        self.progress = progress
        self.current_words = []
        self.current_index = 0
        self.current_word = None
        self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
    
    def start_session(self, limit=None):
        """Start a new study session"""
        if limit:
            self.current_words = [w for w in self.vocabulary if int(w['rank']) <= limit]
        else:
            self.current_words = self.vocabulary.copy()
        
        random.shuffle(self.current_words)
        self.current_index = 0
        self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
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
        # Get words in range
        range_words = [w for w in self.vocabulary if int(w['rank']) <= top_n]
        
        # Filter to words needing practice
        needs_practice = []
        for w in range_words:
            word_key = f"{w['rank']}_{w['hebrew']}"
            if (word_key in self.progress.get('hard', []) or 
                word_key in self.progress.get('again', [])):
                needs_practice.append(w)
        
        if needs_practice:
            self.current_words = needs_practice
            random.shuffle(self.current_words)
            self.current_index = 0
            self.session_stats = {'correct': 0, 'incorrect': 0, 'total': 0}
        
        return len(needs_practice)
    
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
