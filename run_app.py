import os
import sys
from pathlib import Path
import streamlit.web.bootstrap as bootstrap

# ==== 打包后资源路径修正 ====
if getattr(sys, 'frozen', False):  # 如果是打包成 exe
    os.chdir(sys._MEIPASS)

# ==== Streamlit 运行配置 ====
os.environ["STREAMLIT_SERVER_PORT"] = "8501"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_ENABLECORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLEXSRFPROTECTION"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# ==== 指定静态资源目录（关键） ====
build_dir = Path(os.getcwd()) / "streamlit" / "frontend" / "build"
if build_dir.exists():
    os.environ["STREAMLIT_STATIC_FOLDER"] = str(build_dir)

# ==== 你的 Streamlit 应用入口 ====
app_path = str(Path(__file__).parent / "app.py")

# ==== 启动 ====
bootstrap.run(
    app_path,
    [],
    {},
    flag_options={
        "server.port": 8501,
        "server.headless": True,
        "server.enableCORS": False,
        "server.enableXsrfProtection": False
    }
)
