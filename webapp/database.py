"""
数据库管理模块
负责数据库的初始化、连接和基本操作
"""

import sqlite3
import pandas as pd
# 将数据库文件放置在当前目录下
import os
db_path = os.path.join(os.path.dirname(__file__), "student_scores.db")


class DatabaseManager:
    """数据库管理器"""

    def __init__(self, db_path=db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建班级信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_name TEXT UNIQUE NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建考试信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_name TEXT UNIQUE NOT NULL,
                file_path TEXT NOT NULL,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                student_count INTEGER DEFAULT 0
            )
        ''')

        # 创建学生信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                class_id INTEGER,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 检查是否需要添加 student_id 字段（兼容旧版本）
        try:
            cursor.execute('SELECT student_id FROM students LIMIT 1')
        except sqlite3.OperationalError:
            # 如果 student_id 字段不存在，添加它
            cursor.execute('ALTER TABLE students ADD COLUMN student_id TEXT')
            # 为现有记录设置默认值
            cursor.execute(
                'UPDATE students SET student_id = name '
                'WHERE student_id IS NULL'
            )
            # 添加唯一约束
            cursor.execute(
                'CREATE UNIQUE INDEX IF NOT EXISTS idx_student_id '
                'ON students(student_id)'
            )

        # 兼容旧版本：如果没有 class_id 字段则添加
        try:
            cursor.execute('SELECT class_id FROM students LIMIT 1')
        except sqlite3.OperationalError:
            cursor.execute('ALTER TABLE students ADD COLUMN class_id INTEGER')

        # 创建成绩表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                exam_id INTEGER,
                score REAL NOT NULL,
                record_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (exam_id) REFERENCES exams (id),
                UNIQUE(student_id, exam_id)
            )
        ''')

        conn.commit()
        conn.close()

    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)

    def close_connection(self, conn):
        """关闭数据库连接"""
        if conn:
            conn.close()

    def execute_query(self, query, params=None):
        """执行查询语句"""
        conn = self.get_connection()
        try:
            if params:
                df = pd.read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
            return df
        finally:
            self.close_connection(conn)

    def execute_update(self, query, params=None):
        """执行更新语句"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
        finally:
            self.close_connection(conn)

    def get_all_exams(self):
        """获取所有考试"""
        query = '''
            SELECT
                exam_name,
                upload_time,
                student_count,
                file_path
            FROM exams 
            ORDER BY upload_time DESC
        '''
        return self.execute_query(query)

    # =========================
    # 班级管理 CRUD 方法
    # =========================
    def get_all_classes(self):
        """获取所有班级"""
        query = '''
            SELECT
                id,
                class_name,
                created_time
            FROM classes
            ORDER BY class_name
        '''
        return self.execute_query(query)

    def get_class_by_name(self, class_name):
        """根据名称获取班级"""
        query = 'SELECT * FROM classes WHERE class_name = ?'
        return self.execute_query(query, [class_name])

    def create_class(self, class_name):
        """创建班级"""
        query = 'INSERT OR IGNORE INTO classes (class_name) VALUES (?)'
        return self.execute_update(query, (class_name,))

    def update_class_name(self, class_id, new_name):
        """更新班级名称"""
        query = 'UPDATE classes SET class_name = ? WHERE id = ?'
        return self.execute_update(query, (new_name, class_id))

    def delete_class(self, class_id):
        """删除班级并将所属学生的class_id置空"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE students SET class_id = NULL WHERE class_id = ?',
                (class_id,)
            )
            cursor.execute(
                'DELETE FROM classes WHERE id = ?',
                (class_id,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"删除班级失败: {e}")
            return False
        finally:
            self.close_connection(conn)

    def get_class_student_counts(self):
        """各班学生数量统计"""
        query = '''
            SELECT
                c.id as class_id,
                c.class_name,
                COUNT(s.id) as student_count
            FROM classes c
            LEFT JOIN students s ON s.class_id = c.id
            GROUP BY c.id, c.class_name
            ORDER BY c.class_name
        '''
        return self.execute_query(query)

    # =========================
    # 学生管理 CRUD 方法
    # =========================
    def get_all_students(self):
        """获取所有学生（含班级名）"""
        query = '''
            SELECT
                s.id,
                s.student_id,
                s.name,
                s.class_id,
                c.class_name,
                s.created_time
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            ORDER BY s.created_time DESC
        '''
        return self.execute_query(query)

    def create_student_full(self, student_id_value, name, class_id=None):
        """创建学生，指定学号/姓名/班级"""
        query = (
            'INSERT INTO students (student_id, name, class_id) '
            'VALUES (?, ?, ?)'
        )
        return self.execute_update(
            query,
            (student_id_value, name, class_id)
        )

    def update_student_info(self, student_pk_id, student_id_value, name, class_id=None):
        """更新学生信息"""
        query = (
            'UPDATE students SET student_id = ?, name = ?, class_id = ? '
            'WHERE id = ?'
        )
        return self.execute_update(
            query,
            (student_id_value, name, class_id, student_pk_id)
        )

    def delete_student(self, student_pk_id):
        """删除学生（同时清理其成绩）"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM scores WHERE student_id = ?',
                (student_pk_id,)
            )
            cursor.execute(
                'DELETE FROM students WHERE id = ?',
                (student_pk_id,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"删除学生失败: {e}")
            return False
        finally:
            self.close_connection(conn)

    def get_exam_by_name(self, exam_name):
        """根据名称获取考试信息"""
        query = 'SELECT * FROM exams WHERE exam_name = ?'
        return self.execute_query(query, [exam_name])

    def get_exam_scores(self, exam_name):
        """获取指定考试的所有学生成绩"""
        query = '''
            SELECT
                s.student_id as student_id,
                s.name as student_name,
                sc.score,
                sc.record_time
            FROM scores sc
            JOIN students s ON sc.student_id = s.id
            JOIN exams e ON sc.exam_id = e.id
            WHERE e.exam_name = ?
            ORDER BY sc.score DESC
        '''
        return self.execute_query(query, [exam_name])

    def get_student_scores(self, selected_exams):
        """获取学生成绩数据"""
        if not selected_exams:
            return pd.DataFrame()

        placeholders = ','.join(['?' for _ in selected_exams])
        query = (
            'SELECT s.student_id, s.name, e.exam_name, sc.score '
            'FROM scores sc '
            'JOIN students s ON sc.student_id = s.id '
            'JOIN exams e ON sc.exam_id = e.id '
            f'WHERE e.exam_name IN ({placeholders}) '
            'ORDER BY s.name, e.upload_time'
        )

        return self.execute_query(query, selected_exams)

    # =========================
    # 考试管理（补充手动管理）
    # =========================
    def get_all_exams_full(self):
        """获取所有考试（含id等）"""
        query = (
            'SELECT id, exam_name, file_path, upload_time, student_count '
            'FROM exams ORDER BY upload_time DESC'
        )
        return self.execute_query(query)

    def create_exam_manual(self, exam_name, file_path='', student_count=0):
        """手动创建考试"""
        query = (
            'INSERT INTO exams (exam_name, file_path, student_count) '
            'VALUES (?, ?, ?)'
        )
        return self.execute_update(
            query,
            (exam_name, file_path, student_count)
        )

    def rename_exam(self, exam_id, new_name):
        """重命名考试"""
        query = (
            'UPDATE exams SET exam_name = ?, '
            'upload_time = CURRENT_TIMESTAMP WHERE id = ?'
        )
        return self.execute_update(query, (new_name, exam_id))

    def delete_exam_by_id(self, exam_id):
        """按ID删除考试（含成绩）"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM scores WHERE exam_id = ?',
                (exam_id,)
            )
            cursor.execute(
                'DELETE FROM exams WHERE id = ?',
                (exam_id,)
            )
            conn.commit()
            return True, "删除成功"
        except Exception as e:
            return False, f"删除考试时出现错误：{str(e)}"
        finally:
            self.close_connection(conn)

    # =========================
    # 成绩管理 CRUD 方法
    # =========================
    def get_scores(self, student_pk_id=None, exam_id=None, class_id=None):
        """按条件获取成绩列表"""
        base = '''
            SELECT 
                sc.id as score_id,
                s.id as student_pk_id,
                s.student_id,
                s.name,
                e.id as exam_id,
                e.exam_name,
                sc.score,
                sc.record_time,
                s.class_id
            FROM scores sc
            JOIN students s ON sc.student_id = s.id
            JOIN exams e ON sc.exam_id = e.id
        '''
        conditions = []
        params = []
        if student_pk_id is not None:
            conditions.append('s.id = ?')
            params.append(student_pk_id)
        if exam_id is not None:
            conditions.append('e.id = ?')
            params.append(exam_id)
        if class_id is not None:
            conditions.append('s.class_id = ?')
            params.append(class_id)
        if conditions:
            base += ' WHERE ' + ' AND '.join(conditions)
        base += ' ORDER BY sc.record_time DESC'
        return self.execute_query(base, params if params else None)

    def upsert_score(self, student_pk_id, exam_id, score):
        """新增或更新成绩（按学生+考试唯一）"""
        query = '''
            INSERT OR REPLACE INTO scores (student_id, exam_id, score)
            VALUES (?, ?, ?)
        '''
        return self.execute_update(
            query,
            (int(student_pk_id), int(exam_id), float(score))
        )

    def delete_score(self, score_id=None, student_pk_id=None, exam_id=None):
        """删除成绩（支持按score_id或学生+考试对删除）"""
        if score_id is not None:
            query = 'DELETE FROM scores WHERE id = ?'
            return self.execute_update(query, (score_id,))
        if student_pk_id is not None and exam_id is not None:
            query = 'DELETE FROM scores WHERE student_id = ? AND exam_id = ?'
            return self.execute_update(query, (student_pk_id, exam_id))
        raise ValueError('必须提供 score_id 或 (student_pk_id, exam_id)')

    def update_exam_info(self, exam_id, file_path, student_count):
        """更新考试信息"""
        try:
            query = (
                'UPDATE exams SET file_path = ?, student_count = ?, '
                'upload_time = CURRENT_TIMESTAMP WHERE id = ?'
            )
            result = self.execute_update(
                query,
                (file_path, student_count, exam_id)
            )
            return result is not None
        except Exception as e:
            print(f"更新考试信息失败: {e}")
            return False

    def insert_new_exam(self, exam_name, file_path, student_count):
        """插入新的考试信息"""
        try:
            query = '''
                INSERT INTO exams (exam_name, file_path, student_count)
                VALUES (?, ?, ?)
            '''
            exam_id = self.execute_update(
                query,
                (exam_name, file_path, student_count)
            )

            if exam_id:
                print(f"考试 '{exam_name}' 插入成功，ID: {exam_id}")
                return exam_id
            else:
                print(f"考试 '{exam_name}' 插入失败")
                return None

        except Exception as e:
            print(f"插入考试信息失败: {e}")
            return None

    def insert_exam(self, exam_name, file_path, student_count):
        """插入考试信息"""
        try:
            # 先检查是否已存在同名考试
            existing_exam = self.get_exam_by_name(exam_name)
            if not existing_exam.empty:
                print(f"警告：考试 '{exam_name}' 已存在，将更新信息")
                # 更新现有考试信息，而不是删除重插
                exam_id = existing_exam.iloc[0]['id']
                query = (
                    'UPDATE exams SET file_path = ?, student_count = ?, '
                    'upload_time = CURRENT_TIMESTAMP WHERE id = ?'
                )
                self.execute_update(
                    query,
                    (file_path, student_count, exam_id)
                )
                print(f"考试 '{exam_name}' 更新成功，ID: {exam_id}")
                return exam_id

            # 插入新的考试信息
            query = '''
                INSERT INTO exams (exam_name, file_path, student_count)
                VALUES (?, ?, ?)
            '''
            exam_id = self.execute_update(
                query,
                (exam_name, file_path, student_count)
            )

            if exam_id:
                print(f"考试 '{exam_name}' 插入成功，ID: {exam_id}")
                return exam_id
            else:
                print(f"考试 '{exam_name}' 插入失败")
                return None

        except Exception as e:
            print(f"插入考试信息失败: {e}")
            return None

    def insert_student(self, name):
        """插入学生信息（兼容旧版本）"""
        query = (
            'INSERT OR IGNORE INTO students (student_id, name) '
            'VALUES (?, ?)'
        )
        return self.execute_update(query, (name, name))

    def insert_student_with_id(self, name, student_id):
        """插入学生信息（使用学号）"""
        try:
            # 先检查是否已存在
            existing_id = self.get_student_id_by_student_id(student_id)
            if existing_id:
                return existing_id

            # 如果不存在，则插入
            query = 'INSERT INTO students (student_id, name) VALUES (?, ?)'
            return self.execute_update(query, (student_id, name))
        except Exception as e:
            print(f"插入学生信息失败: {e}")
            return None

    def get_student_id(self, name):
        """获取学生ID（兼容旧版本）"""
        query = 'SELECT id FROM students WHERE name = ?'
        df = self.execute_query(query, [name])
        if not df.empty:
            return df.iloc[0]['id']
        return None

    def get_student_id_by_student_id(self, student_id):
        """根据学号获取学生ID"""
        query = 'SELECT id FROM students WHERE student_id = ?'
        df = self.execute_query(query, [student_id])
        if not df.empty:
            return df.iloc[0]['id']
        return None

    def insert_score(self, student_id, exam_id, score):
        """插入成绩信息"""
        try:
            # 验证参数
            if student_id is None or exam_id is None or score is None:
                print(
                    f"插入成绩失败：参数无效 student_id={student_id}, "
                    f"exam_id={exam_id}, score={score}"
                )
                return None

            # 确保ID参数是Python原生类型（修复numpy类型兼容性问题）
            student_id = int(student_id)
            exam_id = int(exam_id)

            # 检查学生是否存在
            student_exists = self.execute_query(
                "SELECT id FROM students WHERE id = ?", [student_id]
            )
            if student_exists.empty:
                print(f"插入成绩失败：学生ID {student_id} 不存在")
                return None

            # 检查考试是否存在
            exam_exists = self.execute_query(
                "SELECT id FROM exams WHERE id = ?", [exam_id]
            )
            if exam_exists.empty:
                print(f"插入成绩失败：考试ID {exam_id} 不存在")
                return None

            # 插入成绩
            query = '''
                INSERT OR REPLACE INTO scores (student_id, exam_id, score)
                VALUES (?, ?, ?)
            '''
            return self.execute_update(query, (student_id, exam_id, score))
        except Exception as e:
            print(f"插入成绩失败: {e}")
            return None

    def delete_exam(self, exam_name):
        """删除指定的考试"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 获取考试ID
            cursor.execute(
                'SELECT id FROM exams WHERE exam_name = ?',
                (exam_name,)
            )
            exam_result = cursor.fetchone()

            if not exam_result:
                return False, f"考试 '{exam_name}' 不存在"

            exam_id = exam_result[0]

            # 删除相关的成绩记录
            cursor.execute(
                'DELETE FROM scores WHERE exam_id = ?',
                (exam_id,)
            )

            # 删除考试记录
            cursor.execute(
                'DELETE FROM exams WHERE id = ?',
                (exam_id,)
            )

            # 注意：不再自动删除学生记录，保持学生信息的完整性
            # 学生可能只是暂时没有成绩，不应该被删除

            conn.commit()
            return True, f"考试 '{exam_name}' 已成功删除"
        except Exception as e:
            return False, f"删除考试时出现错误：{str(e)}"
        finally:
            self.close_connection(conn)

    def clear_all_data(self):
        """清空所有数据"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 清空所有表
            cursor.execute("DELETE FROM scores")
            cursor.execute("DELETE FROM exams")
            cursor.execute("DELETE FROM students")

            # 重置自增ID
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name IN ('scores', "
                "'exams', 'students')"
            )

            conn.commit()
            return True, "所有数据已清空"
        except Exception as e:
            return False, f"清空数据时出现错误：{str(e)}"
        finally:
            self.close_connection(conn)

    def cleanup_orphaned_records(self):
        """清理孤立的记录"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 清理没有对应考试的分数记录
            cursor.execute("""
                DELETE FROM scores
                WHERE exam_id NOT IN (SELECT id FROM exams)
            """)
            orphaned_scores = cursor.rowcount

            # 清理没有对应学生的分数记录
            cursor.execute("""
                DELETE FROM scores
                WHERE student_id NOT IN (SELECT id FROM students)
            """)
            orphaned_students = cursor.rowcount

            # 清理没有成绩记录的学生
            cursor.execute("""
                DELETE FROM students
                WHERE id NOT IN (SELECT DISTINCT student_id FROM scores)
            """)
            orphaned_students_cleanup = cursor.rowcount

            conn.commit()
            return True, (
                f"清理完成：孤立分数记录 {orphaned_scores} 条，"
                f"缺失学生关联分数记录 {orphaned_students} 条，"
                f"孤立学生记录 {orphaned_students_cleanup} 条"
            )

        except Exception as e:
            return False, f"清理孤立记录时出现错误：{str(e)}"
        finally:
            self.close_connection(conn)
