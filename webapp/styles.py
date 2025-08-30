"""
样式模块
包含CSS样式和界面配置
"""

import streamlit as st


def apply_custom_styles():
    """应用自定义CSS样式"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        .search-box {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        .table-container {
            background-color: white;
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .button-container {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .drawer-content {
            background-color: #f8f9fa;
            border-left: 3px solid #007bff;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 0.5rem 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)


def configure_page():
    """配置页面设置"""
    st.set_page_config(
        page_title="学生成绩分析器", 
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
