import os
import sys
from pathlib import Path
import streamlit.web.bootstrap as bootstrap

# 如果是 PyInstaller 打包后的，可执行文件在 _MEIPASS 下
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# 让 Streamlit 默认用打包的静态文件目录（阻止它去找 Node dev server）
os.environ["STREAMLIT_STATIC_FOLDER"] = os.path.join(os.getcwd(), "streamlit", "static")

# 常规配置
os.environ["STREAMLIT_SERVER_PORT"] = "8501"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_ENABLECORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLEXSRFPROTECTION"] = "false"

# app 入口
app_path = str(Path(__file__).parent / "app.py")

# 启动 Streamlit
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
