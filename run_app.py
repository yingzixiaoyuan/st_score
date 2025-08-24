# run_app.py
import sys
import os
import streamlit.web.cli as stcli

if __name__ == '__main__':
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # app.py 必须是你自己的主应用
    app_path = os.path.join(current_dir, "app.py")

    # 设置 streamlit 启动参数
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.address=127.0.0.1",  # 本地运行
        "--server.port=8501",          # 指定端口
        "--server.headless=true"       # 允许无浏览器环境运行
    ]

    # 启动 streamlit
    sys.exit(stcli.main())
