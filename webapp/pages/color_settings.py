"""
颜色设置页面模块
允许用户自定义分数区间的显示颜色
"""

import streamlit as st
import json
import os


def show_color_settings_page():
    """显示颜色设置页面"""
    st.header("🎨 颜色设置")
    st.markdown("自定义不同分数区间的背景颜色，用于成绩详情表格的显示")

    # 默认颜色配置
    default_colors = {
        "优秀": {"min_score": 90, "max_score": 150, "color": "#90EE90", "description": "90分及以上"},
        "良好": {"min_score": 80, "max_score": 89, "color": "#87CEEB", "description": "80-89分"},
        "中等": {"min_score": 70, "max_score": 79, "color": "#F0E68C", "description": "70-79分"},
        "及格": {"min_score": 60, "max_score": 69, "color": "#FFB6C1", "description": "60-69分"},
        "不及格": {"min_score": 0, "max_score": 59, "color": "#FFA07A", "description": "60分以下"}
    }

    # 从session_state或文件加载颜色配置
    if 'color_settings' not in st.session_state:
        # 根据全局最高分生成默认配置
        default_max_score = 150  # 默认最高分
        st.session_state.color_settings = {
            "优秀": {"min_score": 90, "max_score": default_max_score, "color": "#90EE90", "description": "90分及以上"},
            "良好": {"min_score": 80, "max_score": 89, "color": "#87CEEB", "description": "80-89分"},
            "中等": {"min_score": 70, "max_score": 79, "color": "#F0E68C", "description": "70-79分"},
            "及格": {"min_score": 60, "max_score": 69, "color": "#FFB6C1", "description": "60-69分"},
            "不及格": {"min_score": 0, "max_score": 59, "color": "#FFA07A", "description": "60分以下"}
        }

    # 颜色选择器
    st.subheader("📊 分数区间颜色设置")

    # 全局最高分设置
    st.markdown("**全局设置：**")
    global_max_score = st.number_input(
        "设置系统最高分",
        min_value=100,
        max_value=1000,
        value=150,
        step=10,
        help="设置整个系统的最高分数，影响所有分数区间的上限"
    )

    # 创建颜色配置表单
    with st.form("color_settings_form"):
        st.markdown("**设置不同分数区间的背景颜色：**")

        # 为每个等级创建颜色选择器
        updated_colors = {}

        for level, config in st.session_state.color_settings.items():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

            with col1:
                st.write(f"**{level}** ({config['description']})")

            with col2:
                min_score = st.number_input(
                    "最低分",
                    min_value=0,
                    max_value=global_max_score,
                    value=config['min_score'],
                    key=f"min_{level}",
                    label_visibility="collapsed"
                )

            with col3:
                max_score = st.number_input(
                    "最高分",
                    min_value=0,
                    max_value=global_max_score,
                    value=config['max_score'],
                    key=f"max_{level}",
                    label_visibility="collapsed"
                )

            with col4:
                color = st.color_picker(
                    "选择颜色",
                    value=config['color'],
                    key=f"color_{level}",
                    label_visibility="collapsed"
                )

            updated_colors[level] = {
                "min_score": min_score,
                "max_score": max_score,
                "color": color,
                "description": config['description']
            }

        # 表单提交按钮
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("💾 保存颜色设置", type="primary")

        if submit_button:
            # 验证分数区间
            valid = True
            for level, config in updated_colors.items():
                if config['min_score'] > config['max_score']:
                    st.error(f"❌ {level}：最低分不能大于最高分")
                    valid = False
                    break

            if valid:
                # 检查分数区间是否有重叠
                sorted_configs = sorted(
                    updated_colors.items(), key=lambda x: x[1]['min_score'])
                for i in range(len(sorted_configs) - 1):
                    current_max = sorted_configs[i][1]['max_score']
                    next_min = sorted_configs[i + 1][1]['min_score']
                    if current_max >= next_min:
                        st.error(
                            f"❌ 分数区间有重叠：{sorted_configs[i][0]} 和 {sorted_configs[i + 1][0]}")
                        valid = False
                        break

                if valid:
                    st.session_state.color_settings = updated_colors
                    st.success("✅ 颜色设置已保存！")

                    # 保存到文件
                    save_color_settings(updated_colors)

    # 颜色预览
    st.subheader("🎨 颜色预览")
    st.markdown("**当前颜色配置预览：**")

    # 创建预览表格
    preview_data = []
    for level, config in st.session_state.color_settings.items():
        preview_data.append({
            "等级": level,
            "分数区间": f"{config['min_score']}-{config['max_score']}分",
            "描述": config['description'],
            "颜色预览": config['color']
        })

    # 显示预览表格
    for row in preview_data:
        col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
        with col1:
            st.write(f"**{row['等级']}**")
        with col2:
            st.write(row['分数区间'])
        with col3:
            st.write(row['描述'])
        with col4:
            # 显示颜色块
            st.markdown(
                f'<div style="background-color: {row["颜色预览"]}; '
                f'width: 30px; height: 20px; border: 1px solid #ccc; '
                f'border-radius: 3px;"></div>',
                unsafe_allow_html=True
            )

    # 重置和导入导出功能
    st.subheader("⚙️ 高级设置")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 重置为默认", type="secondary"):
            st.session_state.color_settings = default_colors.copy()
            st.success("✅ 已重置为默认颜色设置")
            st.rerun()

    with col2:
        if st.button("📥 导入配置", type="secondary"):
            uploaded_file = st.file_uploader(
                "选择JSON配置文件",
                type=['json'],
                key="import_config"
            )
            if uploaded_file is not None:
                try:
                    imported_config = json.load(uploaded_file)
                    st.session_state.color_settings = imported_config
                    st.success("✅ 配置导入成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 导入失败：{str(e)}")

    with col3:
        if st.button("📤 导出配置", type="secondary"):
            config_json = json.dumps(
                st.session_state.color_settings, indent=2, ensure_ascii=False)
            st.download_button(
                label="下载配置文件",
                data=config_json,
                file_name="color_settings.json",
                mime="application/json"
            )

    # 使用说明
    st.subheader("📖 使用说明")
    st.markdown("""
    **颜色设置说明：**
    1. **分数区间**：设置每个等级对应的分数范围
    2. **背景颜色**：选择该分数区间在成绩表格中显示的颜色
    3. **区间不重叠**：确保不同等级的分数区间没有重叠
    4. **自动应用**：设置保存后，成绩详情表格会自动应用这些颜色
    
    **建议颜色搭配：**
    - 🟢 优秀：绿色系（#90EE90, #98FB98）
    - 🔵 良好：蓝色系（#87CEEB, #ADD8E6）
    - 🟡 中等：黄色系（#F0E68C, #FFFFE0）
    - 🟠 及格：橙色系（#FFB6C1, #FFE4E1）
    - 🔴 不及格：红色系（#FFA07A, #FFE4E1）
    """)


def save_color_settings(colors):
    """保存颜色设置到文件"""
    try:
        config_dir = os.path.join("config")
        os.makedirs(config_dir, exist_ok=True)

        config_file = os.path.join(config_dir, "color_settings.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(colors, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        st.error(f"保存配置文件失败：{str(e)}")
        return False


def load_color_settings():
    """从文件加载颜色设置"""
    try:
        config_file = os.path.join("config", "color_settings.json")
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass

    # 返回默认配置
    return {
        "优秀": {"min_score": 90, "max_score": 150, "color": "#90EE90", "description": "90分及以上"},
        "良好": {"min_score": 80, "max_score": 89, "color": "#87CEEB", "description": "80-89分"},
        "中等": {"min_score": 70, "max_score": 79, "color": "#F0E68C", "description": "70-79分"},
        "及格": {"min_score": 60, "max_score": 69, "color": "#FFB6C1", "description": "60-69分"},
        "不及格": {"min_score": 0, "max_score": 59, "color": "#FFA07A", "description": "60分以下"}
    }


def get_score_color(score, color_settings):
    """根据分数获取对应的背景颜色"""
    try:
        score = float(score)
        for level, config in color_settings.items():
            if config['min_score'] <= score <= config['max_score']:
                return config['color']

        # 如果没有匹配到任何区间，返回默认颜色
        # 根据分数范围返回合适的默认颜色
        if score >= 90:
            return "#90EE90"  # 浅绿色
        elif score >= 80:
            return "#87CEEB"  # 浅蓝色
        elif score >= 70:
            return "#F0E68C"  # 浅黄色
        elif score >= 60:
            return "#FFB6C1"  # 浅粉色
        else:
            return "#FFA07A"  # 浅橙色

    except (ValueError, TypeError) as e:
        print(f"处理分数 {score} 时出错: {e}")
        return "#F0F0F0"  # 浅灰色作为错误情况的默认色
