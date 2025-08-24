"""
配置文件
包含数据库表名、配色方案等常量配置
"""

# 数据库表名
DATABASE_TABLES = {
    'EXAMS': 'exams',
    'STUDENT_SCORES': 'student_scores'
}

# 配色方案
COLOR_SCHEME = {
    'PRIMARY': '#1f77b4',      # 主色调 - 蓝色
    'SECONDARY': '#ff7f0e',    # 次要色调 - 橙色
    'SUCCESS': '#2ca02c',      # 成功色 - 绿色
    'WARNING': '#d62728',      # 警告色 - 红色
    'INFO': '#9467bd',         # 信息色 - 紫色
    'LIGHT': '#f7f7f7',        # 浅色背景
    'DARK': '#2f2f2f',         # 深色文字
    'BORDER': '#e0e0e0'        # 边框色
}

# 成绩等级配置
GRADE_CONFIG = {
    'EXCELLENT': {'min': 90, 'max': 100, 'name': '优秀', 'color': '#2ca02c'},
    'GOOD': {'min': 80, 'max': 89, 'name': '良好', 'color': '#1f77b4'},
    'AVERAGE': {'min': 70, 'max': 79, 'name': '中等', 'color': '#ff7f0e'},
    'PASS': {'min': 60, 'max': 69, 'name': '及格', 'color': '#9467bd'},
    'FAIL': {'min': 0, 'max': 59, 'name': '不及格', 'color': '#d62728'}
}

# 趋势配置
TREND_CONFIG = {
    'IMPROVED': {'name': '进步', 'color': '#2ca02c'},
    'STABLE': {'name': '稳定', 'color': '#1f77b4'},
    'DECLINED': {'name': '下降', 'color': '#d62728'}
}

# 页面配置
PAGE_CONFIG = {
    'OPTIONS': ["📁 数据导入", "📝 考试分析", "📚 数据历史", "🎨 颜色设置"],
    'DEFAULT': "📁 数据导入"
}

# 文件上传配置
UPLOAD_CONFIG = {
    'ALLOWED_TYPES': ['xlsx', 'xls'],
    'MAX_FILE_SIZE': 50 * 1024 * 1024,  # 50MB
    'HELP_TEXT': "可以同时选择多个Excel文件，每个文件代表一次考试"
}

# 表格配置
TABLE_CONFIG = {
    'PAGE_SIZE': 20,
    'MAX_ROWS': 1000,
    'DEFAULT_COLUMN_WIDTH': 'medium'
}

