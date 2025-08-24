import os
import sys
import streamlit.web.bootstrap as bootstrap


def main():
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    if not os.path.exists(app_path):
        print(f"app.py not found at {app_path}")
        sys.exit(1)

    # 运行在无头模式，关闭遥测
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")

    # 确保当前目录在 sys.path 中，便于导入本地模块
    current_dir = os.path.dirname(__file__)
    if current_dir and current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    bootstrap.run(app_path, "", [], {})


if __name__ == "__main__":
    main()
