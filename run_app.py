import sys
import os
import time
import threading
import webbrowser
import streamlit.web.cli as stcli


def open_browser():
    """
    延时打开默认浏览器。
    不绑定 IP，让 Streamlit 按默认配置启动。
    """
    time.sleep(2)  # 等待 server 启动
    webbrowser.open("http://localhost:8501")


if __name__ == '__main__':
    # 当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 你的主应用
    app_path = os.path.join(current_dir, "app.py")

    # 浏览器自动打开线程（不阻塞主程序）
    threading.Thread(target=open_browser, daemon=True).start()

    # 不绑定 IP，不强制端口，可以按需改
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.headless=true"
    ]

    # 启动 streamlit
    sys.exit(stcli.main())
