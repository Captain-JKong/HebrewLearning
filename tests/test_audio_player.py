"""
Tests for AudioPlayer
Tests audio player initialization (actual playback tests are mocked)
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAudioPlayerInit:
    """Test AudioPlayer initialization"""
    
    def test_default_voice(self):
        """Test default voice is set"""
        from audio_player import AudioPlayer
        
        player = AudioPlayer()
        assert player.voice == 'Carmit'
    
    def test_custom_voice(self):
        """Test custom voice can be set"""
        from audio_player import AudioPlayer
        
        player = AudioPlayer(voice='TestVoice')
        assert player.voice == 'TestVoice'


class TestAudioPlayback:
    """Test audio playback (mocked)"""
    
    @patch('audio_player.subprocess.Popen')
    def test_play_calls_subprocess(self, mock_popen):
        """Test that play() calls subprocess"""
        from audio_player import AudioPlayer
        
        player = AudioPlayer()
        player.play('שלום')
        
        mock_popen.assert_called_once()
    
    @patch('audio_player.subprocess.Popen')
    def test_play_uses_correct_voice(self, mock_popen):
        """Test that play() uses the configured voice"""
        from audio_player import AudioPlayer
        
        player = AudioPlayer(voice='Carmit')
        player.play('שלום')
        
        # Check that 'Carmit' is in the call arguments
        call_args = mock_popen.call_args[0][0]
        assert 'Carmit' in call_args
    
    @patch('audio_player.subprocess.Popen')
    def test_play_empty_text_does_nothing(self, mock_popen):
        """Test that empty text doesn't trigger playback"""
        from audio_player import AudioPlayer
        
        player = AudioPlayer()
        player.play('')
        
        mock_popen.assert_not_called()
    
    @patch('audio_player.subprocess.Popen')
    def test_play_none_text_does_nothing(self, mock_popen):
        """Test that None text doesn't trigger playback"""
        from audio_player import AudioPlayer
        
        player = AudioPlayer()
        player.play(None)
        
        mock_popen.assert_not_called()
    
    @patch('audio_player.subprocess.Popen')
    def test_play_handles_exception(self, mock_popen):
        """Test that exceptions are handled gracefully"""
        from audio_player import AudioPlayer
        
        mock_popen.side_effect = Exception("Test error")
        
        player = AudioPlayer()
        # Should not raise an exception
        player.play('שלום')
