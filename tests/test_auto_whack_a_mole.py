# tests/test_auto_whack_a_mole.py

import pytest
from unittest.mock import patch, MagicMock
from src.auto_whack_a_mole import AutoWhackAMole
import numpy as np
import os

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

@patch('pygetwindow.getWindowsWithTitle')
@patch('pyautogui.screenshot')
@patch('cv2.cvtColor')
def test_capture_screen(mock_cvtColor, mock_screenshot, mock_getWindowsWithTitle):
    # 设置模拟返回值
    mock_window = MagicMock()
    mock_window.left = 100
    mock_window.top = 100
    mock_window.width = 800
    mock_window.height = 600
    mock_getWindowsWithTitle.return_value = [mock_window]

    mock_screenshot.return_value = np.zeros((600, 800, 3), dtype=np.uint8)
    mock_cvtColor.side_effect = lambda x, y: x

    config = {
        'time_limit': 60,
        'threshold': 0.8,
        'sleep_interval': 0.03,
        'click_interval': 0.03
    }
    game = AutoWhackAMole('test_game', config)
    game.get_window_resolution()  # 初始化窗口

    screenshot = game.capture_screen()
    
    # 断言
    mock_screenshot.assert_called_once_with(region=(100, 100, 800, 600))
    mock_cvtColor.assert_called_once()
    assert screenshot is not None

@patch('pygetwindow.getWindowsWithTitle')
@patch('cv2.imread')
@patch('cv2.resize')
def test_load_templates(mock_resize, mock_imread, mock_getWindowsWithTitle):
    # 设置模拟返回值
    mock_window = MagicMock()
    mock_window.width = 800
    mock_window.height = 600
    mock_getWindowsWithTitle.return_value = [mock_window]

    mock_imread.return_value = np.zeros((100, 100), dtype=np.uint8)
    mock_resize.side_effect = lambda x, size, fx, fy: np.zeros((int(100 * fy), int(100 * fx)), dtype=np.uint8)

    config = {
        'time_limit': 60,
        'threshold': 0.8,
        'sleep_interval': 0.03,
        'click_interval': 0.03
    }
    game = AutoWhackAMole('test_game', config)
    game.get_window_resolution()  # 初始化窗口

    templates = game.load_templates()
    
    # 断言
    assert 'snake' in templates
    assert 'female_mole' in templates
    assert 'iron_ore' in templates
    mock_imread.assert_any_call(os.path.join(game.image_dir, 'snake.png'), 0)
    mock_imread.assert_any_call(os.path.join(game.image_dir, 'female_mole.png'), 0)
    mock_imread.assert_any_call(os.path.join(game.image_dir, 'iron_ore.png'), 0)
    mock_resize.assert_called()