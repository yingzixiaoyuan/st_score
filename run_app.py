import os
import sys

# ==============================
# 1. 环境变量 —— 在导入任何 streamlit 之前就设置！
# ==============================
os.environ["STREAMLIT_DEVELOPMENT_MODE"] = "0"      # 禁用开发模式
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["BROWSER"] = "none"                      # 不自动打开浏览器
# 关闭跨域 & XSRF（单机运行可关）
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
# 劫持 CLI 启动方式（防止 dev mode 自动开启）
os.environ["STREAMLIT_ENV"] = "production"
os.environ["PYTHONWARNINGS"] = "ignore"

# ==============================
# 2. Streamlit 配置（此时才可以安全导入）
# ==============================
import streamlit.config as _config
_config.set_option("global.developmentMode", False)  # 防御性设置
_config.set_option("server.headless", True)
_config.set_option("server.port", 8501)
# _config.set_option("server.address", "0.0.0.0")    # 如果需要局域网访问，取消注释

# 自动生成配置文件（防止找不到 ~/.streamlit）
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

# ==============================
# 3. CLI 启动 app.py
# ==============================
import streamlit.web.cli as stcli

if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    sys.argv = ["streamlit", "run", app_path, "--server.headless=true", "--server.port=8501"]
    sys.exit(stcli.main())
