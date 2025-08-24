import streamlit.web.cli as stcli
import streamlit.config as _config
import os
import sys

# ==== 1. 生产模式强制设置 ====
# 禁用开发模式（防止 Node Dev Server）
os.environ["STREAMLIT_DEVELOPMENT_MODE"] = "0"

# 禁用浏览器自动打开
os.environ["BROWSER"] = "none"

# 关闭 CORS / XSRF 冲突警告：二选一
# 如果你是本地内网或单机运行，可以直接关掉 XSRF 保护
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"

# ==== 2. 设置 Streamlit 配置 ====

_config.set_option("global.developmentMode", False)  # 关闭 Dev Mode
_config.set_option("server.port", 8501)              # 固定端口
_config.set_option("server.headless", True)          # Headless 模式（不弹浏览器）

# 可选：如果你需要允许外部访问，可以加
# _config.set_option("server.address", "0.0.0.0")

# ==== 3. 启动你的 Streamlit 应用 ====

if __name__ == "__main__":
    # 你的主 app 文件路径（替换成你的实际文件名）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")

    sys.argv = ["streamlit", "run", app_path]
    sys.exit(stcli.main())
