#!/usr/bin/env pythonw
"""
Hebrew Learning App - Main Application
Modular version with separated concerns
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import random

from config import Config, Themes
from data_manager import VocabularyManager, ProgressManager
from audio_player import AudioPlayer
from session_manager import SessionManager
from ui_components import UIBuilder, DialogHelper

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
        self.widgets = {}
        self.create_menu()
        self.create_main_interface()
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
        study_menu.add_command(label="Top 50 Words", command=lambda: self.start_session(50))
        study_menu.add_command(label="Top 100 Words", command=lambda: self.start_session(100))
        study_menu.add_command(label="Top 200 Words", command=lambda: self.start_session(200))
        study_menu.add_command(label="All Words (300)", command=lambda: self.start_session(None))
        study_menu.add_separator()
        study_menu.add_command(label="Custom Range...", command=self.show_custom_range_dialog)
        study_menu.add_separator()
        study_menu.add_command(label="Practice Hard/Again in Top 50", command=lambda: self.practice_difficult_words(50))
        study_menu.add_command(label="Practice Hard/Again in Top 100", command=lambda: self.practice_difficult_words(100))
        
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
        """Create the main interface"""
        # Title frame
        title_frame = tk.Frame(self.root, bg=self.theme['bg'])
        title_frame.pack(pady=20)
        
        tk.Label(
            title_frame,
            text="Hebrew Learning App",
            font=('Helvetica', 24, 'bold'),
            bg=self.theme['bg']
        ).pack()
        
        self.progress_label = tk.Label(
            title_frame,
            text="",
            font=('Helvetica', 11),
            bg=self.theme['bg'],
            fg='#666'
        )
        self.progress_label.pack()
        
        self.stats_label = tk.Label(
            title_frame,
            text="",
            font=('Helvetica', 11),
            bg=self.theme['bg'],
            fg='#666'
        )
        self.stats_label.pack(pady=10)
        
        # Card frame
        self.widgets['card_frame'] = self.ui_builder.create_card_frame()
        
        # Text widgets
        self.widgets['hebrew_text'] = self.ui_builder.create_text_widget(
            self.widgets['card_frame'], 3, ('Arial Hebrew', 36, 'bold'),
            self.theme['text_bg'], self.theme['text_fg']
        )
        
        self.widgets['trans_text'] = self.ui_builder.create_text_widget(
            self.widgets['card_frame'], 2, ('Helvetica', 18),
            self.theme['trans_bg'], self.theme['trans_fg']
        )
        
        self.widgets['english_text'] = self.ui_builder.create_text_widget(
            self.widgets['card_frame'], 2, ('Helvetica', 20, 'bold'),
            self.theme['english_bg'], self.theme['english_fg']
        )
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg=self.theme['bg'])
        button_frame.pack(pady=10)
        
        self.widgets['audio_btn'] = self.ui_builder.create_button(
            button_frame, "🔊 Play Audio", self.play_audio,
            self.theme['btn_audio'], padx=25, pady=12
        )
        self.widgets['audio_btn'].grid(row=0, column=0, padx=8)
        
        self.widgets['show_answer_btn'] = self.ui_builder.create_button(
            button_frame, "👁 Show Answer", self.show_answer,
            self.theme['btn_answer'], padx=25, pady=12
        )
        self.widgets['show_answer_btn'].grid(row=0, column=1, padx=8)
        
        # Response buttons
        self.response_frame = tk.Frame(self.root, bg=self.theme['bg'])
        self.response_frame.pack(pady=10)
        
        self.widgets['again_btn'] = self.ui_builder.create_button(
            self.response_frame, "Again (1)", lambda: self.mark_answer('again'),
            self.theme['btn_again'], font_size=11, padx=18
        )
        self.widgets['again_btn'].grid(row=0, column=0, padx=4)
        
        self.widgets['hard_btn'] = self.ui_builder.create_button(
            self.response_frame, "Hard (2)", lambda: self.mark_answer('hard'),
            self.theme['btn_hard'], font_size=11, padx=18
        )
        self.widgets['hard_btn'].grid(row=0, column=1, padx=4)
        
        self.widgets['good_btn'] = self.ui_builder.create_button(
            self.response_frame, "Good (3)", lambda: self.mark_answer('good'),
            self.theme['btn_good'], font_size=11, padx=18
        )
        self.widgets['good_btn'].grid(row=0, column=2, padx=4)
        
        self.widgets['easy_btn'] = self.ui_builder.create_button(
            self.response_frame, "Easy (4)", lambda: self.mark_answer('easy'),
            self.theme['btn_easy'], font_size=11, padx=18
        )
        self.widgets['easy_btn'].grid(row=0, column=3, padx=4)
        
        # Keyboard shortcuts hint
        tk.Label(
            self.response_frame,
            text="Keyboard: 1=Again  2=Hard  3=Good  4=Easy  |  Space=Show  P=Audio",
            font=('Helvetica', 9, 'italic'),
            bg=self.theme['bg'],
            fg='#666666'
        ).grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        # Initialize display
        self._show_welcome_message()
        self._hide_response_buttons()
        self.widgets['audio_btn'].config(state=tk.DISABLED)
        self.widgets['show_answer_btn'].config(state=tk.DISABLED)
    
    def _show_welcome_message(self):
        """Show welcome message"""
        self.ui_builder.update_text(self.widgets['hebrew_text'], "Welcome! 🎓")
        self.ui_builder.update_text(
            self.widgets['trans_text'],
            "Select 'Study' from the menu bar above\\nto begin learning Hebrew!"
        )
        self.ui_builder.update_text(self.widgets['english_text'], "")
    
    def _hide_response_buttons(self):
        """Hide all response buttons"""
        for btn_name in ['again_btn', 'hard_btn', 'good_btn', 'easy_btn']:
            self.widgets[btn_name].grid_remove()
            self.widgets[btn_name].config(state=tk.DISABLED)
    
    def _show_response_buttons(self):
        """Show all response buttons"""
        for btn_name in ['again_btn', 'hard_btn', 'good_btn', 'easy_btn']:
            self.widgets[btn_name].grid()
            self.widgets[btn_name].config(state=tk.NORMAL)
    
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
                f"No words needing practice in top {top_n}!\\n"
                f"All words are marked as Good or Easy."
            )
            return
        self.progress_label.config(text=f"Practicing {count} Words Needing Review in Top {top_n}")
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
        self.widgets['audio_btn'].config(state=tk.NORMAL)
        self.widgets['show_answer_btn'].config(state=tk.NORMAL)
        self._hide_response_buttons()
        
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
            self._show_response_buttons()
    
    def mark_answer(self, confidence_level):
        """Mark answer with confidence level"""
        if not self.session.current_word:
            return
        
        word_key = f"{self.session.current_word['rank']}_{self.session.current_word['hebrew']}"
        
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
        
        self.widgets['audio_btn'].config(state=tk.DISABLED)
        self.widgets['show_answer_btn'].config(state=tk.DISABLED)
        self._hide_response_buttons()
        
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

def main():
    root = tk.Tk()
    app = HebrewLearningApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
