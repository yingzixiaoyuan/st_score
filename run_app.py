import os
import sys
import subprocess

# ===== 1. 确保执行前是生产模式 =====
os.environ["STREAMLIT_DEVELOPMENT_MODE"] = "0"
os.environ["STREAMLIT_ENV"] = "production"
os.environ["BROWSER"] = "none"

# 关闭 CORS / XSRF
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# ===== 2. 自动写 config.toml =====
config_dir = os.path.join(os.path.expanduser("~"), ".streamlit")
os.makedirs(config_dir, exist_ok=True)
with open(os.path.join(config_dir, "config.toml"), "w", encoding="utf-8") as f:
    f.write("""
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
""")

# ===== 3. 用子进程启动 streamlit CLI =====
if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.headless=true",
        "--server.port=8501"
    ]
    sys.exit(subprocess.call(cmd))
