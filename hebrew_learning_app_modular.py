#!/usr/bin/env pythonw
"""
Hebrew Learning App - Main Application
Modular version with separated concerns
"""

import tkinter as tk
from tkinter import messagebox
import random

from config import Config
from database_manager import DatabaseManager
from data_manager import VocabularyManager, ProgressManager, get_database_path
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
        
        # Create shared database connection
        db_path = get_database_path(self.paths['vocab'])
        self.db = DatabaseManager(db_path)
        
        # Initialize managers with shared database
        self.vocab_manager = VocabularyManager(self.db)
        self.progress_manager = ProgressManager(self.db)
        self.audio_player = AudioPlayer()
        
        # Load data
        self.vocabulary = self.vocab_manager.load()
        self.progress = self.progress_manager.load()
        
        # Initialize session manager with shared database
        self.session = SessionManager(self.vocabulary, self.progress, self.db)
        
        # Load settings from database
        self.settings = self._load_settings()
        
        # App state
        self.dark_mode = False
        self.auto_play_audio = self.settings.get('auto_play_audio', True)
        self.answer_shown = False
        self.show_variants = self.settings.get('show_variants', False)
        self.show_translations = self.settings.get('show_translations', False)
        
        # UI setup
        self.theme = Themes.get_theme(self.dark_mode)
        self.root.configure(bg=self.theme['bg'])
        self.ui_builder = UIBuilder(self.root, self.theme)
        
        # Set icon
        self._set_icon()
        
        # Build interface (navigation bar is built within create_main_interface)
        self.widgets = self.create_main_interface()
        self.setup_keyboard_shortcuts()
    
    def _load_settings(self):
        """Load settings from database"""
        return {
            'auto_play_audio': self.db.get_setting('auto_play_audio', True),
            'show_variants': self.db.get_setting('show_variants', False),
            'show_translations': self.db.get_setting('show_translations', False)
        }
    
    def _save_settings(self):
        """Save settings to database"""
        self.db.save_setting('auto_play_audio', self.auto_play_audio)
        self.db.save_setting('show_variants', self.show_variants)
        self.db.save_setting('show_translations', self.show_translations)
    
    def _set_icon(self):
        """Set application icon"""
        if self.paths['icon'].exists():
            try:
                icon_img = tk.PhotoImage(file=str(self.paths['icon']))
                self.root.iconphoto(True, icon_img)
            except tk.TclError:
                pass
    
    def _get_menu_callbacks(self):
        """Get all menu action callbacks for the navigation bar"""
        return {
            # Quick Start
            'start_50': lambda: self.start_session(50),
            'start_100': lambda: self.start_session(100),
            'start_200': lambda: self.start_session(200),
            'start_all': lambda: self.start_session(None),
            'custom_range': self.show_custom_range_dialog,
            
            # Smart Study
            'srs_review': self.start_srs_session,
            'new_words': self.start_new_words_session,
            'weak_words': self.start_weak_words_session,
            'strong_words': self.start_strong_words_session,
            'difficult_50': lambda: self.practice_difficult_words(50),
            'difficult_100': lambda: self.practice_difficult_words(100),
            
            # By Category
            'cat_greetings': lambda: self.start_category_session("Greetings"),
            'cat_common': lambda: self.start_category_session("Common Words"),
            'cat_verbs': lambda: self.start_category_session("Verbs"),
            'cat_nouns': lambda: self.start_category_session("Nouns"),
            'cat_adjectives': lambda: self.start_category_session("Adjectives"),
            'cat_biblical': lambda: self.start_category_session("Biblical Hebrew"),
            'cat_torah': lambda: self.start_category_session("Torah"),
            'cat_prepositions': lambda: self.start_category_session("Prepositions"),
            'cat_basic': lambda: self.start_category_session("Basic Vocabulary"),
            
            # By Type
            'type_modern': lambda: self.start_register_session("modern"),
            'type_biblical': lambda: self.start_register_session("biblical"),
            'type_both': lambda: self.start_register_session("both"),
            'pos_verb': lambda: self.start_part_of_speech_session("verb"),
            'pos_noun': lambda: self.start_part_of_speech_session("noun"),
            'pos_adjective': lambda: self.start_part_of_speech_session("adjective"),
            'pos_preposition': lambda: self.start_part_of_speech_session("preposition"),
            
            # Random
            'random_10': self.start_random_session,
            
            # Settings
            'toggle_variants': self.toggle_variants,
            'toggle_translations': self.toggle_translations,
            'toggle_auto_play': self.toggle_auto_play,
            'reset_progress': self.reset_progress,
            
            # Vocabulary
            'show_statistics': self.show_statistics,
            
            # Help
            'show_about': self.show_about,
        }
    
    def create_main_interface(self):
        """Create the main interface - all UI details are in ui_components.py"""
        # Create persistent checkbox variables for settings menu
        self.show_variants_var = tk.BooleanVar(value=self.show_variants)
        self.show_translations_var = tk.BooleanVar(value=self.show_translations)
        self.auto_play_var = tk.BooleanVar(value=self.auto_play_audio)
        
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
        
        # Get menu callbacks for navigation bar
        menu_callbacks = self._get_menu_callbacks()
        
        # Checkbox variables for settings menu
        checkbox_vars = {
            'show_variants': self.show_variants_var,
            'show_translations': self.show_translations_var,
            'auto_play': self.auto_play_var,
        }
        
        # Build complete interface with all widgets including navigation bar
        widgets = self.ui_builder.build_complete_interface(callbacks, menu_callbacks, checkbox_vars)
        
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
        """Set button state (handles all button types via duck typing)"""
        if button_name in widgets:
            button = widgets[button_name]
            button._state = state
            if hasattr(button, '_draw_button'):
                button._draw_button()
    
    def _show_welcome_message(self, widgets):
        """Show welcome message"""
        self.ui_builder.update_text(widgets['hebrew_text'], "Welcome! 🎓")
        self.ui_builder.update_text(
            widgets['trans_text'],
            "Click 'Study' above to begin learning Hebrew!"
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
        
        # Clear extra info labels
        if 'root_text' in self.widgets:
            self.widgets['root_text'].config(text="")
        if 'notes_text' in self.widgets:
            self.widgets['notes_text'].config(text="")
        if 'variants_text' in self.widgets:
            self.widgets['variants_text'].config(text="")
        if 'translations_text' in self.widgets:
            self.widgets['translations_text'].config(text="")
        
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
            word = self.session.current_word
            
            # Show main English translation
            self.ui_builder.update_text(
                self.widgets['english_text'],
                word['english']
            )
            
            # Show root if available
            if 'root_text' in self.widgets:
                root_value = word.get('root')
                if root_value:
                    self.widgets['root_text'].config(text=f"🔤 Root: {root_value}")
                else:
                    self.widgets['root_text'].config(text="")
            
            # Show notes if available
            if 'notes_text' in self.widgets and word.get('notes'):
                self.widgets['notes_text'].config(text=f"ℹ️  {word['notes']}")
            
            # Show variants if enabled
            if self.show_variants and 'variants_text' in self.widgets and word.get('lemma_id'):
                variants = self.vocab_manager.db.get_lemma_variants(word['lemma_id'])
                if variants:
                    variant_text = "📝 Variants: " + ", ".join(
                        f"{v['form']} ({v['description']})" for v in variants
                    )
                    self.widgets['variants_text'].config(text=variant_text)
            
            # Show translations if enabled
            if self.show_translations and 'translations_text' in self.widgets and word.get('lemma_id'):
                translations = self.vocab_manager.db.get_lemma_translations(word['lemma_id'])
                if translations:
                    trans_text = "🌍 Translations: " + ", ".join(
                        f"{t['language']}: {t['translation']}" for t in translations
                    )
                    self.widgets['translations_text'].config(text=trans_text)
            
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
        self.auto_play_audio = self.auto_play_var.get()
        self._save_settings()
    
    def toggle_variants(self):
        """Toggle showing word variants"""
        self.show_variants = self.show_variants_var.get()
        self._save_settings()
    
    def toggle_translations(self):
        """Toggle showing translations"""
        self.show_translations = self.show_translations_var.get()
        self._save_settings()
    
    def reset_progress(self):
        """Reset all progress"""
        if messagebox.askyesno(
            "Reset Progress",
            "Are you sure you want to reset all progress?\nThis cannot be undone."
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

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Answer visibility
        self.root.bind('<space>', lambda e: self.show_answer() if self.session.current_word and not self.answer_shown else None)
        
        # Confidence levels - consolidated
        shortcuts = {
            'again': ['1', 'a', 'A'],
            'hard': ['2', 'h', 'H'],
            'good': ['3', 'g', 'G'],
            'easy': ['4', 'e', 'E']
        }
        for action, keys in shortcuts.items():
            for key in keys:
                self.root.bind(key, lambda e, a=action: self.mark_answer(a) if self.answer_shown else None)
        
        # Audio and theme
        for key in ['p', 'P']:
            self.root.bind(key, lambda e: self.play_audio() if self.session.current_word else None)
        self.root.bind('\\', lambda e: self.toggle_theme())
    
    def on_closing(self):
        """Handle app closing - cleanup database connection"""
        self._save_settings()
        self.db.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = HebrewLearningApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
