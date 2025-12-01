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
    
    def _create_rounded_frame(self, parent, bg, radius=15):
        """Create a frame with rounded corners using Canvas - properly handles theme changes"""
        # Store parent reference to get current background dynamically
        container = tk.Frame(parent, bg=bg, highlightthickness=0)
        canvas = tk.Canvas(container, highlightthickness=0, bd=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        def draw_rounded_rect(event=None):
            canvas.delete("all")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Get the actual parent background color dynamically
            try:
                parent_bg = parent.cget('bg')
            except:
                parent_bg = self.root.cget('bg')
            
            # Set canvas background to match parent (to blend corners)
            canvas.config(bg=parent_bg)
            
            # Use the stored background color (updated by theme changes)
            current_bg = container._bg_color
            
            # Create rounded rectangle with the content background
            canvas.create_arc(0, 0, radius*2, radius*2, start=90, extent=90, fill=current_bg, outline=current_bg, tags="shape")
            canvas.create_arc(width-radius*2, 0, width, radius*2, start=0, extent=90, fill=current_bg, outline=current_bg, tags="shape")
            canvas.create_arc(0, height-radius*2, radius*2, height, start=180, extent=90, fill=current_bg, outline=current_bg, tags="shape")
            canvas.create_arc(width-radius*2, height-radius*2, width, height, start=270, extent=90, fill=current_bg, outline=current_bg, tags="shape")
            
            canvas.create_rectangle(radius, 0, width-radius, height, fill=current_bg, outline=current_bg, tags="shape")
            canvas.create_rectangle(0, radius, width, height-radius, fill=current_bg, outline=current_bg, tags="shape")
        
        canvas.bind('<Configure>', draw_rounded_rect)
        container._canvas = canvas
        container._bg_color = bg
        container._radius = radius
        container._parent_ref = parent
        return container
    
    def create_card_frame(self):
        """Create main card frame with rounded corners"""
        # Create rounded container for the main card
        card_container = self._create_rounded_frame(self.root, self.theme['card_bg'], radius=20)
        card_container.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Create inner frame to hold content
        inner_frame = tk.Frame(
            card_container,
            bg=self.theme['card_bg'],
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        inner_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.96, relheight=0.96)
        
        # Store references for theme updates
        inner_frame._parent = card_container
        card_container._inner_frame = inner_frame
        return inner_frame
    
    def create_text_widget(self, parent, height, font, bg, fg):
        """Create a text display widget with rounded corners"""
        # Create rounded container
        rounded_container = self._create_rounded_frame(parent, bg, radius=12)
        rounded_container.pack(fill=tk.X, expand=False, pady=6, padx=12)
        
        # Create text widget inside the rounded container
        text_widget = tk.Text(
            rounded_container,
            height=height,
            font=font,
            bg=bg,
            fg=fg,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            wrap=tk.WORD,
            padx=15,
            pady=4
        )
        # Center the text widget with minimal height (relheight based on height parameter)
        relheight = 0.6 if height == 1 else 0.85
        text_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.96, relheight=relheight)
        
        # Store the container and background color for theme updates
        text_widget._rounded_container = rounded_container
        text_widget._rounded_bg = bg
        return text_widget
    
    def create_label(self, parent, text, font, bg, fg='#666', **kwargs):
        """Create a label that properly handles theme changes"""
        label = tk.Label(
            parent,
            text=text,
            font=font,
            bg=bg,
            fg=fg,
            **kwargs
        )
        label._fg_color = fg  # Store for theme updates
        return label
    
    def create_button(self, parent, text, command, bg, **kwargs):
        """Create a clickable rounded button using Canvas"""
        padx = kwargs.get('padx', 15)
        pady = kwargs.get('pady', 8)
        font_size = kwargs.get('font_size', 11)
        
        # Create canvas for rounded button
        canvas = tk.Canvas(
            parent,
            highlightthickness=0,
            bd=0,
            bg=parent.cget('bg') if hasattr(parent, 'cget') else self.root.cget('bg')
        )
        
        # Store properties
        canvas._bg_color = bg
        canvas._text = text
        canvas._command = command
        canvas._padx = padx
        canvas._pady = pady
        canvas._font_size = font_size
        canvas._state = tk.NORMAL
        canvas._is_canvas_button = True
        
        def draw_button():
            """Draw the rounded button"""
            canvas.delete("all")
            
            # Measure text size
            font = ('Helvetica', font_size, 'bold')
            temp_text = canvas.create_text(0, 0, text=text, font=font)
            bbox = canvas.bbox(temp_text)
            canvas.delete(temp_text)
            
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate canvas size
            width = text_width + padx * 2
            height = text_height + pady * 2
            radius = 8
            
            # Update canvas size
            canvas.config(width=width, height=height)
            
            # Get parent background
            try:
                parent_bg = parent.cget('bg')
            except:
                parent_bg = self.root.cget('bg')
            canvas.config(bg=parent_bg)
            
            # Draw rounded rectangle
            current_bg = canvas._bg_color
            canvas.create_arc(0, 0, radius*2, radius*2, start=90, extent=90, fill=current_bg, outline=current_bg, tags="bg")
            canvas.create_arc(width-radius*2, 0, width, radius*2, start=0, extent=90, fill=current_bg, outline=current_bg, tags="bg")
            canvas.create_arc(0, height-radius*2, radius*2, height, start=180, extent=90, fill=current_bg, outline=current_bg, tags="bg")
            canvas.create_arc(width-radius*2, height-radius*2, width, height, start=270, extent=90, fill=current_bg, outline=current_bg, tags="bg")
            canvas.create_rectangle(radius, 0, width-radius, height, fill=current_bg, outline=current_bg, tags="bg")
            canvas.create_rectangle(0, radius, width, height-radius, fill=current_bg, outline=current_bg, tags="bg")
            
            # Draw text
            text_color = 'white' if canvas._state == tk.NORMAL else '#aaa'
            canvas.create_text(
                width/2, height/2,
                text=text,
                font=font,
                fill=text_color,
                tags="text"
            )
        
        def on_click(event):
            """Handle button click"""
            if canvas._state == tk.NORMAL and canvas._command:
                canvas._command()
        
        def on_enter(event):
            """Handle mouse enter (hover effect)"""
            if canvas._state == tk.NORMAL:
                canvas.config(cursor='hand2')
        
        def on_leave(event):
            """Handle mouse leave"""
            canvas.config(cursor='')
        
        # Bind events
        canvas.bind('<Button-1>', on_click)
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        
        # Initial draw
        canvas.after(10, draw_button)
        canvas._draw_button = draw_button
        
        return canvas
    
    def update_text(self, text_widget, content):
        """Update text widget content"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete('1.0', tk.END)
        text_widget.insert('1.0', content)
        text_widget.config(state=tk.DISABLED)
    
    def apply_theme(self, widgets, theme):
        """Apply theme to widgets"""
        self.root.config(bg=theme['bg'])
        
        # Update frames
        for frame_name in ['top_bar', 'title_frame', 'theme_frame', 'button_frame', 'response_frame']:
            if frame_name in widgets:
                widgets[frame_name].config(bg=theme['bg'])
        
        # Update labels
        label_mappings = [
            ('title_label', theme.get('text_fg', '#000000')),
            ('progress_label', '#888888' if theme['bg'] == '#1a1a1a' else '#666'),
            ('stats_label', '#888888' if theme['bg'] == '#1a1a1a' else '#666'),
            ('keyboard_hint', '#888888' if theme['bg'] == '#1a1a1a' else '#666666')
        ]
        
        for label_name, fg_color in label_mappings:
            if label_name in widgets:
                widgets[label_name].config(bg=theme['bg'], fg=fg_color)
        
        # Update card frame
        if 'card_frame' in widgets:
            card_frame = widgets['card_frame']
            card_frame.config(bg=theme['card_bg'])
            # Update the canvas background for rounded corners
            if hasattr(card_frame, '_parent') and hasattr(card_frame._parent, '_canvas'):
                container = card_frame._parent
                # Update stored color
                container._bg_color = theme['card_bg']
                container.config(bg=theme['card_bg'])
                
                # Trigger redraw using the stored draw function
                canvas = container._canvas
                canvas.event_generate('<Configure>')
        
        # Update text widgets and their rounded containers
        text_widget_mappings = [
            ('hebrew_text', 'text_bg', 'text_fg'),
            ('trans_text', 'trans_bg', 'trans_fg'),
            ('english_text', 'english_bg', 'english_fg')
        ]
        
        for widget_name, bg_key, fg_key in text_widget_mappings:
            if widget_name in widgets:
                text_widget = widgets[widget_name]
                new_bg = theme[bg_key]
                new_fg = theme[fg_key]
                
                # Update text widget
                text_widget.config(bg=new_bg, fg=new_fg)
                
                # Update rounded container canvas background
                if hasattr(text_widget, '_rounded_container'):
                    container = text_widget._rounded_container
                    # Update stored color
                    container._bg_color = new_bg
                    container.config(bg=new_bg)
                    
                    # Trigger redraw using the stored draw function
                    if hasattr(container, '_canvas'):
                        canvas = container._canvas
                        # Manually trigger the configure event to redraw
                        canvas.event_generate('<Configure>')
        
        # Update buttons (now they are containers with canvas backgrounds)
        button_mappings = [
            ('audio_btn', 'btn_audio'),
            ('show_answer_btn', 'btn_answer'),
            ('again_btn', 'btn_again'),
            ('hard_btn', 'btn_hard'),
            ('good_btn', 'btn_good'),
            ('easy_btn', 'btn_easy'),
            ('theme_toggle_btn', 'btn_audio')  # Use same gray color
        ]
        
        for widget_name, theme_key in button_mappings:
            if widget_name in widgets:
                button = widgets[widget_name]
                new_bg = theme[theme_key]
                
                # Canvas button (rounded)
                if hasattr(button, '_is_canvas_button'):
                    button._bg_color = new_bg
                    # Redraw with new colors
                    if hasattr(button, '_draw_button'):
                        button._draw_button()
                # Simple button
                elif hasattr(button, '_is_container') and not button._is_container:
                    button.config(bg=new_bg)
                    button._bg_color = new_bg
                # Fallback
                else:
                    try:
                        button.config(bg=new_bg)
                    except:
                        pass

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
