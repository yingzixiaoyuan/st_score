"""
数据分析模块
负责成绩分析、统计计算和数据处理
"""

import pandas as pd
import numpy as np
from pathlib import Path


class ScoreAnalyzer:
    """成绩分析器"""

    def __init__(self, db_manager):
        self.db = db_manager

    def process_excel_file(self, uploaded_file, require_student_id=True, auto_generate_id=False):
        """处理Excel文件"""
        try:
            print(f"开始处理文件: {uploaded_file.name}")

            # 读取Excel文件
            df = pd.read_excel(uploaded_file)

            # 检查必需列
            required_columns = ["成绩"]
            if require_student_id:
                required_columns.append("学号")
            else:
                required_columns.append("姓名")

            missing_columns = [
                col for col in required_columns if col not in df.columns]
            if missing_columns:
                return False, f"Excel文件缺少必需列：{', '.join(missing_columns)}"

            # 提取考试名称
            exam_name = Path(uploaded_file.name).stem
            print(f"考试名称: {exam_name}")

            # 第一步：处理考试信息
            print("=== 第一步：处理考试信息 ===")
            exam_result = self._handle_exam_info(
                exam_name, uploaded_file.name, len(df))
            if not exam_result['success']:
                return False, exam_result['message']

            exam_id = exam_result['exam_id']
            print(f"考试处理完成，ID: {exam_id}")

            # 第二步：预处理学生信息
            print("=== 第二步：预处理学生信息 ===")
            student_result = self._preprocess_students(
                df, require_student_id, auto_generate_id)
            if not student_result['success']:
                return False, student_result['message']

            student_id_map = student_result['student_id_map']
            print(f"学生预处理完成，映射表包含 {len(student_id_map)} 个学生")

            # 第三步：处理成绩数据
            print("=== 第三步：处理成绩数据 ===")
            score_result = self._process_scores(
                df, student_id_map, exam_id, require_student_id, auto_generate_id)

            # 返回最终结果
            if score_result['success']:
                return True, f"成功导入 {score_result['success_count']} 名学生成绩（现有学生：{student_result['existing_count']}人，新增学生：{student_result['new_count']}人）"
            else:
                return False, f"导入完成，成功: {score_result['success_count']} 人，失败: {score_result['error_count']} 人（现有学生：{student_result['existing_count']}人，新增学生：{student_result['new_count']}人）"

        except Exception as e:
            print(f"处理文件时出现错误: {str(e)}")
            return False, f"处理文件时出现错误：{str(e)}"

    def _handle_exam_info(self, exam_name, file_path, student_count):
        """处理考试信息"""
        try:
            # 检查考试是否已存在
            existing_exam = self.db.get_exam_by_name(exam_name)

            if not existing_exam.empty:
                # 考试已存在，更新信息
                exam_id = existing_exam.iloc[0]['id']
                print(f"考试 '{exam_name}' 已存在，ID: {exam_id}，将更新信息")

                # 更新考试信息
                success = self.db.update_exam_info(
                    exam_id, file_path, student_count)
                if success:
                    return {'success': True, 'exam_id': exam_id, 'message': f"考试信息更新成功"}
                else:
                    return {'success': False, 'message': f"更新考试信息失败"}
            else:
                # 考试不存在，插入新记录
                print(f"考试 '{exam_name}' 不存在，将创建新记录")
                exam_id = self.db.insert_new_exam(
                    exam_name, file_path, student_count)

                if exam_id:
                    return {'success': True, 'exam_id': exam_id, 'message': f"考试创建成功"}
                else:
                    return {'success': False, 'message': f"创建考试失败"}

        except Exception as e:
            print(f"处理考试信息时出错: {e}")
            return {'success': False, 'message': f"处理考试信息时出错: {str(e)}"}

    def _preprocess_students(self, df, require_student_id, auto_generate_id):
        """预处理学生信息"""
        try:
            student_id_map = {}
            new_students = []
            existing_students = []

            print("正在预处理学生信息...")

            for index, row in df.iterrows():
                # 处理学生标识
                if require_student_id and "学号" in df.columns:
                    student_id_value = str(row["学号"])
                    name = row.get("姓名", f"学生{student_id_value}")
                elif auto_generate_id and "姓名" in df.columns:
                    name = row["姓名"]
                    student_id_value = f"ST{index+1:03d}"
                else:
                    name = row["姓名"]
                    student_id_value = name

                # 检查学生是否已存在
                existing_student_id = self.db.get_student_id_by_student_id(
                    student_id_value)

                if existing_student_id:
                    # 学生已存在，使用现有ID
                    student_id_map[student_id_value] = existing_student_id
                    existing_students.append(name)
                    print(
                        f"学生已存在：{name} (学号: {student_id_value}) -> ID: {existing_student_id}")
                else:
                    # 学生不存在，插入新记录
                    new_student_id = self.db.insert_student_with_id(
                        name, student_id_value)
                    if new_student_id:
                        student_id_map[student_id_value] = new_student_id
                        new_students.append(name)
                        print(
                            f"新学生插入成功：{name} (学号: {student_id_value}) -> ID: {new_student_id}")
                    else:
                        print(f"警告：学生信息插入失败，学号: {student_id_value}，姓名: {name}")

            # 打印学生统计信息
            print(f"本次考试学生统计：")
            print(
                f"  - 现有学生：{len(existing_students)} 人 ({', '.join(existing_students[:5])}{'...' if len(existing_students) > 5 else ''})")
            print(
                f"  - 新增学生：{len(new_students)} 人 ({', '.join(new_students[:5])}{'...' if len(new_students) > 5 else ''})")
            print(f"  - 总学生数：{len(student_id_map)} 人")

            return {
                'success': True,
                'student_id_map': student_id_map,
                'existing_count': len(existing_students),
                'new_count': len(new_students)
            }

        except Exception as e:
            print(f"预处理学生信息时出错: {e}")
            return {'success': False, 'message': f"预处理学生信息时出错: {str(e)}"}

    def _process_scores(self, df, student_id_map, exam_id, require_student_id, auto_generate_id):
        """处理成绩数据"""
        try:
            success_count = 0
            error_count = 0

            print("正在处理成绩数据...")

            for index, row in df.iterrows():
                try:
                    score = row["成绩"]

                    # 处理学生标识
                    if require_student_id and "学号" in df.columns:
                        student_id_value = str(row["学号"])
                        name = row.get("姓名", f"学生{student_id_value}")
                    elif auto_generate_id and "姓名" in df.columns:
                        name = row["姓名"]
                        student_id_value = f"ST{index+1:03d}"
                    else:
                        name = row["姓名"]
                        student_id_value = name

                    # 从映射表获取学生ID
                    student_id = student_id_map.get(student_id_value)

                    if student_id is None:
                        print(f"错误：无法获取学生ID，学号: {student_id_value}，姓名: {name}")
                        print(f"当前映射表: {student_id_map}")
                        error_count += 1
                        continue

                    # 确保student_id是Python原生int类型（修复numpy.int64兼容性问题）
                    student_id = int(student_id)

                    # 插入成绩
                    result = self.db.insert_score(student_id, exam_id, score)
                    if result:
                        success_count += 1
                        print(f"成绩插入成功：{name} -> {score}分")
                    else:
                        error_count += 1
                        print(f"成绩插入失败：{name} -> {score}分")

                except Exception as e:
                    print(f"处理第 {index+1} 行数据时出错: {e}")
                    error_count += 1

            return {
                'success': error_count == 0,
                'success_count': success_count,
                'error_count': error_count
            }

        except Exception as e:
            print(f"处理成绩数据时出错: {e}")
            return {'success': False, 'success_count': 0, 'error_count': 0}

    def get_student_scores(self, selected_exams):
        """获取学生成绩数据"""
        if not selected_exams:
            return pd.DataFrame()

        # 获取原始数据
        df = self.db.get_student_scores(selected_exams)

        if df.empty:
            return df

        # 重塑数据
        df_pivot = df.pivot(index=['student_id', 'name'],
                            columns='exam_name', values='score')
        df_pivot = df_pivot.reset_index()

        # 计算统计信息
        score_columns = [
            col for col in df_pivot.columns if col not in ['student_id', 'name']]

        # 对所有成绩列保留1位小数
        for col in score_columns:
            df_pivot[col] = df_pivot[col].round(1)

        df_pivot['平均分'] = df_pivot[score_columns].mean(axis=1).round(1)
        df_pivot['趋势'] = df_pivot.apply(
            lambda row: self.calculate_trend(row, score_columns), axis=1
        )
        df_pivot['等级'] = df_pivot['平均分'].apply(self.calculate_level)

        return df_pivot

    def calculate_trend(self, row, score_columns):
        """计算成绩趋势"""
        scores = [row[col] for col in score_columns if pd.notna(row[col])]
        if len(scores) < 2:
            return "数据不足"

        if len(scores) == 2:
            if scores[1] > scores[0]:
                return "上升"
            elif scores[1] < scores[0]:
                return "下降"
            else:
                return "持平"
        else:
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]

            first_avg = np.mean(first_half)
            second_avg = np.mean(second_half)

            if second_avg > first_avg + 2:
                return "总体上升"
            elif second_avg < first_avg - 2:
                return "总体下降"
            else:
                return "波动"

    def calculate_level(self, score):
        """计算成绩等级"""
        if pd.isna(score):
            return "未知"

        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "中等"
        elif score >= 60:
            return "及格"
        else:
            return "不及格"

    def get_exam_detail(self, exam_name):
        """获取指定考试的详细信息"""
        try:
            # 获取考试基本信息
            exam_info = self.db.get_exam_by_name(exam_name)

            if exam_info.empty:
                return None

            # 获取该考试的所有学生成绩
            scores_df = self.db.get_exam_scores(exam_name)

            # 转换为字典格式
            scores_list = []
            for _, row in scores_df.iterrows():
                scores_list.append({
                    'student_id': row['student_id'],
                    'student_name': row['student_name'],
                    'score': row['score'],
                    'record_time': row['record_time']
                })

            return scores_list

        except Exception:
            return None

    def delete_exam(self, exam_name):
        """删除指定的考试"""
        return self.db.delete_exam(exam_name)

    def clear_all_data(self):
        """清空所有数据"""
        return self.db.clear_all_data()

    def cleanup_orphaned_records(self):
        """清理孤立的记录"""
        return self.db.cleanup_orphaned_records()

    def get_all_exams(self):
        """获取所有考试"""
        return self.db.get_all_exams()
