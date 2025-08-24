"""
学生成绩分析器 - 主程序
使用模块化结构，代码更清晰易维护
"""

import sys

# 如果是直接运行（不是通过 streamlit CLI）
if __name__ == "__main__" and "streamlit" not in sys.argv[0]:
    import streamlit.web.cli as stcli
    # 注意：app_path 用 __file__ 获取准路径
    sys.argv = ["streamlit", "run", __file__,
                "--server.headless=true",
                "--server.port=8501",
                "--server.address=0.0.0.0"]
    sys.exit(stcli.main())

import streamlit as st
from database import DatabaseManager
from analyzer import ScoreAnalyzer
from pages import (
    show_data_import_page,
    show_exam_analysis_page,
    show_data_history_page
)
from pages.color_settings import show_color_settings_page
from config import PAGE_CONFIG
from styles import apply_custom_styles, configure_page


def main():
    """主函数"""
    # 配置页面
    configure_page()

    # 应用自定义样式
    apply_custom_styles()

    # 主标题
    st.markdown(
        '<h1 class="main-header">📊 学生成绩分析器</h1>',
        unsafe_allow_html=True
    )

    # 创建数据库管理器和分析器
    db_manager = DatabaseManager()
    analyzer = ScoreAnalyzer(db_manager)

    # 获取所有考试数据
    exams_df = analyzer.get_all_exams()

    # 左侧页面菜单
    st.sidebar.title("🎯 页面菜单")

    # 页面选项
    page_options = PAGE_CONFIG['OPTIONS']

    # 初始化页面选择状态
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = PAGE_CONFIG['DEFAULT']

    # 页面选择（使用按钮组，更稳定）
    for page_name in page_options:
        if st.sidebar.button(
            page_name,
            key=f"btn_{page_name}",
            use_container_width=True,
            type=("primary" if page_name == st.session_state['current_page']
                  else "secondary")
        ):
            st.session_state['current_page'] = page_name
            st.rerun()

    # 主界面内容
    current_page = st.session_state['current_page']
    if current_page == "📁 数据导入":
        show_data_import_page(analyzer)
    elif current_page == "📝 考试分析":
        show_exam_analysis_page(analyzer, exams_df)
    elif current_page == "📚 数据历史":
        show_data_history_page(analyzer, exams_df)
    elif current_page == "🎨 颜色设置":
        show_color_settings_page()


if __name__ == "__main__":
    main()
