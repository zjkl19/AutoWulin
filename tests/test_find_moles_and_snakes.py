# tests/test_find_moles_and_snakes.py

import pytest
from unittest.mock import patch, MagicMock
from src.auto_whack_a_mole import AutoWhackAMole
import numpy as np

# 测试find_moles_and_snakes方法的单元测试

@patch('cv2.matchTemplate')
@patch('cv2.cvtColor')
def test_find_moles_and_snakes_single_match(mock_cvtColor, mock_matchTemplate):
    """
    测试单一匹配情况：
    模拟一个截图和模板匹配，匹配值为1.0，意味着模板完全匹配。
    """
    # 模拟cv2.cvtColor转换函数，返回原图像
    mock_cvtColor.side_effect = lambda x, y: x
    # 模拟cv2.matchTemplate返回一个全匹配的值矩阵
    mock_matchTemplate.return_value = np.array([[1.0]])
    
    # 配置初始化
    config = {
        'time_limit': 60,
        'threshold': 0.8,
        'sleep_interval': 0.03,
        'click_interval': 0.03
    }
    # 初始化游戏对象
    game = AutoWhackAMole('test_game', config)
    game.resolution = (800, 600)  # 设置分辨率
    
    # 模拟模板
    templates = {
        'iron_ore': np.zeros((50, 50), dtype=np.uint8),
        'snake': np.zeros((50, 50), dtype=np.uint8)
    }
    
    # 模拟截图
    screenshot = np.zeros((600, 800), dtype=np.uint8)

    # 调用方法并获取结果
    results = game.find_moles_and_snakes(screenshot, templates)
    
    # 断言结果
    assert len(results) == 2  # 应匹配两个模板
    assert results[0] == ('iron_ore', (0, 0))  # 模板匹配的位置
    assert results[1] == ('snake', (0, 0))  # 模板匹配的位置

@patch('cv2.matchTemplate')
@patch('cv2.cvtColor')
def test_find_moles_and_snakes_no_match(mock_cvtColor, mock_matchTemplate):
    """
    测试无匹配情况：
    模拟一个截图和模板匹配，匹配值为0.5，低于阈值，意味着模板不匹配。
    """
    # 模拟cv2.cvtColor转换函数，返回原图像
    mock_cvtColor.side_effect = lambda x, y: x
    # 模拟cv2.matchTemplate返回一个低匹配值矩阵
    mock_matchTemplate.return_value = np.array([[0.5]])
    
    # 配置初始化
    config = {
        'time_limit': 60,
        'threshold': 0.8,
        'sleep_interval': 0.03,
        'click_interval': 0.03
    }
    # 初始化游戏对象
    game = AutoWhackAMole('test_game', config)
    game.resolution = (800, 600)
    
    # 模拟模板
    templates = {
        'iron_ore': np.zeros((50, 50), dtype=np.uint8),
        'snake': np.zeros((50, 50), dtype=np.uint8)
    }
    
    # 模拟截图
    screenshot = np.zeros((600, 800), dtype=np.uint8)

    # 调用方法并获取结果
    results = game.find_moles_and_snakes(screenshot, templates)
    
    # 断言结果
    assert len(results) == 0  # 应该没有匹配结果

@patch('cv2.matchTemplate')
@patch('cv2.cvtColor')
def test_find_moles_and_snakes_multiple_matches(mock_cvtColor, mock_matchTemplate):
    """
    测试多重匹配情况：
    模拟一个截图和模板匹配，多个匹配值为0.9，意味着模板多处匹配。
    """
    # 模拟cv2.cvtColor转换函数，返回原图像
    mock_cvtColor.side_effect = lambda x, y: x
    # 模拟cv2.matchTemplate返回一个多匹配值矩阵
    mock_matchTemplate.return_value = np.array([
        [0.9, 0.9],
        [0.9, 0.9]
    ])
    
    # 配置初始化
    config = {
        'time_limit': 60,
        'threshold': 0.8,
        'sleep_interval': 0.03,
        'click_interval': 0.03
    }
    # 初始化游戏对象
    game = AutoWhackAMole('test_game', config)
    game.resolution = (800, 600)
    
    # 模拟模板
    templates = {
        'iron_ore': np.zeros((50, 50), dtype=np.uint8),
        'snake': np.zeros((50, 50), dtype=np.uint8)
    }
    
    # 模拟截图
    screenshot = np.zeros((600, 800), dtype=np.uint8)

    # 调用方法并获取结果
    results = game.find_moles_and_snakes(screenshot, templates)
    
    # 断言结果
    assert len(results) == 8  # 应匹配八个位置，因为每个模板都匹配四个位置
    assert ('iron_ore', (0, 0)) in results
    assert ('iron_ore', (1, 0)) in results
    assert ('iron_ore', (0, 1)) in results
    assert ('iron_ore', (1, 1)) in results
    assert ('snake', (0, 0)) in results
    assert ('snake', (1, 0)) in results
    assert ('snake', (0, 1)) in results
    assert ('snake', (1, 1)) in results

if __name__ == "__main__":
    pytest.main()
