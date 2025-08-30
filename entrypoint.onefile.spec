# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

# 获取项目根目录
project_root = Path.cwd()

# 数据文件配置
datas = [
    # 包含webapp模块的所有Python文件
    (str(project_root / 'webapp'), 'webapp'),
    # 包含config目录
    (str(project_root / 'config'), 'config'),
    # 包含hooks目录  
    (str(project_root / 'hooks'), 'hooks'),
]

# 隐藏导入配置
hiddenimports = [
    'streamlit',
    'streamlit.web.cli',
    'pydantic_settings',
    'pandas',
    'plotly',
    'openpyxl',
    'numpy',
    'sqlite3',
    'webapp.database',
    'webapp.analyzer',
    'webapp.config',
    'webapp.styles',
    'webapp.pages',
    'webapp.pages.data_import',
    'webapp.pages.exam_analysis', 
    'webapp.pages.data_history',
    'webapp.pages.color_settings',
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
    excludes=[],
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
    name='entrypoint',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 在桌面应用中隐藏控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=(
        'build_assets/icon.ico' if sys.platform.startswith('win') and (project_root / 'build_assets' / 'icon.ico').exists()
        else 'build_assets/icon.icns' if (project_root / 'build_assets' / 'icon.icns').exists()
        else None
    ),
)
