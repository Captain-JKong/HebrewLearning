#!/usr/bin/env python
"""
Hebrew Learning App - Main Application
Modular version with separated concerns
Rewritten for Flet
"""

import flet as ft
import random

from config import Config
from database_manager import DatabaseManager
from data_manager import VocabularyManager, ProgressManager, get_database_path
from audio_player import AudioPlayer
from session_manager import SessionManager
from ui_components import UIBuilder, DialogHelper, Themes

class HebrewLearningApp:
    """Main application class"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = Config.APP_NAME
        self.page.window_width = Config.WINDOW_WIDTH
        self.page.window_height = Config.WINDOW_HEIGHT
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
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
        self.page.bgcolor = self.theme['bg']
        self.ui_builder = UIBuilder(self.page, self.theme)
        
        # Set icon
        if self.paths['icon'].exists():
            self.page.window.icon = str(self.paths['icon'])
        
        # Build interface
        self.widgets = self.create_main_interface()
        self.setup_keyboard_shortcuts()
        
        # Handle window close
        self.page.on_window_event = self.on_window_event
    
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
        """Create the main interface"""
        
        # Define callback functions for the UI
        # Note: Flet buttons pass an event argument, so we need to handle it
        # We use e=None to allow calling with or without an event argument
        callbacks = {
            'toggle_theme': lambda e=None: self.toggle_theme(),
            'play_audio': lambda e=None: self.play_audio(),
            'show_answer': lambda e=None: self.show_answer(),
            'mark_again': lambda e=None: self.mark_answer('again'),
            'mark_hard': lambda e=None: self.mark_answer('hard'),
            'mark_good': lambda e=None: self.mark_answer('good'),
            'mark_easy': lambda e=None: self.mark_answer('easy')
        }
        
        # Get menu callbacks for navigation bar
        menu_callbacks = self._get_menu_callbacks()
        
        # Build complete interface
        widgets = self.ui_builder.build_complete_interface(callbacks, menu_callbacks)
        
        # Store references to labels for easy access
        self.progress_label = widgets['progress_label']
        self.stats_label = widgets['stats_label']
        
        # Initialize display
        self._show_welcome_message(widgets)
        self._hide_response_buttons(widgets)
        self._set_button_state(widgets, 'audio_btn', True) # Disabled
        self._set_button_state(widgets, 'show_answer_btn', True) # Disabled
        
        return widgets
    
    def _set_button_state(self, widgets, button_name, disabled):
        """Set button state"""
        if button_name in widgets:
            button = widgets[button_name]
            button.disabled = disabled
            button.update()
    
    def _show_welcome_message(self, widgets):
        """Show welcome message"""
        widgets['hebrew_text'].value = "Welcome! 🎓"
        widgets['trans_text'].value = "Click 'Study' above to begin learning Hebrew!"
        widgets['english_text'].value = ""
        self.page.update()
    
    def _hide_response_buttons(self, widgets):
        """Hide all response buttons"""
        for btn_name in ['again_btn', 'hard_btn', 'good_btn', 'easy_btn']:
            widgets[btn_name].visible = False
            widgets[btn_name].disabled = True
        self.page.update()
    
    def _show_response_buttons(self, widgets):
        """Show all response buttons"""
        for btn_name in ['again_btn', 'hard_btn', 'good_btn', 'easy_btn']:
            widgets[btn_name].visible = True
            widgets[btn_name].disabled = False
        self.page.update()
    
    def start_session(self, limit):
        """Start a study session"""
        count = self.session.start_session(limit)
        label = f"Top {limit}" if limit else "All Words"
        self.progress_label.value = f"Studying {label} ({count} words)"
        self.show_next_word()
    
    def show_custom_range_dialog(self):
        """Show custom range selection dialog"""
        DialogHelper.show_custom_range_dialog(self.page, self.start_custom_session)
    
    def start_custom_session(self, start_rank, end_rank):
        """Start session with custom range"""
        count = self.session.start_custom_session(start_rank, end_rank)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"No words found in rank range {start_rank}-{end_rank}"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"Custom Range: {start_rank}-{end_rank} ({count} words)"
        self.show_next_word()
    
    def practice_difficult_words(self, top_n):
        """Practice difficult words"""
        count = self.session.practice_difficult_words(top_n)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"No words needing practice in top {top_n}!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"Practicing {count} Words Needing Review in Top {top_n}"
        self.show_next_word()
    
    # ========== NEW STUDY MODE HANDLERS ==========
    
    def start_srs_session(self):
        """Start SRS review session"""
        count = self.session.start_srs_session()
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("No words due for review today!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"SRS Review: {count} words due today"
        self.show_next_word()
    
    def start_new_words_session(self):
        """Start learning new words session"""
        count = self.session.start_new_words_session(limit=10)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("You've already reviewed all words!"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"Learning {count} New Words"
        self.show_next_word()
    
    def start_category_session(self, category):
        """Start category-based session"""
        count = self.session.start_category_session(category)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"No words found in category: {category}"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"Category: {category} ({count} words)"
        self.show_next_word()
    
    def start_register_session(self, register):
        """Start register-based session (modern/biblical/both)"""
        count = self.session.start_register_session(register)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"No words found for register: {register}"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        register_label = {"modern": "Modern Hebrew", "biblical": "Biblical Hebrew", "both": "Modern & Biblical"}
        self.progress_label.value = f"{register_label.get(register, register)}: {count} words"
        self.show_next_word()
    
    def start_part_of_speech_session(self, pos):
        """Start part-of-speech session"""
        count = self.session.start_part_of_speech_session(pos)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"No {pos}s found in vocabulary"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"{pos.title()}s: {count} words"
        self.show_next_word()
    
    def start_weak_words_session(self):
        """Start weakest words session"""
        count = self.session.start_weak_words_session(limit=20)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("No words with progress data found"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"Reviewing 20 Weakest Words ({count} found)"
        self.show_next_word()
    
    def start_strong_words_session(self):
        """Start strongest words session"""
        count = self.session.start_strong_words_session(limit=20)
        if count == 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("No words with progress data found"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.progress_label.value = f"Reviewing 20 Strongest Words ({count} found)"
        self.show_next_word()
    
    def start_random_session(self):
        """Start random words session"""
        count = self.session.start_random_session(count=10)
        self.progress_label.value = f"Random Selection: {count} words"
        self.show_next_word()
    
    def show_next_word(self):
        """Display the next word"""
        word = self.session.get_next_word()
        
        if word is None or self.session.is_complete():
            self.show_session_complete()
            return
        
        self.answer_shown = False
        
        # Update displays
        self.widgets['hebrew_text'].value = word['hebrew']
        self.widgets['trans_text'].value = word['transliteration']
        self.widgets['english_text'].value = ""
        
        # Clear extra info labels
        if 'root_text' in self.widgets:
            self.widgets['root_text'].value = ""
        if 'notes_text' in self.widgets:
            self.widgets['notes_text'].value = ""
        if 'variants_text' in self.widgets:
            self.widgets['variants_text'].value = ""
        if 'translations_text' in self.widgets:
            self.widgets['translations_text'].value = ""
        
        # Update stats
        self.stats_label.value = self.session.get_progress_text()
        
        # Enable buttons
        self._set_button_state(self.widgets, 'audio_btn', False) # Enabled
        self._set_button_state(self.widgets, 'show_answer_btn', False) # Enabled
        self._hide_response_buttons(self.widgets)
        
        self.page.update()
        
        # Auto-play audio
        if self.auto_play_audio:
            self.play_audio()
    
    def show_answer(self):
        """Reveal the answer"""
        if not self.answer_shown and self.session.current_word:
            self.answer_shown = True
            word = self.session.current_word
            
            # Show main English translation
            self.widgets['english_text'].value = word['english']
            
            # Show root if available
            if 'root_text' in self.widgets:
                root_value = word.get('root')
                if root_value:
                    self.widgets['root_text'].value = f"🔤 Root: {root_value}"
                else:
                    self.widgets['root_text'].value = ""
            
            # Show notes if available
            if 'notes_text' in self.widgets and word.get('notes'):
                self.widgets['notes_text'].value = f"ℹ️  {word['notes']}"
            
            # Show variants if enabled
            if self.show_variants and 'variants_text' in self.widgets and word.get('lemma_id'):
                variants = self.vocab_manager.db.get_lemma_variants(word['lemma_id'])
                if variants:
                    variant_text = "📝 Variants: " + ", ".join(
                        f"{v['form']} ({v['description']})" for v in variants
                    )
                    self.widgets['variants_text'].value = variant_text
            
            # Show translations if enabled
            if self.show_translations and 'translations_text' in self.widgets and word.get('lemma_id'):
                translations = self.vocab_manager.db.get_lemma_translations(word['lemma_id'])
                if translations:
                    trans_text = "🌍 Translations: " + ", ".join(
                        f"{t['language']}: {t['translation']}" for t in translations
                    )
                    self.widgets['translations_text'].value = trans_text
            
            self._show_response_buttons(self.widgets)
            self.page.update()
    
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
        
        self.widgets['hebrew_text'].value = "🎉 Session Complete!"
        self.widgets['trans_text'].value = f"Total: {stats['total']}  |  Good/Easy: {stats['correct']}  |  Hard/Again: {stats['incorrect']}"
        self.widgets['english_text'].value = ""
        
        self._set_button_state(self.widgets, 'audio_btn', True) # Disabled
        self._set_button_state(self.widgets, 'show_answer_btn', True) # Disabled
        self._hide_response_buttons(self.widgets)
        
        self.progress_label.value = "Select 'Study' to start a new session"
        self.page.update()
    
    def play_audio(self):
        """Play audio for current word"""
        if self.session.current_word:
            self.audio_player.play(self.session.current_word['hebrew'])
    
    def toggle_theme(self):
        """Toggle dark/light mode"""
        self.dark_mode = not self.dark_mode
        self.theme = Themes.get_theme(self.dark_mode)
        self.ui_builder.apply_theme(self.widgets, self.theme)
        
        print(f"Theme switched to {'dark' if self.dark_mode else 'light'} mode")
    
    def toggle_auto_play(self):
        """Toggle auto-play audio"""
        self.auto_play_audio = not self.auto_play_audio
        self._save_settings()
    
    def toggle_variants(self):
        """Toggle showing word variants"""
        self.show_variants = not self.show_variants
        self._save_settings()
    
    def toggle_translations(self):
        """Toggle showing translations"""
        self.show_translations = not self.show_translations
        self._save_settings()
    
    def reset_progress(self):
        """Reset all progress"""
        def on_yes(e):
            self.progress = self.progress_manager._create_empty_progress()
            self.progress_manager.save(self.progress)
            self.session.progress = self.progress
            self.page.dialog.open = False
            self.page.snack_bar = ft.SnackBar(ft.Text("Your progress has been reset."))
            self.page.snack_bar.open = True
            self.page.update()

        def on_no(e):
            self.page.dialog.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Reset Progress"),
            content=ft.Text("Are you sure you want to reset all progress?\nThis cannot be undone."),
            actions=[
                ft.TextButton("Yes", on_click=on_yes),
                ft.TextButton("No", on_click=on_no),
            ],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def show_about(self):
        """Show about dialog"""
        DialogHelper.show_about_dialog(self.page, len(self.vocabulary))
    
    def show_statistics(self):
        """Show statistics dialog"""
        DialogHelper.show_statistics(self.page, len(self.vocabulary), self.progress)

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        def on_keyboard(e: ft.KeyboardEvent):
            if e.key == " ":
                if self.session.current_word and not self.answer_shown:
                    self.show_answer()
            elif e.key in ["1", "A", "a"]:
                if self.answer_shown: self.mark_answer('again')
            elif e.key in ["2", "H", "h"]:
                if self.answer_shown: self.mark_answer('hard')
            elif e.key in ["3", "G", "g"]:
                if self.answer_shown: self.mark_answer('good')
            elif e.key in ["4", "E", "e"]:
                if self.answer_shown: self.mark_answer('easy')
            elif e.key in ["P", "p"]:
                if self.session.current_word: self.play_audio()
            elif e.key == "\\":
                self.toggle_theme()

        self.page.on_keyboard_event = on_keyboard
    
    def on_window_event(self, e):
        """Handle window events"""
        if e.data == "close":
            self._save_settings()
            self.db.close()
            self.page.window_destroy()

def main(page: ft.Page):
    app = HebrewLearningApp(page)
    page.title = "Hebrew Learning App"
    page.window.icon = "icon.png"

if __name__ == '__main__':
    ft.app(
        target=main,
        name="Hebrew Learning App",
        assets_dir="assets"
        )
