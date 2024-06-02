# tests/test_auto_whack_a_mole.py

import pytest
from unittest.mock import patch, MagicMock
from src.auto_whack_a_mole import AutoWhackAMole

@patch('pygetwindow.getWindowsWithTitle')
def test_get_window_resolution(mock_getWindowsWithTitle):
    # 设置模拟返回值
    mock_window = MagicMock()
    mock_window.width = 800
    mock_window.height = 600
    mock_getWindowsWithTitle.return_value = [mock_window]

    config = {
        'time_limit': 60,
        'threshold': 0.8,
        'sleep_interval': 0.03,
        'click_interval': 0.03
    }
    game = AutoWhackAMole('test_game', config)
    resolution = game.get_window_resolution()
    
    # 断言
    assert resolution == (800, 600)
    assert game.window is not None
