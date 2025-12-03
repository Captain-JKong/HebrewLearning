"""
Database Manager
Handles SQLite database operations for Hebrew vocabulary learning
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random


class DatabaseManager:
    """Manages SQLite database for vocabulary and progress"""
    
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database and tables if they don't exist"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Enable column access by name
        
        cursor = self.connection.cursor()
        
        # Table 1: Lemmas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lemmas (
                lemma_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lemma TEXT NOT NULL,
                part_of_speech TEXT,
                transliteration TEXT,
                english TEXT,
                register TEXT,
                notes TEXT,
                root TEXT,
                audio_path TEXT,
                frequency_rank INTEGER
            )
        ''')
        
        # Table 2: Variants
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS variants (
                variant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lemma_id INTEGER NOT NULL,
                form TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (lemma_id) REFERENCES lemmas(lemma_id)
            )
        ''')
        
        # Table 3: Categories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Table 4: Lemma-Categories junction
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lemma_categories (
                lemma_id INTEGER,
                category_id INTEGER,
                PRIMARY KEY (lemma_id, category_id),
                FOREIGN KEY (lemma_id) REFERENCES lemmas(lemma_id),
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        ''')
        
        # Table 5: Translations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                translation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lemma_id INTEGER NOT NULL,
                language TEXT NOT NULL,
                translation TEXT NOT NULL,
                FOREIGN KEY (lemma_id) REFERENCES lemmas(lemma_id)
            )
        ''')
        
        # Table 6: User Progress
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                lemma_id INTEGER PRIMARY KEY,
                familiarity INTEGER DEFAULT 0,
                easiness REAL DEFAULT 2.5,
                interval INTEGER DEFAULT 0,
                last_reviewed DATE,
                next_review DATE,
                streak INTEGER DEFAULT 0,
                FOREIGN KEY (lemma_id) REFERENCES lemmas(lemma_id)
            )
        ''')
        
        self.connection.commit()
    
    def populate_sample_data(self):
        """Populate database with 30 sample words for testing"""
        cursor = self.connection.cursor()
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM lemmas')
        if cursor.fetchone()[0] > 0:
            print("Database already contains data. Skipping sample data insertion.")
            return
        
        print("Populating database with 30 sample words...")
        
        # Sample data: 30 words with diverse attributes
        lemmas_data = [
            # Modern Hebrew - Common words
            (1, 'שלום', 'interjection', 'shalom', 'peace / hello / goodbye', 'both', 'Most common greeting', 'שלם', None, 1),
            (2, 'תודה', 'interjection', 'toda', 'thank you', 'modern', None, 'ידה', None, 2),
            (3, 'כן', 'adverb', 'ken', 'yes', 'both', None, None, None, 3),
            (4, 'לא', 'adverb', 'lo', 'no / not', 'both', 'Most common negation', None, None, 4),
            (5, 'בבקשה', 'interjection', 'bevakasha', 'please / you\'re welcome', 'modern', None, 'בקש', None, 5),
            
            # Nouns
            (6, 'בית', 'noun', 'bayit', 'house', 'both', 'Construct form: בֵּית־', 'בית', None, 6),
            (7, 'ספר', 'noun', 'sefer', 'book', 'both', None, 'ספר', None, 7),
            (8, 'אדם', 'noun', 'adam', 'person / human', 'both', 'Also used as name Adam', 'אדם', None, 8),
            (9, 'מים', 'noun', 'mayim', 'water', 'both', 'Always plural', 'מים', None, 9),
            (10, 'אהבה', 'noun', 'ahava', 'love', 'both', None, 'אהב', None, 10),
            
            # Verbs - Present tense base forms
            (11, 'אוכל', 'verb', 'okhel', 'eat (m.s.)', 'both', 'Present tense masculine singular', 'אכל', None, 11),
            (12, 'הולך', 'verb', 'holekh', 'go / walk (m.s.)', 'both', 'Present tense masculine singular', 'הלך', None, 12),
            (13, 'עושה', 'verb', 'oseh', 'do / make (m.s.)', 'both', 'Present tense masculine singular', 'עשה', None, 13),
            (14, 'אומר', 'verb', 'omer', 'say (m.s.)', 'both', 'Present tense masculine singular', 'אמר', None, 14),
            (15, 'כותב', 'verb', 'kotev', 'write (m.s.)', 'both', 'Present tense masculine singular', 'כתב', None, 15),
            
            # Adjectives
            (16, 'טוב', 'adjective', 'tov', 'good (m.s.)', 'both', None, 'טוב', None, 16),
            (17, 'גדול', 'adjective', 'gadol', 'big / large (m.s.)', 'both', None, 'גדל', None, 17),
            (18, 'קטן', 'adjective', 'katan', 'small (m.s.)', 'both', None, 'קטן', None, 18),
            (19, 'יפה', 'adjective', 'yafe', 'beautiful (m.s.)', 'both', None, 'יפה', None, 19),
            (20, 'חדש', 'adjective', 'hadash', 'new (m.s.)', 'both', None, 'חדש', None, 20),
            
            # Biblical Hebrew words
            (21, 'בראשית', 'noun', 'bereshit', 'in the beginning', 'biblical', 'First word of Genesis', 'ראש', None, 21),
            (22, 'אלהים', 'noun', 'elohim', 'God', 'both', 'Plural form but singular meaning', 'אלה', None, 22),
            (23, 'ברא', 'verb', 'bara', 'create (past 3m.s.)', 'both', 'Perfect tense', 'ברא', None, 23),
            (24, 'הארץ', 'noun', 'ha\'aretz', 'the earth / the land', 'both', 'With definite article', 'ארץ', None, 24),
            (25, 'השמים', 'noun', 'hashamayim', 'the heavens / the sky', 'both', 'With definite article, always plural', 'שמה', None, 25),
            
            # Prepositions and particles
            (26, 'של', 'preposition', 'shel', 'of / belongs to', 'modern', 'Possessive particle', None, None, 26),
            (27, 'עם', 'preposition', 'im', 'with', 'both', None, None, None, 27),
            (28, 'אל', 'preposition', 'el', 'to / toward / God', 'both', 'Also used as name for God', None, None, 28),
            (29, 'על', 'preposition', 'al', 'on / about / concerning', 'both', None, None, None, 29),
            (30, 'את', 'particle', 'et', 'direct object marker / you (f.s.)', 'both', 'Untranslatable particle or pronoun', None, None, 30),
        ]
        
        cursor.executemany('''
            INSERT INTO lemmas (lemma_id, lemma, part_of_speech, transliteration, 
                              english, register, notes, root, audio_path, frequency_rank)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', lemmas_data)
        
        # Add variants for some words
        variants_data = [
            # בית variants
            (6, 'בתים', 'plural'),
            (6, 'ביתי', 'my house'),
            
            # ספר variants
            (7, 'ספרים', 'plural'),
            (7, 'ספרות', 'literature (derived)'),
            
            # טוב variants
            (16, 'טובה', 'feminine singular'),
            (16, 'טובים', 'masculine plural'),
            (16, 'טובות', 'feminine plural'),
            
            # גדול variants
            (17, 'גדולה', 'feminine singular'),
            (17, 'גדולים', 'masculine plural'),
            
            # אוכל variants
            (11, 'אוכלת', 'feminine singular'),
            (11, 'אוכלים', 'masculine plural'),
            (11, 'אכלתי', 'past 1st person singular'),
            (11, 'אוכל', 'future 1st person singular / present m.s.'),
            
            # הולך variants
            (12, 'הולכת', 'feminine singular'),
            (12, 'הולכים', 'masculine plural'),
            (12, 'הלכתי', 'past 1st person singular'),
        ]
        
        cursor.executemany('''
            INSERT INTO variants (lemma_id, form, description)
            VALUES (?, ?, ?)
        ''', variants_data)
        
        # Add categories
        categories = [
            'Greetings',
            'Basic Vocabulary',
            'Verbs',
            'Nouns',
            'Adjectives',
            'Biblical Hebrew',
            'Prepositions',
            'Common Words',
            'Torah',
            'Grammar Particles'
        ]
        
        for cat in categories:
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (cat,))
        
        # Map lemmas to categories
        lemma_categories_data = [
            (1, 1), (1, 8),  # שלום - Greetings, Common
            (2, 1), (2, 8),  # תודה - Greetings, Common
            (3, 2), (3, 8),  # כן - Basic, Common
            (4, 2), (4, 8),  # לא - Basic, Common
            (5, 1), (5, 8),  # בבקשה - Greetings, Common
            (6, 4), (6, 2),  # בית - Nouns, Basic
            (7, 4), (7, 2),  # ספר - Nouns, Basic
            (8, 4), (8, 2),  # אדם - Nouns, Basic
            (9, 4), (9, 2),  # מים - Nouns, Basic
            (10, 4),         # אהבה - Nouns
            (11, 3), (11, 8),  # אוכל - Verbs, Common
            (12, 3), (12, 8),  # הולך - Verbs, Common
            (13, 3), (13, 8),  # עושה - Verbs, Common
            (14, 3), (14, 8),  # אומר - Verbs, Common
            (15, 3),         # כותב - Verbs
            (16, 5), (16, 8),  # טוב - Adjectives, Common
            (17, 5),         # גדול - Adjectives
            (18, 5),         # קטן - Adjectives
            (19, 5),         # יפה - Adjectives
            (20, 5),         # חדש - Adjectives
            (21, 6), (21, 9),  # בראשית - Biblical, Torah
            (22, 6), (22, 9),  # אלהים - Biblical, Torah
            (23, 3), (23, 6), (23, 9),  # ברא - Verbs, Biblical, Torah
            (24, 4), (24, 6),  # הארץ - Nouns, Biblical
            (25, 4), (25, 6),  # השמים - Nouns, Biblical
            (26, 7), (26, 8),  # של - Prepositions, Common
            (27, 7), (27, 8),  # עם - Prepositions, Common
            (28, 7), (28, 6),  # אל - Prepositions, Biblical
            (29, 7), (29, 8),  # על - Prepositions, Common
            (30, 10), (30, 8),  # את - Grammar, Common
        ]
        
        cursor.executemany('''
            INSERT INTO lemma_categories (lemma_id, category_id)
            VALUES (?, ?)
        ''', lemma_categories_data)
        
        # Add translations for some words
        translations_data = [
            (1, 'Greek', 'ειρήνη (eirene)'),
            (1, 'Arabic', 'سلام (salam)'),
            (10, 'Greek', 'αγάπη (agape)'),
            (10, 'Russian', 'любовь (lyubov)'),
            (22, 'Greek', 'Θεός (Theos)'),
            (22, 'Arabic', 'الله (Allah)'),
            (23, 'Greek', 'κτίζω (ktizo)'),
            (23, 'Latin', 'creare'),
        ]
        
        cursor.executemany('''
            INSERT INTO translations (lemma_id, language, translation)
            VALUES (?, ?, ?)
        ''', translations_data)
        
        # Add sample user progress
        today = datetime.now().date()
        progress_data = []
        
        for lemma_id in range(1, 31):
            # Varied familiarity levels
            if lemma_id <= 10:
                familiarity = random.choice([3, 4])  # Good/Easy for common words
                easiness = 2.8 + random.random() * 0.5
                interval = random.randint(7, 30)
                streak = random.randint(3, 10)
                last_reviewed = today - timedelta(days=random.randint(1, 5))
                next_review = today + timedelta(days=interval)
            elif lemma_id <= 20:
                familiarity = random.choice([2, 3])  # Hard/Good
                easiness = 2.3 + random.random() * 0.4
                interval = random.randint(1, 7)
                streak = random.randint(1, 5)
                last_reviewed = today - timedelta(days=random.randint(0, 3))
                next_review = today + timedelta(days=interval)
            else:
                familiarity = random.choice([1, 2])  # Again/Hard
                easiness = 2.0 + random.random() * 0.3
                interval = random.randint(0, 3)
                streak = random.randint(0, 2)
                last_reviewed = today - timedelta(days=random.randint(0, 2))
                next_review = today
            
            progress_data.append((
                lemma_id,
                familiarity,
                round(easiness, 2),
                interval,
                last_reviewed.isoformat(),
                next_review.isoformat(),
                streak
            ))
        
        cursor.executemany('''
            INSERT INTO user_progress 
            (lemma_id, familiarity, easiness, interval, last_reviewed, next_review, streak)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', progress_data)
        
        self.connection.commit()
        print(f"✓ Successfully populated database with 30 lemmas, variants, categories, and progress data")
    
    def get_all_vocabulary(self):
        """Get all vocabulary as list of dictionaries (compatible with old format)"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT 
                l.lemma_id,
                l.lemma as hebrew,
                l.transliteration,
                l.english,
                l.part_of_speech,
                l.register,
                l.notes,
                l.root,
                l.frequency_rank as rank,
                up.familiarity,
                up.easiness,
                up.interval,
                up.last_reviewed,
                up.next_review,
                up.streak
            FROM lemmas l
            LEFT JOIN user_progress up ON l.lemma_id = up.lemma_id
            ORDER BY l.frequency_rank
        ''')
        
        rows = cursor.fetchall()
        vocabulary = []
        for row in rows:
            vocab_dict = {
                'lemma_id': row['lemma_id'],
                'hebrew': row['hebrew'],
                'transliteration': row['transliteration'],
                'english': row['english'],
                'rank': row['rank'],
                'part_of_speech': row['part_of_speech'],
                'register': row['register'],
                'notes': row['notes'],
                'root': row['root'],
                'familiarity': row['familiarity'],
                'easiness': row['easiness'],
                'interval': row['interval'],
                'last_reviewed': row['last_reviewed'],
                'next_review': row['next_review'],
                'streak': row['streak']
            }
            vocabulary.append(vocab_dict)
        
        return vocabulary
    
    def get_lemma_variants(self, lemma_id):
        """Get all variants for a lemma"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT form, description
            FROM variants
            WHERE lemma_id = ?
        ''', (lemma_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_lemma_categories(self, lemma_id):
        """Get all categories for a lemma"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT c.name
            FROM categories c
            JOIN lemma_categories lc ON c.category_id = lc.category_id
            WHERE lc.lemma_id = ?
        ''', (lemma_id,))
        return [row['name'] for row in cursor.fetchall()]
    
    def get_lemma_translations(self, lemma_id):
        """Get all translations for a lemma"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT language, translation
            FROM translations
            WHERE lemma_id = ?
        ''', (lemma_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def update_progress(self, lemma_id, familiarity, easiness=None, interval=None):
        """Update user progress for a lemma"""
        cursor = self.connection.cursor()
        today = datetime.now().date()
        
        # Calculate next review based on interval
        if interval is None:
            if familiarity == 1:  # Again
                interval = 0
            elif familiarity == 2:  # Hard
                interval = 1
            elif familiarity == 3:  # Good
                interval = 3
            else:  # Easy (4)
                interval = 7
        
        next_review = today + timedelta(days=interval)
        
        # Get current streak
        cursor.execute('SELECT streak FROM user_progress WHERE lemma_id = ?', (lemma_id,))
        row = cursor.fetchone()
        current_streak = row['streak'] if row else 0
        
        # Update streak
        new_streak = current_streak + 1 if familiarity >= 3 else 0
        
        # Calculate easiness (simplified SRS)
        if easiness is None:
            cursor.execute('SELECT easiness FROM user_progress WHERE lemma_id = ?', (lemma_id,))
            row = cursor.fetchone()
            current_easiness = row['easiness'] if row else 2.5
            
            # Adjust easiness based on performance
            if familiarity == 1:  # Again
                easiness = max(1.3, current_easiness - 0.2)
            elif familiarity == 2:  # Hard
                easiness = max(1.3, current_easiness - 0.1)
            elif familiarity == 4:  # Easy
                easiness = min(3.0, current_easiness + 0.1)
            else:  # Good
                easiness = current_easiness
        
        # Upsert progress
        cursor.execute('''
            INSERT INTO user_progress 
            (lemma_id, familiarity, easiness, interval, last_reviewed, next_review, streak)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(lemma_id) DO UPDATE SET
                familiarity = excluded.familiarity,
                easiness = excluded.easiness,
                interval = excluded.interval,
                last_reviewed = excluded.last_reviewed,
                next_review = excluded.next_review,
                streak = excluded.streak
        ''', (lemma_id, familiarity, round(easiness, 2), interval, 
              today.isoformat(), next_review.isoformat(), new_streak))
        
        self.connection.commit()
        return round(easiness, 2)
    
    def get_vocabulary_stats(self):
        """Get statistics about vocabulary progress"""
        cursor = self.connection.cursor()
        
        # Count by familiarity level
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN familiarity = 4 THEN 1 END) as easy,
                COUNT(CASE WHEN familiarity = 3 THEN 1 END) as good,
                COUNT(CASE WHEN familiarity = 2 THEN 1 END) as hard,
                COUNT(CASE WHEN familiarity = 1 THEN 1 END) as again,
                COUNT(CASE WHEN familiarity IS NULL OR familiarity = 0 THEN 1 END) as not_studied
            FROM lemmas l
            LEFT JOIN user_progress up ON l.lemma_id = up.lemma_id
        ''')
        
        return dict(cursor.fetchone())
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
