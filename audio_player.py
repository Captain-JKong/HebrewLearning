"""
Audio Playback
Handles Hebrew text-to-speech using macOS 'say' command
"""

import subprocess

class AudioPlayer:
    """Manages audio pronunciation"""
    
    def __init__(self, voice='Carmit'):
        self.voice = voice
    
    def play(self, hebrew_text):
        """Play Hebrew text using macOS text-to-speech"""
        if not hebrew_text:
            return
        
        try:
            # Use macOS 'say' command with Hebrew voice
            subprocess.Popen(
                ['say', '-v', self.voice, hebrew_text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"Audio playback error: {e}")
