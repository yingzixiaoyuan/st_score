import sys
import os
import streamlit.config as _config
import streamlit.web.cli as stcli

if __name__ == "__main__":
    # 强制关闭开发模式
    _config.set_option("global.developmentMode", False)

    # 设置服务器端口和 headless
    _config.set_option("server.port", 8501)
    _config.set_option("server.headless", True)

    # 定位你的 Streamlit app
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")

    # 等价于: streamlit run app.py
    sys.argv = ["streamlit", "run", app_path]
    sys.exit(stcli.main())
