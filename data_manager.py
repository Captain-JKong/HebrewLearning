"""
Data Management
Handles vocabulary and progress data loading/saving
"""

import csv
import json
import sys
from pathlib import Path
from datetime import datetime

class VocabularyManager:
    """Manages vocabulary data"""
    
    def __init__(self, vocab_file):
        self.vocab_file = vocab_file
        self.vocabulary = []
    
    def load(self):
        """Load vocabulary from CSV file"""
        try:
            with open(self.vocab_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.vocabulary = list(reader)
            print(f"✓ Loaded {len(self.vocabulary)} vocabulary entries")
            return self.vocabulary
        except FileNotFoundError:
            raise Exception(f"Vocabulary file not found: {self.vocab_file}")
    
    def save(self, vocabulary, csv_file):
        """Save vocabulary list to CSV file"""
        # If running from PyInstaller bundle, save to user's home directory
        if getattr(sys, 'frozen', False):
            save_path = Path.home() / '.hebrew_learning' / 'hebrew_vocabulary.csv'
            save_path.parent.mkdir(exist_ok=True)
        else:
            save_path = csv_file
        
        try:
            with open(save_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['rank', 'english', 'transliteration', 'hebrew'])
                writer.writeheader()
                writer.writerows(vocabulary)
            print(f"✓ Saved {len(vocabulary)} words to {save_path}")
        except Exception as e:
            print(f"Error saving vocabulary: {e}")
    
    def sort_by_frequency(self, vocabulary):
        """Sort by rank (frequency)"""
        vocabulary.sort(key=lambda x: x['rank'])
        return vocabulary
    
    def sort_by_confidence(self, vocabulary, confidence_scores):
        """Sort by confidence score (descending)"""
        def get_confidence(word):
            word_key = f"{word['rank']}_{word['hebrew']}"
            return confidence_scores.get(word_key, 0)
        vocabulary.sort(key=get_confidence, reverse=True)
        return vocabulary
    
    def sort_by_hebrew(self, vocabulary):
        """Sort alphabetically by Hebrew"""
        vocabulary.sort(key=lambda x: x['hebrew'])
        return vocabulary
    
    def sort_by_english(self, vocabulary):
        """Sort alphabetically by English"""
        vocabulary.sort(key=lambda x: x['english'].lower())
        return vocabulary

class ProgressManager:
    """Manages learning progress data"""
    
    def __init__(self, progress_file):
        self.progress_file = progress_file
    
    def load(self):
        """Load progress from JSON file"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return self._create_empty_progress()
    
    def save(self, progress):
        """Save progress to JSON file"""
        progress['last_session'] = datetime.now().isoformat()
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, indent=2, fp=f)
    
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
        """Mark a word with confidence level and update scores"""
        # Remove from all categories
        for category in ['easy', 'good', 'hard', 'again']:
            if word_key in progress.get(category, []):
                progress[category].remove(word_key)
        
        # Add to appropriate category
        progress.setdefault(confidence_level, []).append(word_key)
        
        # Update confidence score (running average)
        confidence_values = {'again': 1, 'hard': 2, 'good': 3, 'easy': 4}
        scores = progress.setdefault('confidence_scores', {})
        
        if word_key in scores:
            # Calculate running average (weight: 70% old, 30% new)
            old_score = scores[word_key]
            new_score = confidence_values[confidence_level]
            scores[word_key] = old_score * 0.7 + new_score * 0.3
        else:
            scores[word_key] = confidence_values[confidence_level]
        
        return scores[word_key]
