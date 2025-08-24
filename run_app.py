import streamlit.web.cli as stcli
import streamlit.config as _config
import os
import sys

# ==== 1. 环境变量，强制生产模式 ====
os.environ["STREAMLIT_DEVELOPMENT_MODE"] = "0"          # 禁用 dev mode
os.environ["BROWSER"] = "none"                          # 不自动弹浏览器
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"    # 关闭 CORS
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"  # 关闭 XSRF 防护

# ==== 2. Streamlit 配置 ====
_config.set_option("global.developmentMode", False)
_config.set_option("server.headless", True)
_config.set_option("server.port", 8501)
# _config.set_option("server.address", "0.0.0.0")  # 如果需要局域网访问，取消注释

# ==== 3. 自动生成本地 config.toml（防止找不到配置文件） ====
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

# ==== 4. 启动项目 ====

if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(__file__), "app.py")  # 主入口
    sys.argv = ["streamlit", "run", app_path]
    sys.exit(stcli.main())
