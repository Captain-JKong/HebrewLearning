#!/usr/bin/env python3
"""
Parse the learning_hebrew.py file and convert to CSV format.
"""
import csv
import re

def parse_hebrew_file(input_file, output_file):
    """Parse the hebrew vocabulary file and convert to CSV."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    vocabulary = []
    current_rank = None
    
    for line in lines:
        if not line.strip():
            continue
            
        # Split by tabs
        parts = line.split('\t')
        
        # Check if this line starts with a number (new rank entry)
        if parts[0].strip().isdigit():
            current_rank = int(parts[0].strip())
            # Handle lines with rank number
            if len(parts) >= 4:
                english = parts[1].strip()
                transliteration = parts[2].strip()
                hebrew = parts[3].strip()
                vocabulary.append({
                    'rank': current_rank,
                    'english': english,
                    'transliteration': transliteration,
                    'hebrew': hebrew
                })
        else:
            # This is a continuation line with additional meanings
            if len(parts) >= 3 and current_rank is not None:
                english = parts[0].strip()
                transliteration = parts[1].strip()
                hebrew = parts[2].strip()
                vocabulary.append({
                    'rank': current_rank,
                    'english': english,
                    'transliteration': transliteration,
                    'hebrew': hebrew
                })
    
    # Write to CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['rank', 'english', 'transliteration', 'hebrew'])
        writer.writeheader()
        writer.writerows(vocabulary)
    
    print(f"✓ Converted {len(vocabulary)} vocabulary entries to {output_file}")
    return len(vocabulary)

if __name__ == '__main__':
    parse_hebrew_file('learning_hebrew.txt', 'hebrew_vocabulary.csv')
