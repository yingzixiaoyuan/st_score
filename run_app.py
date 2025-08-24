import sys
import os
import streamlit.web.cli as stcli

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    sys.argv = ["streamlit", "run", app_path, "--server.headless=true", "--server.port=8501"]
    sys.exit(stcli.main())
