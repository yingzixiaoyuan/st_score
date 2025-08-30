# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

# 获取项目根目录
project_root = Path.cwd()

# 数据文件配置 - 更全面的打包
datas = [
    # 包含webapp模块的所有Python文件
    (str(project_root / 'webapp'), 'webapp'),
    # 包含config目录
    (str(project_root / 'config'), 'config'),
    # 包含hooks目录  
    (str(project_root / 'hooks'), 'hooks'),
]

# 更完整的隐藏导入配置
hiddenimports = [
    # Streamlit核心
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.state',
    'streamlit.components.v1.components',
    'pydantic_settings',
    # 数据处理
    'pandas',
    'plotly',
    'plotly.graph_objs',
    'plotly.express',
    'openpyxl',
    'openpyxl.styles',
    'numpy',
    'sqlite3',
    # 项目模块
    'webapp.database',
    'webapp.analyzer', 
    'webapp.config',
    'webapp.styles',
    'webapp.pages',
    'webapp.pages.data_import',
    'webapp.pages.exam_analysis', 
    'webapp.pages.data_history',
    'webapp.pages.color_settings',
    # Streamlit依赖
    'tornado',
    'tornado.web',
    'tornado.websocket',
    'altair',
    'click',
    'toml',
    'typing_extensions',
    'packaging',
    'pillow',
    'PIL',
    'PIL.Image',
]

# 分析配置
a = Analysis(
    ['entrypoint.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib'],  # 排除不需要的模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='学生成绩分析器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # macOS .app 包通常不显示控制台
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='build_assets/icon.icns' if (project_root / 'build_assets' / 'icon.icns').exists() else None,
)

# 创建 .app 包
app = BUNDLE(
    exe,
    name='学生成绩分析器.app',
    icon='build_assets/icon.icns' if (project_root / 'build_assets' / 'icon.icns').exists() else None,
    bundle_identifier='com.student.score.analyzer',
    version='1.0.0',
    info_plist={
        'CFBundleDisplayName': '学生成绩分析器',
        'CFBundleName': '学生成绩分析器',
        'CFBundleIdentifier': 'com.student.score.analyzer',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.14.0',  # macOS Mojave
        'NSRequiresAquaSystemAppearance': False,  # 支持深色模式
    }
)
