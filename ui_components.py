"""
UI Components
Builds and manages the graphical interface
All UI configuration, themes, layout, fonts, colors, and widget creation in one place
"""

import tkinter as tk
from tkinter import messagebox


# ============================================================================
#                           UI CONFIGURATION SECTION
#              ALL VISUAL SETTINGS ARE HERE FOR EASY CUSTOMIZATION
# ============================================================================

class UIConfig:
    """All UI layout parameters - modify these to adjust the interface"""
    
    # ===== LAYOUT SPACING =====
    WINDOW_TOP_PADDING = 15          # Space at top of window
    WINDOW_SIDE_PADDING = 40         # Space on sides of window
    CARD_FRAME_PADY = 15             # Vertical padding around main card
    CARD_FRAME_PADX = 40             # Horizontal padding around main card
    
    # ===== DIALOGS =====
    CUSTOM_RANGE_DIALOG_GEOMETRY = "300x150"  # Custom range dialog size
    
    # ===== TEXT BOXES =====
    TEXT_BOX_VERTICAL_SPACING = 3    # Space between text boxes (pady)
    TEXT_BOX_HORIZONTAL_PADDING = 12 # Side padding for text boxes (padx)
    TEXT_BOX_BORDER_RADIUS = 12      # Corner roundness of text boxes
    TEXT_BOX_INNER_PADX = 10         # Text padding inside box (horizontal)
    TEXT_BOX_INNER_PADY = 5          # Text padding inside box (vertical)
    TEXT_BOX_HEIGHT = 1              # Line height for text boxes
    TEXT_BOX_CONTAINER_HEIGHT_SINGLE = 60  # Fixed height for single-line boxes (Hebrew)
    TEXT_BOX_CONTAINER_HEIGHT_MULTI = 85   # Fixed height for multi-line boxes
    TEXT_BOX_INNER_REL_WIDTH = 0.96  # Relative width of text inside container
    TEXT_BOX_INNER_REL_HEIGHT = 0.85 # Relative height of text inside container
    INFO_BOX_HEIGHT = 100            # Fixed height for info box
    INFO_BOX_PADDING = 5             # Padding inside info box
    INFO_BOX_LABEL_PADY = 2          # Vertical padding for info labels
    INFO_BOX_WRAP_LENGTH = 600       # Text wrap length for info labels
    
    # ===== FONTS =====
    # Hebrew text
    HEBREW_FONT_FAMILY = 'Arial Hebrew'
    HEBREW_FONT_SIZE = 36
    HEBREW_FONT_WEIGHT = 'bold'
    
    # Transliteration text
    TRANS_FONT_FAMILY = 'Helvetica'
    TRANS_FONT_SIZE = 18
    TRANS_FONT_WEIGHT = 'normal'
    
    # English text
    ENGLISH_FONT_FAMILY = 'Helvetica'
    ENGLISH_FONT_SIZE = 20
    ENGLISH_FONT_WEIGHT = 'bold'
    
    # Title
    TITLE_FONT_FAMILY = 'Helvetica'
    TITLE_FONT_SIZE = 24
    TITLE_FONT_WEIGHT = 'bold'
    
    # Progress/Stats labels
    LABEL_FONT_FAMILY = 'Helvetica'
    LABEL_FONT_SIZE = 11
    LABEL_FONT_WEIGHT = 'normal'
    
    # Keyboard hint
    HINT_FONT_FAMILY = 'Helvetica'
    HINT_FONT_SIZE = 9
    HINT_FONT_WEIGHT = 'italic'
    
    # ===== BUTTONS =====
    CARD_BORDER_RADIUS = 20          # Corner roundness of main card
    BUTTON_BORDER_RADIUS = 8         # Corner roundness of buttons
    
    # Main buttons (Audio, Show Answer)
    MAIN_BUTTON_PADX = 18
    MAIN_BUTTON_PADY = 8
    MAIN_BUTTON_FONT_SIZE = 11
    MAIN_BUTTON_SPACING = 6          # Space between buttons (grid padx)
    MAIN_BUTTON_ROW_SPACING = 5      # Vertical space (grid pady)
    
    # Response buttons (Again, Hard, Good, Easy)
    RESPONSE_BUTTON_PADX = 14
    RESPONSE_BUTTON_PADY = 7
    RESPONSE_BUTTON_FONT_SIZE = 10
    RESPONSE_BUTTON_SPACING = 3      # Space between buttons (grid padx)
    RESPONSE_BUTTON_ROW_SPACING = 5  # Vertical space (grid pady)
    
    # Theme toggle button
    THEME_BUTTON_PADX = 12
    THEME_BUTTON_PADY = 8
    THEME_BUTTON_FONT_SIZE = 18
    
    # ===== BUTTON FRAME SPACING =====
    BUTTON_FRAME_PADY = 10           # Space above/below button frames
    RESPONSE_FRAME_PADY = 10         # Space above/below response frame
    KEYBOARD_HINT_TOP_PADDING = 10   # Space above keyboard hint
    
    # ===== TITLE SECTION =====
    TITLE_BOTTOM_PADDING = 10        # Space below stats label
    
    @staticmethod
    def get_hebrew_font():
        """Get Hebrew text font tuple"""
        return (UIConfig.HEBREW_FONT_FAMILY, UIConfig.HEBREW_FONT_SIZE, UIConfig.HEBREW_FONT_WEIGHT)
    
    @staticmethod
    def get_trans_font():
        """Get transliteration text font tuple"""
        return (UIConfig.TRANS_FONT_FAMILY, UIConfig.TRANS_FONT_SIZE, UIConfig.TRANS_FONT_WEIGHT)
    
    @staticmethod
    def get_english_font():
        """Get English text font tuple"""
        return (UIConfig.ENGLISH_FONT_FAMILY, UIConfig.ENGLISH_FONT_SIZE, UIConfig.ENGLISH_FONT_WEIGHT)
    
    @staticmethod
    def get_title_font():
        """Get title font tuple"""
        return (UIConfig.TITLE_FONT_FAMILY, UIConfig.TITLE_FONT_SIZE, UIConfig.TITLE_FONT_WEIGHT)
    
    @staticmethod
    def get_label_font():
        """Get label font tuple"""
        return (UIConfig.LABEL_FONT_FAMILY, UIConfig.LABEL_FONT_SIZE, UIConfig.LABEL_FONT_WEIGHT)
    
    @staticmethod
    def get_hint_font():
        """Get hint font tuple"""
        return (UIConfig.HINT_FONT_FAMILY, UIConfig.HINT_FONT_SIZE, UIConfig.HINT_FONT_WEIGHT)


class Themes:
    """UI theme color definitions - modify these to change app colors"""
    
    LIGHT = {
        'bg': '#f0f0f0',
        'card_bg': '#ffffff',
        'text_bg': '#f8f9fa',
        'text_fg': '#2c3e50',
        'trans_bg': '#e3f2fd',
        'trans_fg': '#1565c0',
        'english_bg': '#e8f5e9',
        'english_fg': '#2e7d32',
        'info_bg': '#f8f9fa',
        'info_fg': '#495057',
        'label_fg': '#666666',
        'hint_fg': '#666666',
        'btn_audio': '#607d8b',
        'btn_answer': '#78909c',
        'btn_again': '#e57373',
        'btn_hard': '#ffb74d',
        'btn_good': '#aed581',
        'btn_easy': '#81c784'
    }
    
    DARK = {
        'bg': '#1e1e1e',
        'card_bg': '#2d2d2d',
        'text_bg': '#3a3a3a',
        'text_fg': '#e0e0e0',
        'trans_bg': '#263238',
        'trans_fg': '#81d4fa',
        'english_bg': '#1b5e20',
        'english_fg': '#a5d6a7',
        'info_bg': '#3a3a3a',
        'info_fg': '#e0e0e0',
        'label_fg': '#888888',
        'hint_fg': '#888888',
        'btn_audio': '#546e7a',
        'btn_answer': '#5f7780',
        'btn_again': '#c62828',
        'btn_hard': '#e65100',
        'btn_good': '#558b2f',
        'btn_easy': '#2e7d32'
    }
    
    @staticmethod
    def get_theme(dark_mode=False):
        """Get theme colors based on mode"""
        return Themes.DARK if dark_mode else Themes.LIGHT


# ============================================================================
#                           UI BUILDER CLASSES
# ============================================================================

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
        card_container = self._create_rounded_frame(
            self.root, 
            self.theme['card_bg'], 
            radius=UIConfig.CARD_BORDER_RADIUS
        )
        card_container.pack(
            pady=UIConfig.CARD_FRAME_PADY, 
            padx=UIConfig.CARD_FRAME_PADX, 
            fill=tk.BOTH, 
            expand=True
        )
        
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
        container_height = UIConfig.TEXT_BOX_CONTAINER_HEIGHT_SINGLE if height == 1 else UIConfig.TEXT_BOX_CONTAINER_HEIGHT_MULTI
        
        rounded_container = self._create_rounded_frame(parent, bg, radius=UIConfig.TEXT_BOX_BORDER_RADIUS)
        rounded_container.pack(
            fill=tk.X, 
            expand=False, 
            pady=UIConfig.TEXT_BOX_VERTICAL_SPACING, 
            padx=UIConfig.TEXT_BOX_HORIZONTAL_PADDING
        )
        rounded_container.config(height=container_height)
        rounded_container.pack_propagate(False)
        
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
            padx=UIConfig.TEXT_BOX_INNER_PADX,
            pady=UIConfig.TEXT_BOX_INNER_PADY
        )
        text_widget.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER,
            relwidth=UIConfig.TEXT_BOX_INNER_REL_WIDTH,
            relheight=UIConfig.TEXT_BOX_INNER_REL_HEIGHT
        )
        
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
            radius = UIConfig.BUTTON_BORDER_RADIUS
            
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
    
    def build_complete_interface(self, callbacks):
        """
        Build the complete user interface with all widgets
        
        Args:
            callbacks: Dictionary with callback functions:
                - 'toggle_theme': Function to toggle dark/light mode
                - 'play_audio': Function to play audio
                - 'show_answer': Function to show answer
                - 'mark_again': Function to mark word as 'again'
                - 'mark_hard': Function to mark word as 'hard'
                - 'mark_good': Function to mark word as 'good'
                - 'mark_easy': Function to mark word as 'easy'
        
        Returns:
            Dictionary containing all created widgets with keys:
            - Frames: 'top_bar', 'title_frame', 'theme_frame', 'card_frame', 
                     'button_frame', 'response_frame'
            - Labels: 'title_label', 'progress_label', 'stats_label', 'keyboard_hint'
            - Text widgets: 'hebrew_text', 'trans_text', 'english_text'
            - Buttons: 'theme_toggle_btn', 'audio_btn', 'show_answer_btn',
                      'again_btn', 'hard_btn', 'good_btn', 'easy_btn'
        """
        widgets = {}
        
        # ===== TOP BAR WITH TITLE AND THEME TOGGLE =====
        top_bar = tk.Frame(self.root, bg=self.theme['bg'])
        top_bar.pack(
            pady=UIConfig.WINDOW_TOP_PADDING, 
            fill=tk.X, 
            padx=UIConfig.WINDOW_SIDE_PADDING
        )
        widgets['top_bar'] = top_bar
        
        # Title frame (left side)
        title_frame = tk.Frame(top_bar, bg=self.theme['bg'])
        title_frame.pack(side=tk.LEFT)
        widgets['title_frame'] = title_frame
        
        # Main title
        widgets['title_label'] = self.create_label(
            title_frame,
            text="Hebrew Learning App",
            font=UIConfig.get_title_font(),
            bg=self.theme['bg'],
            fg=self.theme['text_fg']
        )
        widgets['title_label'].pack()
        
        # Progress label
        widgets['progress_label'] = self.create_label(
            title_frame,
            text="",
            font=UIConfig.get_label_font(),
            bg=self.theme['bg'],
            fg=self.theme['label_fg']
        )
        widgets['progress_label'].pack()
        
        # Stats label
        widgets['stats_label'] = self.create_label(
            title_frame,
            text="",
            font=UIConfig.get_label_font(),
            bg=self.theme['bg'],
            fg=self.theme['label_fg']
        )
        widgets['stats_label'].pack(pady=UIConfig.TITLE_BOTTOM_PADDING)
        
        # Theme toggle button (right side)
        theme_frame = tk.Frame(top_bar, bg=self.theme['bg'])
        theme_frame.pack(side=tk.RIGHT)
        widgets['theme_frame'] = theme_frame
        
        widgets['theme_toggle_btn'] = self.create_button(
            theme_frame,
            "🌙",  # Will be updated based on dark_mode
            callbacks['toggle_theme'],
            self.theme['btn_audio'],
            font_size=UIConfig.THEME_BUTTON_FONT_SIZE,
            padx=UIConfig.THEME_BUTTON_PADX,
            pady=UIConfig.THEME_BUTTON_PADY
        )
        widgets['theme_toggle_btn'].pack()
        
        # ===== MAIN CARD FRAME =====
        widgets['card_frame'] = self.create_card_frame()
        
        # ===== TEXT DISPLAY WIDGETS =====
        # Hebrew text
        widgets['hebrew_text'] = self.create_text_widget(
            widgets['card_frame'],
            UIConfig.TEXT_BOX_HEIGHT,
            UIConfig.get_hebrew_font(),
            self.theme['text_bg'],
            self.theme['text_fg']
        )
        
        # Transliteration text
        widgets['trans_text'] = self.create_text_widget(
            widgets['card_frame'],
            UIConfig.TEXT_BOX_HEIGHT,
            UIConfig.get_trans_font(),
            self.theme['trans_bg'],
            self.theme['trans_fg']
        )
        
        # English text
        widgets['english_text'] = self.create_text_widget(
            widgets['card_frame'],
            UIConfig.TEXT_BOX_HEIGHT,
            UIConfig.get_english_font(),
            self.theme['english_bg'],
            self.theme['english_fg']
        )
        
        # ===== EXTRA INFO BOX (ROOT, NOTES, VARIANTS, TRANSLATIONS) =====
        info_container = self._create_rounded_frame(
            widgets['card_frame'],
            self.theme['info_bg'],
            radius=UIConfig.TEXT_BOX_BORDER_RADIUS
        )
        info_container.pack(
            fill=tk.BOTH,
            expand=False,
            pady=UIConfig.TEXT_BOX_VERTICAL_SPACING,
            padx=UIConfig.TEXT_BOX_HORIZONTAL_PADDING
        )
        info_container.config(height=UIConfig.INFO_BOX_HEIGHT)
        info_container.pack_propagate(False)
        
        info_inner = tk.Frame(info_container, bg=self.theme['info_bg'])
        info_inner.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER,
            relwidth=UIConfig.TEXT_BOX_INNER_REL_WIDTH,
            relheight=UIConfig.TEXT_BOX_INNER_REL_HEIGHT
        )
        
        # Create info labels with consistent configuration
        info_labels = [
            ('root_text', 'normal'),
            ('notes_text', 'italic'),
            ('variants_text', 'normal'),
            ('translations_text', 'normal')
        ]
        
        for label_name, weight in info_labels:
            widgets[label_name] = self.create_label(
                info_inner,
                text="",
                font=(UIConfig.TRANS_FONT_FAMILY, 12, weight),
                bg=self.theme['info_bg'],
                fg=self.theme['info_fg'],
                anchor='w',
                justify=tk.LEFT,
                wraplength=UIConfig.INFO_BOX_WRAP_LENGTH
            )
            widgets[label_name].pack(
                fill=tk.X,
                padx=UIConfig.INFO_BOX_PADDING,
                pady=UIConfig.INFO_BOX_LABEL_PADY,
                anchor='w'
            )
        
        # Store info container for theme updates
        widgets['info_container'] = info_container
        widgets['info_inner'] = info_inner
        
        # ===== CONTROL BUTTONS (AUDIO & SHOW ANSWER) =====
        button_frame = tk.Frame(self.root, bg=self.theme['bg'])
        button_frame.pack(pady=UIConfig.BUTTON_FRAME_PADY)
        widgets['button_frame'] = button_frame
        
        widgets['audio_btn'] = self.create_button(
            button_frame,
            "🔊 Play Audio",
            callbacks['play_audio'],
            self.theme['btn_audio'],
            padx=UIConfig.MAIN_BUTTON_PADX,
            pady=UIConfig.MAIN_BUTTON_PADY,
            font_size=UIConfig.MAIN_BUTTON_FONT_SIZE
        )
        widgets['audio_btn'].grid(
            row=0, column=0,
            padx=UIConfig.MAIN_BUTTON_SPACING,
            pady=UIConfig.MAIN_BUTTON_ROW_SPACING
        )
        
        widgets['show_answer_btn'] = self.create_button(
            button_frame,
            "👁 Show Answer",
            callbacks['show_answer'],
            self.theme['btn_answer'],
            padx=UIConfig.MAIN_BUTTON_PADX,
            pady=UIConfig.MAIN_BUTTON_PADY,
            font_size=UIConfig.MAIN_BUTTON_FONT_SIZE
        )
        widgets['show_answer_btn'].grid(
            row=0, column=1,
            padx=UIConfig.MAIN_BUTTON_SPACING,
            pady=UIConfig.MAIN_BUTTON_ROW_SPACING
        )
        
        # ===== RESPONSE BUTTONS (AGAIN, HARD, GOOD, EASY) =====
        response_frame = tk.Frame(self.root, bg=self.theme['bg'])
        response_frame.pack(pady=UIConfig.RESPONSE_FRAME_PADY)
        widgets['response_frame'] = response_frame
        
        widgets['again_btn'] = self.create_button(
            response_frame,
            "Again (1)",
            callbacks['mark_again'],
            self.theme['btn_again'],
            font_size=UIConfig.RESPONSE_BUTTON_FONT_SIZE,
            padx=UIConfig.RESPONSE_BUTTON_PADX,
            pady=UIConfig.RESPONSE_BUTTON_PADY
        )
        widgets['again_btn'].grid(
            row=0, column=0,
            padx=UIConfig.RESPONSE_BUTTON_SPACING,
            pady=UIConfig.RESPONSE_BUTTON_ROW_SPACING
        )
        
        widgets['hard_btn'] = self.create_button(
            response_frame,
            "Hard (2)",
            callbacks['mark_hard'],
            self.theme['btn_hard'],
            font_size=UIConfig.RESPONSE_BUTTON_FONT_SIZE,
            padx=UIConfig.RESPONSE_BUTTON_PADX,
            pady=UIConfig.RESPONSE_BUTTON_PADY
        )
        widgets['hard_btn'].grid(
            row=0, column=1,
            padx=UIConfig.RESPONSE_BUTTON_SPACING,
            pady=UIConfig.RESPONSE_BUTTON_ROW_SPACING
        )
        
        widgets['good_btn'] = self.create_button(
            response_frame,
            "Good (3)",
            callbacks['mark_good'],
            self.theme['btn_good'],
            font_size=UIConfig.RESPONSE_BUTTON_FONT_SIZE,
            padx=UIConfig.RESPONSE_BUTTON_PADX,
            pady=UIConfig.RESPONSE_BUTTON_PADY
        )
        widgets['good_btn'].grid(
            row=0, column=2,
            padx=UIConfig.RESPONSE_BUTTON_SPACING,
            pady=UIConfig.RESPONSE_BUTTON_ROW_SPACING
        )
        
        widgets['easy_btn'] = self.create_button(
            response_frame,
            "Easy (4)",
            callbacks['mark_easy'],
            self.theme['btn_easy'],
            font_size=UIConfig.RESPONSE_BUTTON_FONT_SIZE,
            padx=UIConfig.RESPONSE_BUTTON_PADX,
            pady=UIConfig.RESPONSE_BUTTON_PADY
        )
        widgets['easy_btn'].grid(
            row=0, column=3,
            padx=UIConfig.RESPONSE_BUTTON_SPACING,
            pady=UIConfig.RESPONSE_BUTTON_ROW_SPACING
        )
        
        # ===== KEYBOARD SHORTCUTS HINT =====
        widgets['keyboard_hint'] = self.create_label(
            response_frame,
            text="Keyboard: 1=Again  2=Hard  3=Good  4=Easy  |  Space=Show  P=Audio",
            font=UIConfig.get_hint_font(),
            bg=self.theme['bg'],
            fg=self.theme['hint_fg']
        )
        widgets['keyboard_hint'].grid(
            row=1, column=0, columnspan=4,
            pady=(UIConfig.KEYBOARD_HINT_TOP_PADDING, 0)
        )
        
        return widgets
    
    def apply_theme(self, widgets, theme):
        """Apply theme to widgets"""
        self.root.config(bg=theme['bg'])
        
        # Update frames
        for frame_name in ['top_bar', 'title_frame', 'theme_frame', 'button_frame', 'response_frame']:
            if frame_name in widgets:
                widgets[frame_name].config(bg=theme['bg'])
        
        # Update labels
        label_mappings = [
            ('title_label', theme['text_fg']),
            ('progress_label', theme['label_fg']),
            ('stats_label', theme['label_fg']),
            ('keyboard_hint', theme['hint_fg'])
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
        
        # Update info box (fourth box with root, notes, variants, translations)
        if 'info_container' in widgets and 'info_inner' in widgets:
            # Update container
            info_container = widgets['info_container']
            info_container._bg_color = theme['info_bg']
            info_container.config(bg=theme['info_bg'])
            if hasattr(info_container, '_canvas'):
                info_container._canvas.event_generate('<Configure>')
            
            # Update inner frame
            widgets['info_inner'].config(bg=theme['info_bg'])
            
            # Update all info labels
            for label_name in ['root_text', 'notes_text', 'variants_text', 'translations_text']:
                if label_name in widgets:
                    widgets[label_name].config(bg=theme['info_bg'], fg=theme['info_fg'])
        
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
        dialog.geometry(UIConfig.CUSTOM_RANGE_DIALOG_GEOMETRY)
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
        # Handle new database format (integers) or old format (lists)
        if isinstance(progress.get('easy'), int):
            easy = progress.get('easy', 0)
            good = progress.get('good', 0)
            hard = progress.get('hard', 0)
            again = progress.get('again', 0)
            not_studied = progress.get('not_studied', 0)
        else:
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
