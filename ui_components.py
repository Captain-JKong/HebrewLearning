"""
UI Components
Builds and manages the graphical interface
"""

import tkinter as tk
from tkinter import messagebox

class UIBuilder:
    """Builds UI components"""
    
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.widgets = {}
    
    def create_card_frame(self):
        """Create main card frame"""
        card_frame = tk.Frame(
            self.root, 
            bg=self.theme['card_bg'], 
            relief=tk.FLAT, 
            borderwidth=0, 
            highlightthickness=0
        )
        card_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        return card_frame
    
    def create_text_widget(self, parent, height, font, bg, fg):
        """Create a text display widget"""
        text_widget = tk.Text(
            parent,
            height=height,
            font=font,
            bg=bg,
            fg=fg,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            wrap=tk.WORD,
            padx=20 if height > 2 else 15,
            pady=15 if height > 2 else 10
        )
        text_widget.pack(fill=tk.BOTH if height > 2 else tk.X, expand=True if height > 2 else False, pady=8, padx=8)
        return text_widget
    
    def create_button(self, parent, text, command, bg, **kwargs):
        """Create a styled button"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg='white',
            font=('Helvetica', kwargs.get('font_size', 12), 'bold'),
            padx=kwargs.get('padx', 25),
            pady=kwargs.get('pady', 14),
            relief=tk.FLAT,
            cursor='hand2'
        )
        return button
    
    def update_text(self, text_widget, content):
        """Update text widget content"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete('1.0', tk.END)
        text_widget.insert('1.0', content)
        text_widget.config(state=tk.DISABLED)
    
    def apply_theme(self, widgets, theme):
        """Apply theme to widgets"""
        self.root.config(bg=theme['bg'])
        
        if 'card_frame' in widgets:
            widgets['card_frame'].config(bg=theme['card_bg'])
        
        if 'hebrew_text' in widgets:
            widgets['hebrew_text'].config(bg=theme['text_bg'], fg=theme['text_fg'])
        
        if 'trans_text' in widgets:
            widgets['trans_text'].config(bg=theme['trans_bg'], fg=theme['trans_fg'])
        
        if 'english_text' in widgets:
            widgets['english_text'].config(bg=theme['english_bg'], fg=theme['english_fg'])
        
        # Update buttons
        button_mappings = [
            ('audio_btn', 'btn_audio'),
            ('show_answer_btn', 'btn_answer'),
            ('again_btn', 'btn_again'),
            ('hard_btn', 'btn_hard'),
            ('good_btn', 'btn_good'),
            ('easy_btn', 'btn_easy')
        ]
        
        for widget_name, theme_key in button_mappings:
            if widget_name in widgets:
                widgets[widget_name].config(bg=theme[theme_key])

class DialogHelper:
    """Helper for creating dialogs"""
    
    @staticmethod
    def show_custom_range_dialog(root, callback):
        """Show dialog for custom rank range selection"""
        dialog = tk.Toplevel(root)
        dialog.title("Custom Range")
        dialog.geometry("300x150")
        dialog.transient(root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select rank range:", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        frame = tk.Frame(dialog)
        frame.pack(pady=10)
        
        tk.Label(frame, text="From rank:").grid(row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(frame, width=10)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        start_entry.insert(0, "1")
        
        tk.Label(frame, text="To rank:").grid(row=1, column=0, padx=5, pady=5)
        end_entry = tk.Entry(frame, width=10)
        end_entry.grid(row=1, column=1, padx=5, pady=5)
        end_entry.insert(0, "100")
        
        def on_ok():
            try:
                start = int(start_entry.get())
                end = int(end_entry.get())
                if start > 0 and end >= start:
                    dialog.destroy()
                    callback(start, end)
                else:
                    messagebox.showerror("Invalid Range", "Please enter valid rank numbers.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter numbers only.")
        
        tk.Button(dialog, text="Start Session", command=on_ok, bg='#2196f3', fg='white', padx=20, pady=10).pack(pady=10)
    
    @staticmethod
    def show_about_dialog(vocabulary_count):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            f"Hebrew Learning App\n"
            f"Version 2.5\n\n"
            f"Learn Hebrew vocabulary with flashcards\n"
            f"and audio pronunciation.\n\n"
            f"Total vocabulary: {vocabulary_count} words\n\n"
            f"Confidence-Based Learning:\n"
            f"Rate each word honestly for better results!\n\n"
            f"Keyboard Shortcuts:\n"
            f"1 or A - Again (complete failure)\n"
            f"2 or H - Hard (difficult recall)\n"
            f"3 or G - Good (recalled with effort)\n"
            f"4 or E - Easy (perfect recall)\n\n"
            f"Space - Show Answer\n"
            f"P - Play Audio"
        )
    
    @staticmethod
    def show_statistics(vocabulary_count, progress):
        """Show vocabulary statistics"""
        easy = len(progress.get('easy', []))
        good = len(progress.get('good', []))
        hard = len(progress.get('hard', []))
        again = len(progress.get('again', []))
        studied = easy + good + hard + again
        not_studied = vocabulary_count - studied
        
        # Get highest confidence words
        confidence = progress.get('confidence_scores', {})
        if confidence:
            top_confidence = sorted(confidence.items(), key=lambda x: x[1], reverse=True)[:5]
            confidence_text = "\\n\\nHighest Confidence Words:\\n"
            for word_key, score in top_confidence:
                hebrew = word_key.split('_', 1)[1] if '_' in word_key else word_key
                confidence_text += f"  {hebrew}: {score:.2f}/4.0\\n"
        else:
            confidence_text = ""
        
        messagebox.showinfo(
            "Vocabulary Statistics",
            f"Total Words: {vocabulary_count}\\n\\n"
            f"Confidence Levels:\\n"
            f"  Easy (Mastered): {easy} ({easy/vocabulary_count*100:.1f}%)\\n"
            f"  Good (Confident): {good} ({good/vocabulary_count*100:.1f}%)\\n"
            f"  Hard (Struggling): {hard} ({hard/vocabulary_count*100:.1f}%)\\n"
            f"  Again (Need Review): {again} ({again/vocabulary_count*100:.1f}%)\\n\\n"
            f"Not Studied Yet: {not_studied} ({not_studied/vocabulary_count*100:.1f}%)"
            f"{confidence_text}"
        )
