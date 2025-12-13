"""
UI Components
Builds and manages the graphical interface using Flet
All UI configuration, themes, layout, fonts, colors, and widget creation in one place
"""

import flet as ft

# ============================================================================
#                           UI CONFIGURATION SECTION
#              ALL VISUAL SETTINGS ARE HERE FOR EASY CUSTOMIZATION
# ============================================================================

class UIConfig:
    """All UI layout parameters - modify these to adjust the interface"""
    
    # ===== LAYOUT SPACING =====
    WINDOW_PADDING = 20
    CARD_PADDING = 20
    
    # ===== TEXT BOXES =====
    TEXT_BOX_BORDER_RADIUS = 12
    TEXT_BOX_PADDING = 10
    
    # ===== FONTS =====
    # Hebrew text
    HEBREW_FONT_FAMILY = 'Arial Hebrew'
    HEBREW_FONT_SIZE = 36
    HEBREW_FONT_WEIGHT = ft.FontWeight.BOLD
    
    # Transliteration text
    TRANS_FONT_FAMILY = 'Helvetica'
    TRANS_FONT_SIZE = 18
    TRANS_FONT_WEIGHT = ft.FontWeight.NORMAL
    
    # English text
    ENGLISH_FONT_FAMILY = 'Helvetica'
    ENGLISH_FONT_SIZE = 20
    ENGLISH_FONT_WEIGHT = ft.FontWeight.BOLD
    
    # Title
    TITLE_FONT_FAMILY = 'Helvetica'
    TITLE_FONT_SIZE = 24
    TITLE_FONT_WEIGHT = ft.FontWeight.BOLD
    
    # Progress/Stats labels
    LABEL_FONT_FAMILY = 'Helvetica'
    LABEL_FONT_SIZE = 12
    LABEL_FONT_WEIGHT = ft.FontWeight.NORMAL
    
    # Keyboard hint
    HINT_FONT_FAMILY = 'Helvetica'
    HINT_FONT_SIZE = 10
    HINT_FONT_WEIGHT = ft.FontWeight.W_300 # Italic not directly supported in weight, handled in style
    
    # ===== BUTTONS =====
    CARD_BORDER_RADIUS = 20
    BUTTON_BORDER_RADIUS = 8
    
    # Navigation bar
    NAV_BUTTON_FONT_SIZE = 14


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
        'nav_bg': '#e0e0e0',
        'nav_btn_bg': '#d0d0d0',
        'nav_btn_fg': '#333333',
        'nav_btn_hover': '#c0c0c0',
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
        'nav_bg': '#2a2a2a',
        'nav_btn_bg': '#3a3a3a',
        'nav_btn_fg': '#e0e0e0',
        'nav_btn_hover': '#4a4a4a',
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
    
    def __init__(self, page: ft.Page, theme):
        self.page = page
        self.theme = theme
        self.widgets = {}
    
    def create_text_widget(self, font_family, font_size, font_weight, bg, fg, height=None):
        """Create a text display widget with rounded corners"""
        text = ft.Text(
            value="",
            font_family=font_family,
            size=font_size,
            weight=font_weight,
            color=fg,
            text_align=ft.TextAlign.CENTER,
            selectable=True
        )
        
        container = ft.Container(
            content=text,
            bgcolor=bg,
            border_radius=UIConfig.TEXT_BOX_BORDER_RADIUS,
            padding=UIConfig.TEXT_BOX_PADDING,
            alignment=ft.alignment.center,
            width=float('inf') # Expand horizontally
        )
        
        if height:
            container.height = height
            
        return container, text
    
    def create_button(self, text, on_click, bg, fg='white', width=None):
        """Create a rounded button"""
        return ft.ElevatedButton(
            text=text,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=fg,
                bgcolor=bg,
                shape=ft.RoundedRectangleBorder(radius=UIConfig.BUTTON_BORDER_RADIUS),
            ),
            width=width
        )

    def build_complete_interface(self, callbacks, menu_callbacks=None, checkbox_vars=None):
        """
        Build the complete user interface with all widgets
        """
        widgets = {}
        
        # ===== NAVIGATION BAR =====
        if menu_callbacks:
            
            def create_menu_item(label, command):
                return ft.PopupMenuItem(text=label, on_click=lambda _: command())

            def create_submenu_item(label, submenu_items, indent_level=0):
                items = []
                # Add header for the submenu
                prefix = "  " * indent_level
                items.append(ft.PopupMenuItem(text=f"{prefix}--- {label} ---", disabled=True))
                
                for item in submenu_items:
                    if item.get('separator'):
                        items.append(ft.PopupMenuItem(height=6, content=ft.Divider(thickness=1), disabled=True))
                    elif 'submenu' in item:
                        items.extend(create_submenu_item(item['label'], item['submenu'], indent_level + 1))
                    elif 'variable' in item:
                         item_text = f"{'  ' * (indent_level + 1)}{item['label']}"
                         items.append(ft.PopupMenuItem(text=item_text, on_click=lambda _, cmd=item.get('command'): cmd() if cmd else None))
                    else:
                        item_text = f"{'  ' * (indent_level + 1)}{item['label']}"
                        items.append(ft.PopupMenuItem(text=item_text, on_click=lambda _, cmd=item.get('command'): cmd() if cmd else None))
                return items

            def build_menu_items(items_config):
                items = []
                for item in items_config:
                    if item.get('separator'):
                        items.append(ft.PopupMenuItem(height=6, content=ft.Divider(thickness=1), disabled=True))
                    elif 'submenu' in item:
                        items.extend(create_submenu_item(item['label'], item['submenu']))
                    elif 'variable' in item:
                        items.append(ft.PopupMenuItem(text=item['label'], on_click=lambda _, cmd=item.get('command'): cmd() if cmd else None))
                    else:
                        items.append(ft.PopupMenuItem(text=item['label'], on_click=lambda _, cmd=item.get('command'): cmd() if cmd else None))
                return items

            # Study Menu
            study_items_config = [
                {'label': 'Quick Start', 'submenu': [
                    {'label': 'Top 50 Words', 'command': menu_callbacks.get('start_50')},
                    {'label': 'Top 100 Words', 'command': menu_callbacks.get('start_100')},
                    {'label': 'Top 200 Words', 'command': menu_callbacks.get('start_200')},
                    {'label': 'All Words', 'command': menu_callbacks.get('start_all')},
                    {'separator': True},
                    {'label': 'Custom Range...', 'command': menu_callbacks.get('custom_range')},
                ]},
                {'separator': True},
                {'label': 'Smart Study', 'submenu': [
                    {'label': 'SRS Review (Due Today)', 'command': menu_callbacks.get('srs_review')},
                    {'label': 'Learn New Words', 'command': menu_callbacks.get('new_words')},
                    {'label': 'Review Weakest Words', 'command': menu_callbacks.get('weak_words')},
                    {'label': 'Review Strongest Words', 'command': menu_callbacks.get('strong_words')},
                    {'separator': True},
                    {'label': 'Practice Difficult (Top 50)', 'command': menu_callbacks.get('difficult_50')},
                    {'label': 'Practice Difficult (Top 100)', 'command': menu_callbacks.get('difficult_100')},
                ]},
                {'separator': True},
                {'label': 'By Category', 'submenu': [
                    {'label': 'Greetings', 'command': menu_callbacks.get('cat_greetings')},
                    {'label': 'Common Words', 'command': menu_callbacks.get('cat_common')},
                    {'label': 'Verbs', 'command': menu_callbacks.get('cat_verbs')},
                    {'label': 'Nouns', 'command': menu_callbacks.get('cat_nouns')},
                    {'label': 'Adjectives', 'command': menu_callbacks.get('cat_adjectives')},
                    {'separator': True},
                    {'label': 'Biblical Hebrew', 'command': menu_callbacks.get('cat_biblical')},
                    {'label': 'Torah', 'command': menu_callbacks.get('cat_torah')},
                    {'separator': True},
                    {'label': 'Prepositions', 'command': menu_callbacks.get('cat_prepositions')},
                    {'label': 'Basic Vocabulary', 'command': menu_callbacks.get('cat_basic')},
                ]},
                {'separator': True},
                {'label': 'By Type', 'submenu': [
                    {'label': 'Modern Hebrew', 'command': menu_callbacks.get('type_modern')},
                    {'label': 'Biblical Hebrew', 'command': menu_callbacks.get('type_biblical')},
                    {'label': 'Both Modern & Biblical', 'command': menu_callbacks.get('type_both')},
                    {'separator': True},
                    {'label': 'Verbs Only', 'command': menu_callbacks.get('pos_verb')},
                    {'label': 'Nouns Only', 'command': menu_callbacks.get('pos_noun')},
                    {'label': 'Adjectives Only', 'command': menu_callbacks.get('pos_adjective')},
                    {'label': 'Prepositions Only', 'command': menu_callbacks.get('pos_preposition')},
                ]},
                {'separator': True},
                {'label': 'Random 10 Words', 'command': menu_callbacks.get('random_10')},
            ]
            
            widgets['nav_study'] = ft.PopupMenuButton(
                content=ft.Text("Study ▼", color=self.theme['nav_btn_fg']),
                items=build_menu_items(study_items_config),
            )

            # Settings Menu
            settings_items_config = [
                {'label': 'Show Variants', 'variable': True, 'command': menu_callbacks.get('toggle_variants')},
                {'label': 'Show Translations', 'variable': True, 'command': menu_callbacks.get('toggle_translations')},
                {'separator': True},
                {'label': 'Auto-play Audio', 'variable': True, 'command': menu_callbacks.get('toggle_auto_play')},
                {'separator': True},
                {'label': 'Toggle Dark Mode', 'command': callbacks['toggle_theme']},
                {'separator': True},
                {'label': 'Reset Progress', 'command': menu_callbacks.get('reset_progress')},
            ]
            widgets['nav_settings'] = ft.PopupMenuButton(
                content=ft.Text("Settings ▼", color=self.theme['nav_btn_fg']),
                items=build_menu_items(settings_items_config),
            )

            # Vocabulary Menu
            vocab_items_config = [
                {'label': 'View Statistics', 'command': menu_callbacks.get('show_statistics')},
            ]
            widgets['nav_vocabulary'] = ft.PopupMenuButton(
                content=ft.Text("Vocabulary ▼", color=self.theme['nav_btn_fg']),
                items=build_menu_items(vocab_items_config),
            )

            # Help Menu
            help_items_config = [
                {'label': 'About', 'command': menu_callbacks.get('show_about')},
            ]
            widgets['nav_help'] = ft.PopupMenuButton(
                content=ft.Text("Help ▼", color=self.theme['nav_btn_fg']),
                items=build_menu_items(help_items_config),
            )

            widgets['nav_bar'] = ft.Container(
                content=ft.Row(
                    controls=[
                        widgets['nav_study'],
                        widgets['nav_settings'],
                        widgets['nav_vocabulary'],
                        widgets['nav_help']
                    ],
                    spacing=10
                ),
                bgcolor=self.theme['nav_bg'],
                padding=10,
            )

        # ===== TOP BAR =====
        widgets['title_label'] = ft.Text(
            value="Hebrew Learning App",
            font_family=UIConfig.TITLE_FONT_FAMILY,
            size=UIConfig.TITLE_FONT_SIZE,
            weight=UIConfig.TITLE_FONT_WEIGHT,
            color=self.theme['text_fg']
        )
        
        widgets['progress_label'] = ft.Text(
            value="",
            font_family=UIConfig.LABEL_FONT_FAMILY,
            size=UIConfig.LABEL_FONT_SIZE,
            weight=UIConfig.LABEL_FONT_WEIGHT,
            color=self.theme['label_fg']
        )
        
        widgets['stats_label'] = ft.Text(
            value="",
            font_family=UIConfig.LABEL_FONT_FAMILY,
            size=UIConfig.LABEL_FONT_SIZE,
            weight=UIConfig.LABEL_FONT_WEIGHT,
            color=self.theme['label_fg']
        )
        
        widgets['theme_toggle_btn'] = ft.IconButton(
            icon=ft.Icons.DARK_MODE if self.theme == Themes.LIGHT else ft.Icons.LIGHT_MODE,
            on_click=lambda _: callbacks['toggle_theme'](),
            icon_color=self.theme['text_fg']
        )

        top_bar = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        widgets['title_label'],
                        widgets['progress_label'],
                        widgets['stats_label']
                    ],
                    spacing=5
                ),
                widgets['theme_toggle_btn']
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        widgets['top_bar'] = top_bar

        # ===== TEXT DISPLAY WIDGETS =====
        widgets['hebrew_container'], widgets['hebrew_text'] = self.create_text_widget(
            UIConfig.HEBREW_FONT_FAMILY, UIConfig.HEBREW_FONT_SIZE, UIConfig.HEBREW_FONT_WEIGHT,
            self.theme['text_bg'], self.theme['text_fg'], height=80
        )
        
        widgets['trans_container'], widgets['trans_text'] = self.create_text_widget(
            UIConfig.TRANS_FONT_FAMILY, UIConfig.TRANS_FONT_SIZE, UIConfig.TRANS_FONT_WEIGHT,
            self.theme['trans_bg'], self.theme['trans_fg'], height=60
        )
        
        widgets['english_container'], widgets['english_text'] = self.create_text_widget(
            UIConfig.ENGLISH_FONT_FAMILY, UIConfig.ENGLISH_FONT_SIZE, UIConfig.ENGLISH_FONT_WEIGHT,
            self.theme['english_bg'], self.theme['english_fg'], height=60
        )

        # ===== INFO BOX =====
        widgets['root_text'] = ft.Text("", color=self.theme['info_fg'], size=12)
        widgets['notes_text'] = ft.Text("", color=self.theme['info_fg'], size=12, italic=True)
        widgets['variants_text'] = ft.Text("", color=self.theme['info_fg'], size=12)
        widgets['translations_text'] = ft.Text("", color=self.theme['info_fg'], size=12)

        widgets['info_container'] = ft.Container(
            content=ft.Column(
                controls=[
                    widgets['root_text'],
                    widgets['notes_text'],
                    widgets['variants_text'],
                    widgets['translations_text']
                ],
                spacing=2
            ),
            bgcolor=self.theme['info_bg'],
            border_radius=UIConfig.TEXT_BOX_BORDER_RADIUS,
            padding=10,
            width=float('inf')
        )

        # ===== CARD FRAME =====
        widgets['card_frame'] = ft.Container(
            content=ft.Column(
                controls=[
                    widgets['hebrew_container'],
                    widgets['trans_container'],
                    widgets['english_container'],
                    widgets['info_container']
                ],
                spacing=10
            ),
            bgcolor=self.theme['card_bg'],
            border_radius=UIConfig.CARD_BORDER_RADIUS,
            padding=20,
            alignment=ft.alignment.center
        )

        # ===== CONTROL BUTTONS =====
        widgets['audio_btn'] = self.create_button(
            "🔊 Play Audio", callbacks['play_audio'], self.theme['btn_audio']
        )
        
        widgets['show_answer_btn'] = self.create_button(
            "👁 Show Answer", callbacks['show_answer'], self.theme['btn_answer']
        )

        widgets['button_frame'] = ft.Row(
            controls=[widgets['audio_btn'], widgets['show_answer_btn']],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # ===== RESPONSE BUTTONS =====
        widgets['again_btn'] = self.create_button("Again (1)", callbacks['mark_again'], self.theme['btn_again'])
        widgets['hard_btn'] = self.create_button("Hard (2)", callbacks['mark_hard'], self.theme['btn_hard'])
        widgets['good_btn'] = self.create_button("Good (3)", callbacks['mark_good'], self.theme['btn_good'])
        widgets['easy_btn'] = self.create_button("Easy (4)", callbacks['mark_easy'], self.theme['btn_easy'])

        widgets['response_frame'] = ft.Row(
            controls=[
                widgets['again_btn'],
                widgets['hard_btn'],
                widgets['good_btn'],
                widgets['easy_btn']
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        # ===== KEYBOARD HINT =====
        widgets['keyboard_hint'] = ft.Text(
            "Keyboard: 1=Again  2=Hard  3=Good  4=Easy  |  Space=Show  P=Audio",
            font_family=UIConfig.HINT_FONT_FAMILY,
            size=UIConfig.HINT_FONT_SIZE,
            color=self.theme['hint_fg'],
            italic=True,
            text_align=ft.TextAlign.CENTER
        )

        # ===== MAIN LAYOUT =====
        self.page.add(
            widgets['nav_bar'],
            ft.Container(
                content=ft.Column(
                    controls=[
                        widgets['top_bar'],
                        widgets['card_frame'],
                        widgets['button_frame'],
                        widgets['response_frame'],
                        widgets['keyboard_hint']
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=UIConfig.WINDOW_PADDING,
                expand=True
            )
        )
        
        return widgets

    def apply_theme(self, widgets, theme):
        """Apply theme to all widgets"""
        self.theme = theme
        self.page.bgcolor = theme['bg']
        
        # Update Nav Bar
        if 'nav_bar' in widgets:
            widgets['nav_bar'].bgcolor = theme['nav_bg']
            # Update nav buttons text color if possible, or recreate them
            # Flet controls update automatically if we change their properties
            for nav_key in ['nav_study', 'nav_settings', 'nav_vocabulary', 'nav_help']:
                if nav_key in widgets:
                    widgets[nav_key].content.color = theme['nav_btn_fg']

        # Update Top Bar
        if 'title_label' in widgets: widgets['title_label'].color = theme['text_fg']
        if 'progress_label' in widgets: widgets['progress_label'].color = theme['label_fg']
        if 'stats_label' in widgets: widgets['stats_label'].color = theme['label_fg']
        if 'theme_toggle_btn' in widgets:
            widgets['theme_toggle_btn'].icon = ft.Icons.DARK_MODE if theme == Themes.LIGHT else ft.Icons.LIGHT_MODE
            widgets['theme_toggle_btn'].icon_color = theme['text_fg']

        # Update Card Frame
        if 'card_frame' in widgets: widgets['card_frame'].bgcolor = theme['card_bg']
        
        # Update Text Containers
        if 'hebrew_container' in widgets: widgets['hebrew_container'].bgcolor = theme['text_bg']
        if 'hebrew_text' in widgets: widgets['hebrew_text'].color = theme['text_fg']
        
        if 'trans_container' in widgets: widgets['trans_container'].bgcolor = theme['trans_bg']
        if 'trans_text' in widgets: widgets['trans_text'].color = theme['trans_fg']
        
        if 'english_container' in widgets: widgets['english_container'].bgcolor = theme['english_bg']
        if 'english_text' in widgets: widgets['english_text'].color = theme['english_fg']
        
        # Update Info Box
        if 'info_container' in widgets: widgets['info_container'].bgcolor = theme['info_bg']
        for key in ['root_text', 'notes_text', 'variants_text', 'translations_text']:
            if key in widgets: widgets[key].color = theme['info_fg']
            
        # Update Buttons
        btn_map = {
            'audio_btn': 'btn_audio',
            'show_answer_btn': 'btn_answer',
            'again_btn': 'btn_again',
            'hard_btn': 'btn_hard',
            'good_btn': 'btn_good',
            'easy_btn': 'btn_easy'
        }
        for btn_key, color_key in btn_map.items():
            if btn_key in widgets:
                widgets[btn_key].style.bgcolor = theme[color_key]
                
        # Update Hint
        if 'keyboard_hint' in widgets: widgets['keyboard_hint'].color = theme['hint_fg']
        
        self.page.update()

class DialogHelper:
    """Helper for creating dialogs"""
    
    @staticmethod
    def show_custom_range_dialog(page, callback):
        """Show dialog for custom rank range selection"""
        start_field = ft.TextField(label="From rank", value="1", width=100)
        end_field = ft.TextField(label="To rank", value="100", width=100)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Custom Range"),
            content=ft.Column([
                ft.Text("Select rank range:"),
                ft.Row([start_field, end_field])
            ], height=100),
        )

        def close_dlg(e):
            page.close(dlg)

        def on_ok(e):
            try:
                start = int(start_field.value)
                end = int(end_field.value)
                if start > 0 and end >= start:
                    page.close(dlg)
                    callback(start, end)
                else:
                    page.open(ft.SnackBar(ft.Text("Please enter valid rank numbers.")))
            except ValueError:
                page.open(ft.SnackBar(ft.Text("Please enter numbers only.")))

        dlg.actions = [
            ft.TextButton("Cancel", on_click=close_dlg),
            ft.TextButton("Start Session", on_click=on_ok),
        ]
        
        page.open(dlg)
    
    @staticmethod
    def show_about_dialog(page, vocabulary_count):
        """Show about dialog"""
        dlg = ft.AlertDialog(
            title=ft.Text("About"),
            content=ft.Text(
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
            ),
        )
        dlg.actions = [
            ft.TextButton("OK", on_click=lambda e: page.close(dlg))
        ]
        page.open(dlg)
    
    @staticmethod
    def show_statistics(page, vocabulary_count, progress):
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
            confidence_text = "\n\nHighest Confidence Words:\n"
            for word_key, score in top_confidence:
                hebrew = word_key.split('_', 1)[1] if '_' in word_key else word_key
                confidence_text += f"  {hebrew}: {score:.2f}/4.0\n"
        else:
            confidence_text = ""
        
        dlg = ft.AlertDialog(
            title=ft.Text("Vocabulary Statistics"),
            content=ft.Text(
                f"Total Words: {vocabulary_count}\n\n"
                f"Confidence Levels:\n"
                f"  Easy (Mastered): {easy} ({easy/vocabulary_count*100:.1f}%)\n"
                f"  Good (Confident): {good} ({good/vocabulary_count*100:.1f}%)\n"
                f"  Hard (Struggling): {hard} ({hard/vocabulary_count*100:.1f}%)\n"
                f"  Again (Need Review): {again} ({again/vocabulary_count*100:.1f}%)\n\n"
                f"Not Studied Yet: {not_studied} ({not_studied/vocabulary_count*100:.1f}%)"
                f"{confidence_text}"
            ),
        )
        dlg.actions = [
            ft.TextButton("OK", on_click=lambda e: page.close(dlg))
        ]
        page.open(dlg)
