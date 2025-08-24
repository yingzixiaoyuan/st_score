import os
import sys
import subprocess

print("=== RUN_APP START ===")
print("sys.executable =", sys.executable)
print("cwd =", os.getcwd())

try:
    import streamlit
    print("Streamlit version:", streamlit.__version__)
except Exception as e:
    print("Import streamlit failed:", e)

app_path = os.path.join(os.path.dirname(__file__), "app.py")
print("App path:", app_path, "exists?", os.path.exists(app_path))

# 配置环境变量
os.environ["STREAMLIT_DEVELOPMENT_MODE"] = "0"
os.environ["STREAMLIT_ENV"] = "production"
os.environ["BROWSER"] = "none"
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# 配置文件
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

cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.headless=true", "--server.port=8501"]
print("Launching Streamlit with:", cmd)

result = subprocess.run(cmd, capture_output=True, text=True)
print("=== STREAMLIT STDOUT ===")
print(result.stdout)
print("=== STREAMLIT STDERR ===")
print(result.stderr)

print("=== RUN_APP END ===")
