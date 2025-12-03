#!/usr/bin/env pythonw
"""
Hebrew Learning App - Main Application
Modular version with separated concerns
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import random

from config import Config
from data_manager import VocabularyManager, ProgressManager
from audio_player import AudioPlayer
from session_manager import SessionManager
from ui_components import UIBuilder, DialogHelper, Themes

class HebrewLearningApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(Config.APP_NAME)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        
        # Initialize paths
        self.paths = Config.get_paths()
        
        # Initialize managers
        self.vocab_manager = VocabularyManager(self.paths['vocab'])
        self.progress_manager = ProgressManager(self.paths['progress'])
        self.audio_player = AudioPlayer()
        
        # Load data
        self.vocabulary = self.vocab_manager.load()
        self.progress = self.progress_manager.load()
        
        # Initialize session manager
        self.session = SessionManager(self.vocabulary, self.progress)
        
        # App state
        self.dark_mode = False
        self.auto_play_audio = True
        self.answer_shown = False
        
        # UI setup
        self.theme = Themes.get_theme(self.dark_mode)
        self.root.configure(bg=self.theme['bg'])
        self.ui_builder = UIBuilder(self.root, self.theme)
        
        # Set icon
        self._set_icon()
        
        # Build interface
        self.create_menu()
        self.widgets = self.create_main_interface()
        self.setup_keyboard_shortcuts()
    
    def _set_icon(self):
        """Set application icon"""
        if self.paths['icon'].exists():
            try:
                icon_img = tk.PhotoImage(file=str(self.paths['icon']))
                self.root.iconphoto(True, icon_img)
            except:
                pass
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Study Menu
        study_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Study", menu=study_menu)
        
        # Quick Start submenu
        quick_menu = tk.Menu(study_menu, tearoff=0)
        study_menu.add_cascade(label="Quick Start", menu=quick_menu)
        quick_menu.add_command(label="Top 50 Words", command=lambda: self.start_session(50))
        quick_menu.add_command(label="Top 100 Words", command=lambda: self.start_session(100))
        quick_menu.add_command(label="Top 200 Words", command=lambda: self.start_session(200))
        quick_menu.add_command(label="All Words", command=lambda: self.start_session(None))
        quick_menu.add_separator()
        quick_menu.add_command(label="Custom Range...", command=self.show_custom_range_dialog)
        
        study_menu.add_separator()
        
        # Smart Study submenu
        smart_menu = tk.Menu(study_menu, tearoff=0)
        study_menu.add_cascade(label="Smart Study", menu=smart_menu)
        smart_menu.add_command(label="SRS Review (Due Today)", command=self.start_srs_session)
        smart_menu.add_command(label="Learn New Words", command=self.start_new_words_session)
        smart_menu.add_command(label="Review Weakest Words", command=self.start_weak_words_session)
        smart_menu.add_command(label="Review Strongest Words", command=self.start_strong_words_session)
        smart_menu.add_separator()
        smart_menu.add_command(label="Practice Difficult (Top 50)", command=lambda: self.practice_difficult_words(50))
        smart_menu.add_command(label="Practice Difficult (Top 100)", command=lambda: self.practice_difficult_words(100))
        
        study_menu.add_separator()
        
        # By Category submenu
        category_menu = tk.Menu(study_menu, tearoff=0)
        study_menu.add_cascade(label="By Category", menu=category_menu)
        category_menu.add_command(label="Greetings", command=lambda: self.start_category_session("Greetings"))
        category_menu.add_command(label="Common Words", command=lambda: self.start_category_session("Common Words"))
        category_menu.add_command(label="Verbs", command=lambda: self.start_category_session("Verbs"))
        category_menu.add_command(label="Nouns", command=lambda: self.start_category_session("Nouns"))
        category_menu.add_command(label="Adjectives", command=lambda: self.start_category_session("Adjectives"))
        category_menu.add_separator()
        category_menu.add_command(label="Biblical Hebrew", command=lambda: self.start_category_session("Biblical Hebrew"))
        category_menu.add_command(label="Torah", command=lambda: self.start_category_session("Torah"))
        category_menu.add_separator()
        category_menu.add_command(label="Prepositions", command=lambda: self.start_category_session("Prepositions"))
        category_menu.add_command(label="Basic Vocabulary", command=lambda: self.start_category_session("Basic Vocabulary"))
        
        study_menu.add_separator()
        
        # By Type submenu
        type_menu = tk.Menu(study_menu, tearoff=0)
        study_menu.add_cascade(label="By Type", menu=type_menu)
        type_menu.add_command(label="Modern Hebrew", command=lambda: self.start_register_session("modern"))
        type_menu.add_command(label="Biblical Hebrew", command=lambda: self.start_register_session("biblical"))
        type_menu.add_command(label="Both Modern & Biblical", command=lambda: self.start_register_session("both"))
        type_menu.add_separator()
        type_menu.add_command(label="Verbs Only", command=lambda: self.start_part_of_speech_session("verb"))
        type_menu.add_command(label="Nouns Only", command=lambda: self.start_part_of_speech_session("noun"))
        type_menu.add_command(label="Adjectives Only", command=lambda: self.start_part_of_speech_session("adjective"))
        type_menu.add_command(label="Prepositions Only", command=lambda: self.start_part_of_speech_session("preposition"))
        
        study_menu.add_separator()
        study_menu.add_command(label="Random 10 Words", command=self.start_random_session)
        
        # Vocabulary Menu
        vocab_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Vocabulary", menu=vocab_menu)
        vocab_menu.add_command(label="Add New Words from File", command=self.import_vocabulary)
        vocab_menu.add_command(label="View Statistics", command=self.show_statistics)
        vocab_menu.add_separator()
        vocab_menu.add_command(label="Sort by Frequency", command=lambda: self.sort_vocabulary('frequency'))
        vocab_menu.add_command(label="Sort by Confidence", command=lambda: self.sort_vocabulary('confidence'))
        vocab_menu.add_command(label="Sort Alphabetically (Hebrew)", command=lambda: self.sort_vocabulary('hebrew'))
        vocab_menu.add_command(label="Sort Alphabetically (English)", command=lambda: self.sort_vocabulary('english'))
        
        # Settings Menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_checkbutton(
            label="Auto-play Audio",
            variable=tk.BooleanVar(value=self.auto_play_audio),
            command=self.toggle_auto_play
        )
        settings_menu.add_separator()
        settings_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)
        settings_menu.add_separator()
        settings_menu.add_command(label="Reset Progress", command=self.reset_progress)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_interface(self):
        """Create the main interface - all UI details are in ui_components.py"""
        # Define callback functions for the UI
        callbacks = {
            'toggle_theme': self.toggle_theme,
            'play_audio': self.play_audio,
            'show_answer': self.show_answer,
            'mark_again': lambda: self.mark_answer('again'),
            'mark_hard': lambda: self.mark_answer('hard'),
            'mark_good': lambda: self.mark_answer('good'),
            'mark_easy': lambda: self.mark_answer('easy')
        }
        
        # Build complete interface with all widgets
        widgets = self.ui_builder.build_complete_interface(callbacks)
        
        # Update theme toggle button icon based on current mode
        widgets['theme_toggle_btn']._text = "☀️" if self.dark_mode else "🌙"
        if hasattr(widgets['theme_toggle_btn'], '_draw_button'):
            widgets['theme_toggle_btn']._draw_button()
        
        # Store references to labels for easy access
        self.progress_label = widgets['progress_label']
        self.stats_label = widgets['stats_label']
        
        # Initialize display
        self._show_welcome_message(widgets)
        self._hide_response_buttons(widgets)
        self._set_button_state(widgets, 'audio_btn', tk.DISABLED)
        self._set_button_state(widgets, 'show_answer_btn', tk.DISABLED)
        
        return widgets
    
    def _set_button_state(self, widgets, button_name, state):
        """Set button state (handles canvas buttons, simple buttons, and containers)"""
        if button_name in widgets:
            button = widgets[button_name]
            
            # Canvas button (rounded)
            if hasattr(button, '_is_canvas_button'):
                button._state = state
                # Redraw to update appearance
                if hasattr(button, '_draw_button'):
                    button._draw_button()
            # Container with inner button
            elif hasattr(button, '_button'):
                button._button.config(state=state)
            # Simple button
            else:
                button.config(state=state)
    
    def _show_welcome_message(self, widgets):
        """Show welcome message"""
        self.ui_builder.update_text(widgets['hebrew_text'], "Welcome! 🎓")
        self.ui_builder.update_text(
            widgets['trans_text'],
            "Select 'Study' from the menu bar above\nto begin learning Hebrew!"
        )
        self.ui_builder.update_text(widgets['english_text'], "")
    
    def _hide_response_buttons(self, widgets):
        """Hide all response buttons"""
        for btn_name in ['again_btn', 'hard_btn', 'good_btn', 'easy_btn']:
            widgets[btn_name].grid_remove()
            self._set_button_state(widgets, btn_name, tk.DISABLED)
    
    def _show_response_buttons(self, widgets):
        """Show all response buttons"""
        for btn_name in ['again_btn', 'hard_btn', 'good_btn', 'easy_btn']:
            widgets[btn_name].grid()
            self._set_button_state(widgets, btn_name, tk.NORMAL)
    
    def start_session(self, limit):
        """Start a study session"""
        count = self.session.start_session(limit)
        label = f"Top {limit}" if limit else "All Words"
        self.progress_label.config(text=f"Studying {label} ({count} words)")
        self.show_next_word()
    
    def show_custom_range_dialog(self):
        """Show custom range selection dialog"""
        DialogHelper.show_custom_range_dialog(self.root, self.start_custom_session)
    
    def start_custom_session(self, start_rank, end_rank):
        """Start session with custom range"""
        count = self.session.start_custom_session(start_rank, end_rank)
        if count == 0:
            messagebox.showinfo("No Words", f"No words found in rank range {start_rank}-{end_rank}")
            return
        self.progress_label.config(text=f"Custom Range: {start_rank}-{end_rank} ({count} words)")
        self.show_next_word()
    
    def practice_difficult_words(self, top_n):
        """Practice difficult words"""
        count = self.session.practice_difficult_words(top_n)
        if count == 0:
            messagebox.showinfo(
                "Practice",
                f"No words needing practice in top {top_n}!\n"
                f"All words are marked as Good or Easy."
            )
            return
        self.progress_label.config(text=f"Practicing {count} Words Needing Review in Top {top_n}")
        self.show_next_word()
    
    # ========== NEW STUDY MODE HANDLERS ==========
    
    def start_srs_session(self):
        """Start SRS review session"""
        count = self.session.start_srs_session()
        if count == 0:
            messagebox.showinfo(
                "SRS Review",
                "No words due for review today!\n"
                "Come back tomorrow or study new words."
            )
            return
        self.progress_label.config(text=f"SRS Review: {count} words due today")
        self.show_next_word()
    
    def start_new_words_session(self):
        """Start learning new words session"""
        count = self.session.start_new_words_session(limit=10)
        if count == 0:
            messagebox.showinfo(
                "New Words",
                "You've already reviewed all words!\n"
                "Great job!"
            )
            return
        self.progress_label.config(text=f"Learning {count} New Words")
        self.show_next_word()
    
    def start_category_session(self, category):
        """Start category-based session"""
        count = self.session.start_category_session(category)
        if count == 0:
            messagebox.showinfo(
                "Category",
                f"No words found in category: {category}"
            )
            return
        self.progress_label.config(text=f"Category: {category} ({count} words)")
        self.show_next_word()
    
    def start_register_session(self, register):
        """Start register-based session (modern/biblical/both)"""
        count = self.session.start_register_session(register)
        if count == 0:
            messagebox.showinfo(
                "Register",
                f"No words found for register: {register}"
            )
            return
        register_label = {"modern": "Modern Hebrew", "biblical": "Biblical Hebrew", "both": "Modern & Biblical"}
        self.progress_label.config(text=f"{register_label.get(register, register)}: {count} words")
        self.show_next_word()
    
    def start_part_of_speech_session(self, pos):
        """Start part-of-speech session"""
        count = self.session.start_part_of_speech_session(pos)
        if count == 0:
            messagebox.showinfo(
                "Part of Speech",
                f"No {pos}s found in vocabulary"
            )
            return
        self.progress_label.config(text=f"{pos.title()}s: {count} words")
        self.show_next_word()
    
    def start_weak_words_session(self):
        """Start weakest words session"""
        count = self.session.start_weak_words_session(limit=20)
        if count == 0:
            messagebox.showinfo(
                "Weak Words",
                "No words with progress data found"
            )
            return
        self.progress_label.config(text=f"Reviewing 20 Weakest Words ({count} found)")
        self.show_next_word()
    
    def start_strong_words_session(self):
        """Start strongest words session"""
        count = self.session.start_strong_words_session(limit=20)
        if count == 0:
            messagebox.showinfo(
                "Strong Words",
                "No words with progress data found"
            )
            return
        self.progress_label.config(text=f"Reviewing 20 Strongest Words ({count} found)")
        self.show_next_word()
    
    def start_random_session(self):
        """Start random words session"""
        count = self.session.start_random_session(count=10)
        self.progress_label.config(text=f"Random Selection: {count} words")
        self.show_next_word()
    
    def show_next_word(self):
        """Display the next word"""
        word = self.session.get_next_word()
        
        if word is None or self.session.is_complete():
            self.show_session_complete()
            return
        
        self.answer_shown = False
        
        # Update displays
        self.ui_builder.update_text(self.widgets['hebrew_text'], word['hebrew'])
        self.ui_builder.update_text(self.widgets['trans_text'], word['transliteration'])
        self.ui_builder.update_text(self.widgets['english_text'], "")
        
        # Update stats
        self.stats_label.config(text=self.session.get_progress_text())
        
        # Enable buttons
        self._set_button_state(self.widgets, 'audio_btn', tk.NORMAL)
        self._set_button_state(self.widgets, 'show_answer_btn', tk.NORMAL)
        self._hide_response_buttons(self.widgets)
        
        # Auto-play audio
        if self.auto_play_audio:
            self.play_audio()
    
    def show_answer(self):
        """Reveal the answer"""
        if not self.answer_shown and self.session.current_word:
            self.answer_shown = True
            self.ui_builder.update_text(
                self.widgets['english_text'],
                self.session.current_word['english']
            )
            self._show_response_buttons(self.widgets)
    
    def mark_answer(self, confidence_level):
        """Mark answer with confidence level"""
        if not self.session.current_word:
            return
        
        # Use lemma_id for database (new system) or construct old key for backward compatibility
        word_key = self.session.current_word.get('lemma_id', f"{self.session.current_word['rank']}_{self.session.current_word['hebrew']}")
        
        # Update progress
        score = self.progress_manager.mark_word(self.progress, word_key, confidence_level)
        self.session.record_answer(confidence_level)
        self.progress_manager.save(self.progress)
        
        print(f"Marked '{word_key}' as {confidence_level.upper()} (score: {score:.2f})")
        
        # Move to next word
        self.session.advance()
        self.show_next_word()
    
    def show_session_complete(self):
        """Show session completion"""
        stats = self.session.session_stats
        
        self.ui_builder.update_text(
            self.widgets['hebrew_text'],
            "🎉 Session Complete!"
        )
        self.ui_builder.update_text(
            self.widgets['trans_text'],
            f"Total: {stats['total']}  |  Good/Easy: {stats['correct']}  |  Hard/Again: {stats['incorrect']}"
        )
        self.ui_builder.update_text(self.widgets['english_text'], "")
        
        self._set_button_state(self.widgets, 'audio_btn', tk.DISABLED)
        self._set_button_state(self.widgets, 'show_answer_btn', tk.DISABLED)
        self._hide_response_buttons(self.widgets)
        
        self.progress_label.config(text="Select 'Study' to start a new session")
    
    def play_audio(self):
        """Play audio for current word"""
        if self.session.current_word:
            self.audio_player.play(self.session.current_word['hebrew'])
    
    def toggle_theme(self):
        """Toggle dark/light mode"""
        self.dark_mode = not self.dark_mode
        self.theme = Themes.get_theme(self.dark_mode)
        self.ui_builder.apply_theme(self.widgets, self.theme)
        
        # Update theme toggle button icon
        if 'theme_toggle_btn' in self.widgets:
            new_icon = "☀️" if self.dark_mode else "🌙"
            btn = self.widgets['theme_toggle_btn']
            if hasattr(btn, '_text'):
                btn._text = new_icon
                if hasattr(btn, '_draw_button'):
                    btn._draw_button()
        
        print(f"Theme switched to {'dark' if self.dark_mode else 'light'} mode")
    
    def toggle_auto_play(self):
        """Toggle auto-play audio"""
        self.auto_play_audio = not self.auto_play_audio
    
    def reset_progress(self):
        """Reset all progress"""
        if messagebox.askyesno(
            "Reset Progress",
            "Are you sure you want to reset all progress?\\nThis cannot be undone."
        ):
            self.progress = self.progress_manager._create_empty_progress()
            self.progress_manager.save(self.progress)
            self.session.progress = self.progress
            messagebox.showinfo("Reset Complete", "Your progress has been reset.")
    
    def show_about(self):
        """Show about dialog"""
        DialogHelper.show_about_dialog(len(self.vocabulary))
    
    def show_statistics(self):
        """Show statistics dialog"""
        DialogHelper.show_statistics(len(self.vocabulary), self.progress)
    
    def import_vocabulary(self):
        """Import vocabulary from file"""
        filepath = filedialog.askopenfilename(
            title="Select vocabulary file",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_words = []
            for line in content.strip().split('\\n'):
                if not line.strip() or line.startswith('#'):
                    continue
                
                parts = line.strip().split('\\t')
                if len(parts) >= 4:
                    rank, english, trans, hebrew = parts[0], parts[1], parts[2], parts[3]
                    new_words.append({
                        'rank': int(rank) if rank.isdigit() else len(self.vocabulary) + len(new_words) + 1,
                        'english': english,
                        'transliteration': trans,
                        'hebrew': hebrew
                    })
            
            if new_words:
                self.vocabulary.extend(new_words)
                self.vocab_manager.save(self.vocabulary, self.paths['csv'])
                self.session.vocabulary = self.vocabulary
                
                messagebox.showinfo(
                    "Import Complete",
                    f"Successfully imported {len(new_words)} new words!\\n"
                    f"Total vocabulary: {len(self.vocabulary)} words"
                )
            else:
                messagebox.showwarning(
                    "No Words Found",
                    "Could not find any valid vocabulary entries in the file."
                )
        
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import vocabulary:\\n{str(e)}")
    
    def sort_vocabulary(self, sort_by):
        """Sort vocabulary"""
        if sort_by == 'frequency':
            self.vocabulary = self.vocab_manager.sort_by_frequency(self.vocabulary)
            message = "Sorted by frequency (rank order)"
        elif sort_by == 'confidence':
            confidence_scores = self.progress.get('confidence_scores', {})
            self.vocabulary = self.vocab_manager.sort_by_confidence(self.vocabulary, confidence_scores)
            message = "Sorted by confidence (highest confidence first)"
        elif sort_by == 'hebrew':
            self.vocabulary = self.vocab_manager.sort_by_hebrew(self.vocabulary)
            message = "Sorted alphabetically by Hebrew"
        elif sort_by == 'english':
            self.vocabulary = self.vocab_manager.sort_by_english(self.vocabulary)
            message = "Sorted alphabetically by English"
        
        # Re-assign ranks
        for i, word in enumerate(self.vocabulary, 1):
            word['rank'] = i
        
        self.vocab_manager.save(self.vocabulary, self.paths['csv'])
        self.session.vocabulary = self.vocabulary
        
        messagebox.showinfo("Vocabulary Sorted", message)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<space>', lambda e: self.show_answer() if self.session.current_word and not self.answer_shown else None)
        
        # Number keys
        self.root.bind('1', lambda e: self.mark_answer('again') if self.answer_shown else None)
        self.root.bind('2', lambda e: self.mark_answer('hard') if self.answer_shown else None)
        self.root.bind('3', lambda e: self.mark_answer('good') if self.answer_shown else None)
        self.root.bind('4', lambda e: self.mark_answer('easy') if self.answer_shown else None)
        
        # Letter shortcuts
        self.root.bind('a', lambda e: self.mark_answer('again') if self.answer_shown else None)
        self.root.bind('A', lambda e: self.mark_answer('again') if self.answer_shown else None)
        self.root.bind('h', lambda e: self.mark_answer('hard') if self.answer_shown else None)
        self.root.bind('H', lambda e: self.mark_answer('hard') if self.answer_shown else None)
        self.root.bind('g', lambda e: self.mark_answer('good') if self.answer_shown else None)
        self.root.bind('G', lambda e: self.mark_answer('good') if self.answer_shown else None)
        self.root.bind('e', lambda e: self.mark_answer('easy') if self.answer_shown else None)
        self.root.bind('E', lambda e: self.mark_answer('easy') if self.answer_shown else None)
        
        # Audio
        self.root.bind('p', lambda e: self.play_audio() if self.session.current_word else None)
        self.root.bind('P', lambda e: self.play_audio() if self.session.current_word else None)
        
        # Theme toggle
        self.root.bind('\\', lambda e: self.toggle_theme())

def main():
    root = tk.Tk()
    app = HebrewLearningApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
