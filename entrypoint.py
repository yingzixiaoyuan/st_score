import sys
from pathlib import Path

import streamlit.web.cli as stcli
from pydantic_settings import BaseSettings


class StreamlitConfig(BaseSettings):
    browser_server_address: str = "localhost"


def resolve_path(path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", str(Path.cwd()))
    return str(Path(base_path) / path)


if __name__ == "__main__":
    config = StreamlitConfig()
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("webapp/app.py"),
        f"--browser.serverAddress={config.browser_server_address}",
        "--browser.gatherUsageStats=false",
        "--client.showSidebarNavigation=false",
        "--client.toolbarMode=viewer",
        "--global.developmentMode=false",
        "--server.headless=true",
    ]
    sys.exit(stcli.main())


# import os
# import sys
# from pathlib import Path
# import json

# # 添加项目根目录到Python路径，以便能导入webapp模块
# sys.path.append(str(Path(__file__).parent.parent))

# from webapp.database import DatabaseManager

# os.environ["STREAMLIT_DEVELOP_MODE"] = "false"
# os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"  # 无需打开浏览器
# os.environ["STREAMLIT_SERVER_PORT"] = "8501"     # 可修改端口


# def resolve_path(path: str) -> str:
#     base_path = getattr(sys, "_MEIPASS", os.getcwd())
#     return str(Path(base_path) / path)


# def ensure_database_exists() -> None:
#     """服务启动时确保数据库文件存在，不存在则创建并初始化表结构。"""
#     db_path = "student_scores.db"
#     if not os.path.exists(db_path):
#         # 确保目录存在
#         Path(db_path).parent.mkdir(parents=True, exist_ok=True)
#         # 创建并初始化数据库
#         DatabaseManager(db_path=db_path)


# def ensure_config_exists() -> None:
#     """服务启动时确保 config 目录与默认配置文件存在。"""
#     config_dir = "config"
#     Path(config_dir).mkdir(parents=True, exist_ok=True)

#     color_settings_path = Path(config_dir) / "color_settings.json"
#     if not color_settings_path.exists():
#         default_colors = {
#             "优秀": {
#                 "min_score": 90,
#                 "max_score": 150,
#                 "color": "#90EE90",
#                 "description": "90分及以上",
#             },
#             "良好": {
#                 "min_score": 80,
#                 "max_score": 89,
#                 "color": "#87CEEB",
#                 "description": "80-89分",
#             },
#             "中等": {
#                 "min_score": 70,
#                 "max_score": 79,
#                 "color": "#F0E68C",
#                 "description": "70-79分",
#             },
#             "及格": {
#                 "min_score": 60,
#                 "max_score": 69,
#                 "color": "#FFB6C1",
#                 "description": "60-69分",
#             },
#             "不及格": {
#                 "min_score": 0,
#                 "max_score": 59,
#                 "color": "#FFA07A",
#                 "description": "60分以下",
#             },
#         }
#         with open(color_settings_path, "w", encoding="utf-8") as f:
#             json.dump(default_colors, f, indent=2, ensure_ascii=False)


# if __name__ == "__main__":
#     # 启动前检查数据库是否存在，不存在则创建
#     ensure_database_exists()
#     # 启动前检查 config 目录和默认配置
#     ensure_config_exists()
#     import streamlit.web.cli as stcli
#     sys.argv = [
#         "streamlit",
#         "run",
#         resolve_path("app.py"),
#         "--global.developmentMode=false",
#         "--server.headless=true",
#     ]
#     sys.exit(stcli.main())
