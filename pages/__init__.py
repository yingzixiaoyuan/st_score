"""
页面模块包
包含所有页面的显示逻辑和用户界面
"""

from .data_import import show_data_import_page
from .exam_analysis import show_exam_analysis_page
from .data_history import show_data_history_page
from .color_settings import show_color_settings_page

__all__ = [
    'show_data_import_page',
    'show_exam_analysis_page', 
    'show_data_history_page',
    'show_color_settings_page'
]

