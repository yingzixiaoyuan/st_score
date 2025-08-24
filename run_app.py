import os
import sys
import subprocess

print("=== RUN_APP START ===")
print("sys.executable =", sys.executable)
print("cwd =", os.getcwd())

# 检查 streamlit 是否存在
try:
    import streamlit
    print("Streamlit version:", streamlit.__version__)
except Exception as e:
    print("Import streamlit failed:", repr(e))

# app 路径
app_path = os.path.join(os.path.dirname(__file__), "app.py")
print("App path:", app_path, "exists?", os.path.exists(app_path))

# 环境变量
os.environ["STREAMLIT_DEVELOPMENT_MODE"] = "0"
os.environ["BROWSER"] = "none"

if hasattr(sys, '_MEIPASS'):
    # 用 PyInstaller 打包后的内置 Python 来运行
    python_path = os.path.join(sys._MEIPASS, 'python.exe')
else:
    # 本地调试模式
    python_path = sys.executable

print("Using python interpreter:", python_path)

cmd = [python_path, "-m", "streamlit", "run", app_path,
       "--server.headless=true", "--server.port=8501"]

print("Launching Streamlit with:", cmd)

result = subprocess.run(cmd, capture_output=True, text=True)
print("=== STREAMLIT STDOUT ===")
print(result.stdout)
print("=== STREAMLIT STDERR ===")
print(result.stderr)

print("=== RUN_APP END ===")
input("按回车退出...")
