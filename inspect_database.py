#!/usr/bin/env python3
"""
Database Inspector - Query your Hebrew vocabulary database
Usage: python inspect_database.py
"""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'hebrew_vocabulary.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

# 1. All lemmas with their info
print_header("ALL LEMMAS")
c.execute('''
    SELECT lemma_id, lemma, transliteration, english, 
           part_of_speech, register, root, frequency_rank
    FROM lemmas 
    ORDER BY frequency_rank
''')
for row in c.fetchall():
    print(f"{row['frequency_rank']:2d}. {row['lemma']:8s} ({row['transliteration']:12s}) "
          f"= {row['english']:30s} [{row['part_of_speech']:12s}, {row['register']:10s}]")
    if row['root']:
        print(f"    Root: {row['root']}")

# 2. Words with variants
print_header("WORDS WITH VARIANTS")
c.execute('''
    SELECT l.lemma, l.transliteration, v.form, v.description
    FROM lemmas l
    JOIN variants v ON l.lemma_id = v.lemma_id
    ORDER BY l.frequency_rank, v.variant_id
''')
current_lemma = None
for row in c.fetchall():
    if row['lemma'] != current_lemma:
        print(f"\n{row['lemma']} ({row['transliteration']}):")
        current_lemma = row['lemma']
    print(f"  → {row['form']} ({row['description']})")

# 3. Categories and their words
print_header("CATEGORIES")
c.execute('SELECT category_id, name FROM categories ORDER BY name')
categories = c.fetchall()
for cat in categories:
    c.execute('''
        SELECT l.lemma, l.transliteration
        FROM lemmas l
        JOIN lemma_categories lc ON l.lemma_id = lc.lemma_id
        WHERE lc.category_id = ?
        ORDER BY l.frequency_rank
        LIMIT 10
    ''', (cat['category_id'],))
    words = c.fetchall()
    if words:
        word_list = ', '.join([f"{w['lemma']} ({w['transliteration']})" for w in words])
        print(f"\n{cat['name']}: {word_list}")

# 4. Words with translations
print_header("WORDS WITH TRANSLATIONS")
c.execute('''
    SELECT l.lemma, l.transliteration, t.language, t.translation
    FROM lemmas l
    JOIN translations t ON l.lemma_id = t.lemma_id
    ORDER BY l.frequency_rank, t.language
''')
current_lemma = None
for row in c.fetchall():
    if row['lemma'] != current_lemma:
        print(f"\n{row['lemma']} ({row['transliteration']}):")
        current_lemma = row['lemma']
    print(f"  {row['language']:8s}: {row['translation']}")

# 5. Progress statistics
print_header("LEARNING PROGRESS")
c.execute('''
    SELECT 
        familiarity,
        COUNT(*) as count,
        ROUND(AVG(easiness), 2) as avg_easiness,
        ROUND(AVG(interval), 1) as avg_interval,
        ROUND(AVG(streak), 1) as avg_streak
    FROM user_progress
    GROUP BY familiarity
    ORDER BY familiarity DESC
''')
levels = {1: 'Again (Need Review)', 2: 'Hard (Struggling)', 
          3: 'Good (Confident)', 4: 'Easy (Mastered)'}
for row in c.fetchall():
    print(f"\n{levels[row['familiarity']]}: {row['count']} words")
    print(f"  Avg Easiness: {row['avg_easiness']}")
    print(f"  Avg Interval: {row['avg_interval']} days")
    print(f"  Avg Streak: {row['avg_streak']}")

# 6. Due for review
print_header("DUE FOR REVIEW TODAY")
c.execute('''
    SELECT l.lemma, l.transliteration, l.english, 
           up.familiarity, up.next_review, up.streak
    FROM lemmas l
    JOIN user_progress up ON l.lemma_id = up.lemma_id
    WHERE DATE(up.next_review) <= DATE('now')
    ORDER BY up.next_review
''')
due = c.fetchall()
if due:
    for row in due:
        print(f"{row['lemma']:8s} ({row['transliteration']:12s}) - "
              f"Level: {row['familiarity']}, Streak: {row['streak']}, "
              f"Due: {row['next_review']}")
else:
    print("No words due for review today!")

# 7. Biblical Hebrew words
print_header("BIBLICAL HEBREW WORDS")
c.execute('''
    SELECT lemma, transliteration, english, notes
    FROM lemmas
    WHERE register IN ('biblical', 'both')
    ORDER BY frequency_rank
''')
for row in c.fetchall():
    note = f" - {row['notes']}" if row['notes'] else ""
    print(f"{row['lemma']:10s} ({row['transliteration']:12s}) = {row['english']:30s}{note}")

# 8. Word families (same root)
print_header("WORD FAMILIES (BY ROOT)")
c.execute('''
    SELECT root, COUNT(*) as count
    FROM lemmas
    WHERE root IS NOT NULL
    GROUP BY root
    HAVING count > 1
    ORDER BY count DESC
''')
roots = c.fetchall()
for root_row in roots:
    c.execute('''
        SELECT lemma, transliteration, english, part_of_speech
        FROM lemmas
        WHERE root = ?
        ORDER BY frequency_rank
    ''', (root_row['root'],))
    words = c.fetchall()
    print(f"\nRoot: {root_row['root']} ({root_row['count']} words)")
    for word in words:
        print(f"  {word['lemma']:8s} ({word['transliteration']:12s}) "
              f"= {word['english']:25s} [{word['part_of_speech']}]")

# 9. Parts of speech distribution
print_header("PARTS OF SPEECH DISTRIBUTION")
c.execute('''
    SELECT part_of_speech, COUNT(*) as count
    FROM lemmas
    GROUP BY part_of_speech
    ORDER BY count DESC
''')
for row in c.fetchall():
    print(f"{row['part_of_speech']:15s}: {row['count']} words")

# 10. Summary
print_header("DATABASE SUMMARY")
c.execute('SELECT COUNT(*) FROM lemmas')
total_lemmas = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM variants')
total_variants = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM categories')
total_categories = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM translations')
total_translations = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM user_progress')
total_progress = c.fetchone()[0]

print(f"\nTotal Lemmas: {total_lemmas}")
print(f"Total Variants: {total_variants}")
print(f"Total Categories: {total_categories}")
print(f"Total Translations: {total_translations}")
print(f"Words with Progress: {total_progress}")

conn.close()
print("\n" + "="*60 + "\n")
