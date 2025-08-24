"""
数据导入页面模块
处理Excel文件上传和数据导入功能
"""

import streamlit as st
from config import UPLOAD_CONFIG
from pathlib import Path


def show_data_import_page(analyzer):
    """显示数据导入页面"""
    st.header("📁 数据导入")

    # 显示Excel文件格式要求
    st.subheader("📋 Excel文件格式要求")

    # 创建两列布局
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        **必需字段：**
        - **学号**：学生的唯一标识符（必填）
        - **姓名**：学生姓名（必填）
        - **成绩**：考试分数（必填）

        **可选字段：**
        - **班级**：学生所在班级
        - **备注**：其他说明信息

        **注意事项：**
        - 学号必须唯一，避免同名学生数据混乱
        - 成绩必须是数字，支持小数
        - 文件第一行应该是字段标题
        - 支持.xlsx和.xls格式
        """)

    with col2:
        # 显示示例表格
        st.markdown("**示例格式：**")
        import pandas as pd

        example_data = {
            '学号': ['2024001', '2024002', '2024003'],
            '姓名': ['张三', '李四', '王五'],
            '成绩': [85, 92, 78],
            '班级': ['一班', '一班', '二班']
        }
        example_df = pd.DataFrame(example_data)
        st.dataframe(example_df, use_container_width=True)

    # 字段验证选项
    st.subheader("⚙️ 导入选项")

    col1, col2 = st.columns(2)
    with col1:
        require_student_id = st.checkbox(
            "要求学号列",
            value=True,
            help="勾选后，Excel文件必须包含学号列，否则导入失败"
        )

    with col2:
        auto_generate_id = st.checkbox(
            "自动生成学号",
            value=False,
            help="如果没有学号列，自动生成学号（格式：ST001, ST002...）"
        )

    # 检查是否已经处理过文件
    if 'files_processed' in st.session_state and st.session_state['files_processed']:
        st.success("✅ 文件已处理完成！如需重新导入，请刷新页面。")
        if st.button("🔄 重新导入"):
            st.session_state['files_processed'] = False
            st.rerun()
        return

    # 支持多文件上传
    uploaded_files = st.file_uploader(
        "选择Excel文件（支持多选）",
        type=UPLOAD_CONFIG['ALLOWED_TYPES'],
        accept_multiple_files=True,
        help=UPLOAD_CONFIG['HELP_TEXT']
    )

    # 显示导入统计
    if uploaded_files:
        st.success(f"已选择 {len(uploaded_files)} 个文件")

        # 文件类型统计
        excel_count = len([
            f for f in uploaded_files
            if f.name.endswith(tuple(UPLOAD_CONFIG['ALLOWED_TYPES']))
        ])
        other_count = len(uploaded_files) - excel_count

        if excel_count > 0:
            st.write(f"📊 Excel文件: {excel_count} 个")
        if other_count > 0:
            st.write(f"⚠️ 其他文件: {other_count} 个")

        # 显示选择的文件列表
        st.subheader("📋 选择的文件")
        for i, file in enumerate(uploaded_files):
            file_icon = ("📊" if file.name.endswith(
                tuple(UPLOAD_CONFIG['ALLOWED_TYPES'])) else "📄")
            st.write(f"{file_icon} {i+1}. {file.name}")

        # 自动导入所有Excel文件
        if excel_count > 0:
            st.subheader("🚀 自动导入")
            
            # 检查是否正在导入
            if 'importing' not in st.session_state:
                st.session_state['importing'] = False
            
            if not st.session_state['importing']:
                if st.button("🚀 开始导入", type="primary"):
                    st.session_state['importing'] = True
                    st.rerun()
            else:
                st.info(f"检测到 {excel_count} 个Excel文件，正在自动导入...")

                # 自动导入
                with st.spinner("正在批量导入..."):
                    success_count = 0
                    skip_files = []
                    error_messages = []

                    # 只处理Excel文件
                    excel_files = [
                        f for f in uploaded_files
                        if f.name.endswith(tuple(UPLOAD_CONFIG['ALLOWED_TYPES']))
                    ]

                    # 预检查：已存在考试跳过
                    files_to_import = []
                    for file in excel_files:
                        exam_name = Path(file.name).stem
                        try:
                            existing_exam = analyzer.db.get_exam_by_name(exam_name)
                            if existing_exam is not None and not existing_exam.empty:
                                skip_files.append(file.name)
                            else:
                                files_to_import.append(file)
                        except Exception:
                            # 若检查失败，谨慎起见仍加入导入列表
                            files_to_import.append(file)

                    if skip_files:
                        st.warning("以下考试已存在，已跳过导入：")
                        for name in skip_files:
                            st.warning(f"- {name}")

                    # 执行导入（仅新考试）
                    for file in files_to_import:
                        success, message = analyzer.process_excel_file(
                            file,
                            require_student_id=require_student_id,
                            auto_generate_id=auto_generate_id
                        )
                        if success:
                            success_count += 1
                        else:
                            error_messages.append(f"{file.name}: {message}")

                    total = len(excel_files)
                    skipped = len(skip_files)
                    imported = len(files_to_import)

                    # 显示导入结果
                    if imported == 0 and skipped > 0 and not error_messages:
                        st.info(f"ℹ️ 所有 {total} 个文件对应的考试均已存在，全部跳过导入。")
                        st.session_state['files_processed'] = True
                        st.session_state['importing'] = False
                    elif success_count == imported and not error_messages:
                        st.success(f"✅ 导入完成：成功 {success_count} 个，跳过 {skipped} 个。")
                        st.session_state['files_processed'] = True
                        st.session_state['importing'] = False
                    elif success_count > 0 or skipped > 0:
                        st.warning(
                            f"⚠️ 导入部分完成：成功 {success_count} 个，跳过 {skipped} 个，失败 {len(error_messages)} 个。")
                        if error_messages:
                            st.error("❌ 导入失败的文件：")
                            for error in error_messages:
                                st.error(error)
                        st.session_state['files_processed'] = True
                        st.session_state['importing'] = False
                    else:
                        st.error("❌ 所有Excel文件导入失败")
                        for error in error_messages:
                            st.error(error)
                        st.session_state['importing'] = False
        else:
            st.warning("没有选择Excel文件，请选择包含学生成绩的Excel文件")
    else:
        st.info("请选择Excel文件进行导入")
