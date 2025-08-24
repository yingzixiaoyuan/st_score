"""
数据历史页面模块
处理考试数据历史查看和管理功能
"""

import streamlit as st
from .color_settings import get_score_color, load_color_settings


def show_data_history_page(analyzer, exams_df):
    """显示数据历史页面"""
    st.header("📚 数据历史")

    if not exams_df.empty:
        # 显示考试统计
        col1, col2, col3 = st.columns(3)
        with col1:
            total_exams = len(exams_df)
            st.metric("📊 总考试数", total_exams)
        with col2:
            latest_exam = exams_df.iloc[0]['exam_name']
            st.metric("🕒 最新考试", latest_exam)
        with col3:
            latest_time = exams_df.iloc[0]['upload_time']
            st.metric("🔄 更新时间", latest_time)

        # 考试历史列表
        st.subheader("📋 考试历史")

        # 简化的搜索功能
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_term = st.text_input(
                "🔍 搜索考试名称",
                placeholder="输入考试名称关键词",
                key="search_exam"
            )
        with search_col2:
            # 添加空行来对齐按钮位置
            st.write("")  # 空行，用于垂直对齐
            # 删除所有数据按钮放在搜索框右边
            if st.button(
                "🗑️ 删除所有数据",
                type="primary",
                help="删除所有考试数据",
                use_container_width=True
            ):
                st.session_state['show_delete_all_dialog'] = True

        # 过滤考试数据
        if search_term:
            filtered_exams = exams_df[
                exams_df['exam_name'].str.contains(
                    search_term, case=False, na=False)
            ]
            if filtered_exams.empty:
                st.warning(f"🔍 未找到包含 '{search_term}' 的考试")
            else:
                st.success(
                    f"🔍 搜索 '{search_term}' 找到 {len(filtered_exams)} 个考试")
        else:
            filtered_exams = exams_df

        # 显示考试列表
        if not filtered_exams.empty:
            display_df = filtered_exams.copy()
            if 'file_path' not in display_df.columns:
                display_df['file_path'] = '未知'

            # 重命名为中文列名以便展示
            rename_map = {
                'exam_name': '考试名称',
                'upload_time': '上传时间',
                'student_count': '学生数量',
                'file_path': '文件路径'
            }
            display_df = display_df.rename(columns=rename_map)

            # 使用简单的dataframe显示，并添加操作列
            # 为每行添加详情和删除按钮
            for index, row in display_df.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns(
                    [3, 2, 1, 2, 1, 1])

                with col1:
                    st.write(f"**{row['考试名称']}**")
                with col2:
                    st.write(row['上传时间'])
                with col3:
                    st.write(f"{row['学生数量']} 人")
                with col4:
                    st.write(row['文件路径'])
                with col5:
                    # 详情按钮
                    if st.button(
                        "👁️",
                        key=f"detail_btn_{index}",
                        help="查看此考试详情"
                    ):
                        st.session_state['selected_exam_for_detail'] = \
                            row['考试名称']
                with col6:
                    # 删除按钮
                    if st.button(
                        "🗑️",
                        key=f"delete_btn_{index}",
                        help="删除此考试"
                    ):
                        st.session_state['delete_exam_name'] = row['考试名称']
                        st.session_state['show_delete_dialog'] = True

                # 分隔线
                st.divider()

            # 使用st.dialog实现删除确认对话框
            if st.session_state.get('show_delete_dialog', False):
                exam_to_delete = st.session_state.get('delete_exam_name', '')

                # 创建删除确认对话框
                @st.dialog("⚠️ 确认删除考试")
                def delete_confirmation_dialog():
                    st.warning(
                        f"确认删除考试 '{exam_to_delete}' 吗？"
                    )
                    st.info(
                        "此操作不可恢复，将删除该考试的所有数据！"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ 确认删除", type="primary"):
                            # 执行删除操作
                            success, message = analyzer.delete_exam(
                                exam_to_delete)
                            if success:
                                st.success(f"✅ 考试 '{exam_to_delete}' 已成功删除")
                                # 清除状态并关闭对话框
                                st.session_state.pop(
                                    'show_delete_dialog', None)
                                st.session_state.pop('delete_exam_name', None)
                                st.rerun()
                            else:
                                st.error(f"❌ 删除失败: {message}")

                    with col2:
                        if st.button("❌ 取消"):
                            st.session_state.pop('show_delete_dialog', None)
                            st.session_state.pop('delete_exam_name', None)
                            st.rerun()

                # 调用对话框函数
                delete_confirmation_dialog()

            # 删除所有数据的确认对话框
            if st.session_state.get('show_delete_all_dialog', False):
                @st.dialog("⚠️ 确认删除所有数据")
                def delete_all_confirmation_dialog():
                    st.error("⚠️ 危险操作警告！")
                    st.warning("确认删除所有考试数据吗？")
                    st.info(
                        "此操作将：\n"
                        "• 删除所有考试记录\n"
                        "• 删除所有学生成绩数据\n"
                        "• 此操作不可恢复！"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ 确认删除所有", type="primary"):
                            # 执行删除所有操作
                            success, message = analyzer.clear_all_data()
                            if success:
                                st.success("✅ 所有考试数据已成功删除")
                                # 清除状态并关闭对话框
                                st.session_state.pop('show_delete_all_dialog',
                                                     None)
                                st.rerun()
                            else:
                                st.error(f"❌ 删除失败: {message}")

                    with col2:
                        if st.button("❌ 取消", type="secondary"):
                            st.session_state.pop('show_delete_all_dialog',
                                                 None)
                            st.rerun()

                # 调用对话框函数
                delete_all_confirmation_dialog()

            # 简化的考试详情查看
            st.subheader("📊 考试详情查看")

            # 检查是否有选中的考试
            selected_exam = st.session_state.get(
                'selected_exam_for_detail', None)

            if selected_exam:
                # 显示当前选中的考试名称
                st.info(f"当前查看：**{selected_exam}**")

                # 获取考试详情
                exam_detail = analyzer.get_exam_detail(selected_exam)
                if exam_detail:
                    # 考试基本信息
                    st.markdown(f"**考试名称**: {selected_exam}")
                    st.markdown(f"**学生数量**: {len(exam_detail)} 人")

                    # 成绩统计
                    scores = []
                    for score in exam_detail:
                        try:
                            scores.append(float(score['score']))
                        except Exception:
                            pass

                    if scores:
                        avg_score = sum(scores) / len(scores)
                        max_score = max(scores)
                        min_score = min(scores)

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("平均分", f"{avg_score:.1f}")
                        with col2:
                            st.metric("最高分", f"{max_score}")
                        with col3:
                            st.metric("最低分", f"{min_score}")
                        with col4:
                            st.metric("参与人数", f"{len(scores)}")

                        # 成绩分布与等级分布图已移除

                        # 详细成绩列表
                        st.markdown("#### 📋 详细成绩列表")
                        score_data = []
                        for score in exam_detail:
                            score_data.append({
                                "学号": score['student_id'],
                                "学生姓名": score['student_name'],
                                "成绩": round(float(score['score']), 1)  # 保留1位小数
                            })

                        # 按成绩排序
                        score_data.sort(key=lambda x: x['成绩'], reverse=True)

                        # 显示成绩表格，应用颜色设置
                        import pandas as pd
                        score_df = pd.DataFrame(score_data)

                        # 加载颜色设置
                        color_settings = load_color_settings()

                        # 为每行添加背景颜色
                        def highlight_row(row):
                            score = row['成绩']
                            bg_color = get_score_color(score, color_settings)
                            return [
                                f'background-color: {bg_color}' for _ in row
                            ]

                        # 应用样式并显示表格
                        styled_df = score_df.style.apply(
                            highlight_row, axis=1
                        ).format({
                            "成绩": "{:.1f}"
                        })
                        st.dataframe(styled_df, use_container_width=True)

                        # 显示颜色说明
                        st.markdown("**颜色说明：**")
                        color_legend = []
                        for level, config in color_settings.items():
                            color_span_prefix = (
                                f'<span style="background-color: '
                                f'{config["color"]}; '
                            )
                            color_span_mid = (
                                'padding: 2px 8px; border-radius: 3px; '
                                'margin: 2px; display: inline-block;">'
                            )
                            color_span_text = (
                                f'{level} ({config["min_score"]}-'
                                f'{config["max_score"]}分)'
                            )
                            color_legend.append(
                                color_span_prefix + color_span_mid +
                                color_span_text + '</span>'
                            )
                        st.markdown(" ".join(color_legend),
                                    unsafe_allow_html=True)
                else:
                    st.warning(f"❌ 无法获取考试 '{selected_exam}' 的详细信息")
            else:
                st.info("👆 请点击上方考试列表中的 👁️ 按钮查看考试详情")
        else:
            st.info('暂无考试数据')
    else:
        st.info("暂无数据历史，请先导入Excel文件")
