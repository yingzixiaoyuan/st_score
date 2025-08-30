# 📊 学生成绩分析器桌面应用

基于Tauri和Streamlit构建的跨平台学生成绩分析桌面应用程序。

## ✨ 功能特性

- 📊 **数据导入分析**: 支持Excel文件导入，自动解析学生成绩数据
- 📈 **多维度统计**: 提供丰富的图表展示，包括分数分布、趋势分析等
- 🎨 **自定义配置**: 支持颜色主题设置，个性化界面显示
- 📚 **历史管理**: 完整的数据历史记录，方便追踪和对比
- 🖥️ **原生桌面应用**: 基于Tauri构建，启动快速，资源占用低
- 🌐 **内置Web界面**: 集成Streamlit应用，提供直观的操作界面

## 🔧 技术架构

- **前端**: Tauri 2.0 + TypeScript + Vite
- **后端**: Python 3.11 + Streamlit + SQLite
- **打包**: 跨平台原生应用，无需浏览器依赖
- **构建系统**: GitHub Actions自动化CI/CD + UV包管理器
- **配置管理**: 现代化pyproject.toml + 平台特定Tauri配置

## 🚀 快速开始

### 前提条件

- Python 3.11+
- Node.js 18+
- pnpm
- Rust (最新稳定版)
- **UV** (推荐，用于更快的依赖管理)

### 安装UV (推荐)

```bash
# 安装UV - 最快的Python包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或者使用pip
pip install uv
```

### 安装依赖

**使用UV (推荐 - 速度提升10倍):**
```bash
# 设置Python环境
uv python install
uv venv
uv sync --all-extras --group build

# 安装Tauri前端依赖
cd tauri
pnpm install
```

**传统方法:**
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Tauri前端依赖
cd tauri
pnpm install
```

### 开发运行

```bash
# 启动开发模式
cd tauri
pnpm tauri dev
```

### 生成图标

```bash
# 生成所有平台图标（ASCII兼容版本）
python3 build_assets/universal_icon_generator_ascii.py
```

### 构建发布版本

```bash
# 构建所有平台
cd tauri
pnpm tauri build
```

## 🏗️ 现代化开发工作流

### 项目配置

项目使用现代Python打包标准 `pyproject.toml`：

```toml
[project]
name = "student-score-analyzer"
version = "0.1.0"  # 版本号统一管理
dependencies = [
    "streamlit>=1.28.0",
    "pandas>=2.0.0",
    "plotly",
    "openpyxl",
    "numpy",
    "pydantic-settings",
    "Pillow",
]

[project.optional-dependencies]
build = ["pyinstaller>=6.0.0"]
```

### 平台特定Tauri配置

```
tauri/src-tauri/
├── tauri.conf.json           # 主配置
├── tauri.linux.conf.json    # Linux特定: deb + appimage  
└── tauri.windows.conf.json  # Windows特定: nsis + msi
```

### 自动变更日志生成

使用 `git-cliff` 基于规范化提交自动生成变更日志：

```bash
# 安装git-cliff
pip install git-cliff

# 生成变更日志
git cliff --latest > CHANGELOG.md
```

## 📁 项目结构

```
st_score/
├── .github/workflows/              # GitHub Actions工作流
│   ├── build-release.yml              # 主要Tauri桌面应用构建
│   ├── build-release-optimized.yml    # 优化构建（使用UV）
│   ├── build-pyinstaller.yml          # PyInstaller构建
│   └── build-windows-exe.yml          # Windows专用构建
├── webapp/                         # Streamlit应用源码
│   ├── pages/                     # Streamlit页面模块
│   │   ├── color_settings.py     # 颜色设置页面
│   │   ├── data_history.py       # 数据历史页面
│   │   ├── data_import.py         # 数据导入页面
│   │   └── exam_analysis.py       # 考试分析页面
│   ├── app.py                    # 主应用程序
│   ├── analyzer.py               # 成绩分析器
│   ├── database.py               # 数据库管理
│   ├── config.py                 # 配置管理
│   └── styles.py                 # 样式定义
├── tauri/                          # Tauri桌面应用
│   ├── src-tauri/                 # Rust后端代码
│   │   ├── tauri.conf.json           # 主Tauri配置
│   │   ├── tauri.linux.conf.json     # Linux特定配置
│   │   ├── tauri.windows.conf.json   # Windows特定配置
│   │   ├── Cargo.toml                # Rust依赖
│   │   └── src/
│   │       ├── main.rs               # Rust入口
│   │       └── lib.rs                # 库文件
│   ├── src/                      # TypeScript前端源码
│   │   └── main.ts               # TypeScript入口
│   ├── public/                   # 静态资源
│   │   ├── splashscreen.html     # 启动画面
│   │   └── styles.css            # 样式文件
│   ├── index.html                # 主HTML文件
│   └── package.json              # 前端依赖
├── build_assets/                   # 构建资源和图标
│   ├── universal_icon_generator_ascii.py  # ASCII兼容图标生成器
│   └── icon*.*                   # 各种格式的应用图标
├── config/                         # 配置文件
│   └── color_settings.json       # 颜色配置
├── hooks/                          # PyInstaller钩子文件
│   └── hook-streamlit.py         # Streamlit钩子
├── entrypoint.py                  # Python应用入口
├── entrypoint*.spec               # PyInstaller配置文件
├── pyproject.toml                 # 现代Python项目配置
├── cliff.toml                     # 变更日志生成配置
├── requirements.txt               # Python依赖（兼容性）
└── README.md                      # 本文件
```

## 📦 构建和发布选项

本项目提供多种构建方式，满足不同的使用需求：

### 🖥️ Tauri桌面应用版本 (推荐)

**特点**:
- ✨ **原生桌面应用**: 真正的桌面应用体验
- 🚀 **启动速度快**: Rust + Tauri 框架，性能优异
- 🎨 **美观界面**: 自定义启动画面和应用图标
- 💾 **资源占用少**: 比Electron应用更轻量
- 📦 **标准安装包**: 提供各平台的标准安装程序

**发布命令**:
```bash
# 传统方法
git tag v1.0.0
git push origin v1.0.0

# 现代化方法（推荐）
# 1. 更新pyproject.toml中的版本号
# 2. 使用规范化提交
git commit -m "feat: 添加新的分析功能"
git tag v1.0.0
git push origin v1.0.0
```

**构建产物**:
- **Windows**: `.exe`安装包和`.msi`文件
- **macOS**: `.dmg`磁盘映像文件
- **Linux**: `.deb`包和`.AppImage`文件

### 💻 PyInstaller简化版本

**特点**:
- 🔧 **简单部署**: 纯Python可执行文件
- 📁 **绿色软件**: 无需安装，解压即用
- 🖥️ **控制台输出**: 显示运行日志，方便调试
- 🌐 **浏览器访问**: 启动后在浏览器中使用

**发布命令**:
```bash
# 推送到pyinstaller分支进行构建
git checkout -b pyinstaller
git push origin pyinstaller

# 或创建PyInstaller版本标签
git tag py-v1.0.0
git push origin py-v1.0.0
```

**构建产物**:
- **Windows**: `.zip`压缩包（含可执行文件）
- **macOS**: `.tar.gz`压缩包
- **Linux**: 单个可执行文件

### 🔄 版本对比

| 特性 | Tauri版本 | PyInstaller版本 |
|------|-----------|-----------------|
| 用户体验 | ⭐⭐⭐⭐⭐ 原生桌面应用 | ⭐⭐⭐ 控制台+浏览器 |
| 安装体验 | ⭐⭐⭐⭐⭐ 标准安装程序 | ⭐⭐ 手动解压 |
| 启动速度 | ⭐⭐⭐⭐⭐ 极快 | ⭐⭐⭐ 中等 |
| 资源占用 | ⭐⭐⭐⭐ 较低 | ⭐⭐⭐ 中等 |
| 部署复杂度 | ⭐⭐ 需安装 | ⭐⭐⭐⭐⭐ 绿色软件 |
| 调试便利性 | ⭐⭐ 隐藏日志 | ⭐⭐⭐⭐⭐ 显示日志 |

## 🎯 使用方法

1. 下载对应平台的安装包
2. 安装并启动应用程序
3. 等待启动画面加载完成
4. 应用会自动打开内置的Web界面
5. 开始导入和分析学生成绩数据

## 📊 GitHub Actions 工作流

### 可用工作流

1. **`build-release-optimized.yml`** - 现代化Tauri构建（推荐）
   - **触发器**: 推送 `v*.*.*` 标签或 `main`/`release` 分支
   - **特性**: 
     - UV包管理器，构建速度提升10倍
     - 使用git-cliff自动生成变更日志
     - 平台特定配置
     - 跨平台工件生成
   - **输出**: `.exe`, `.msi`, `.dmg`, `.deb`, `.AppImage`

2. **`build-release.yml`** - 传统Tauri构建
   - **触发器**: 推送 `v*.*.*` 标签或 `release` 分支  
   - **特性**: 传统pip依赖管理
   - **输出**: 与优化版本相同

3. **`build-pyinstaller.yml`** - PyInstaller简单构建
   - **触发器**: 推送 `py-v*.*.*` 标签或 `pyinstaller` 分支
   - **特性**: 跨平台可执行文件
   - **输出**: 独立可执行程序

4. **`build-windows-exe.yml`** - Windows专用构建
   - **触发器**: 推送 `release` 分支或手动触发
   - **输出**: Windows可执行文件

### 性能对比

| 工作流 | 依赖安装时间 | 总构建时间 | 特性评价 |
|----------|------------------------|------------------|----------|
| **优化版 (UV)** | ~30-60秒 | ~8-12分钟 | ⭐⭐⭐⭐⭐ 现代化、快速 |
| **传统版 (pip)** | ~2-3分钟 | ~12-18分钟 | ⭐⭐⭐ 传统、稳定 |
| **PyInstaller** | ~2-3分钟 | ~10-15分钟 | ⭐⭐⭐ 简单、实用 |

### 推荐用法

- **开发调试**: 使用优化工作流获得最快反馈
- **正式发布**: 使用优化工作流发布版本  
- **问题排查**: 使用PyInstaller版本查看控制台输出

## 🔄 发布流程

### 现代化发布流程

**1. 更新pyproject.toml中的版本**
```toml
[project]
version = "1.0.0"  # 更新这里
```

**2. 使用规范化提交**
```bash
# 使用规范化提交格式自动生成变更日志
git add .
git commit -m "feat: 添加新的分析功能

- 添加高级分数分布图表
- 实现趋势分析算法
- 优化用户界面体验"
```

**3. 创建发布**
```bash
# 推送到main分支（触发测试构建）
git push origin main

# 创建并推送标签（触发正式发布）
git tag v1.0.0
git push origin v1.0.0
```

**4. 自动化流程**
- GitHub Actions自动构建所有平台
- 从提交历史生成变更日志
- 创建Release并附加所有工件
- 从pyproject.toml提取版本信息

### PyInstaller版本发布

```bash
# 1. 创建或切换到pyinstaller分支
git checkout -b pyinstaller

# 2. 提交更改
git add .
git commit -m "Release PyInstaller v1.0.0"

# 3. 创建并推送标签
git tag py-v1.0.0
git push origin pyinstaller
git push origin py-v1.0.0

# 4. GitHub Actions 会自动构建并创建Release
```

## 🍎 macOS 构建说明

### 三种macOS构建方式

1. **简单可执行文件**
   ```bash
   pyinstaller entrypoint.pyinstaller.onefile.spec
   ```
   - ✅ 文件小，启动快
   - ❌ 需要在终端中运行

2. **macOS应用包 (.app)**
   ```bash
   pyinstaller entrypoint.macos.app.spec
   ```
   - ✅ 可以双击启动
   - ✅ 显示在应用程序列表中
   - ✅ 可以拖拽到Applications文件夹

3. **Tauri桌面应用 (推荐)**
   ```bash
   cd tauri && pnpm tauri build
   ```
   - ✅ 专业的安装体验
   - ✅ 启动画面和图标
   - ✅ 更小的文件大小

### macOS构建步骤

```bash
# 生成所有图标
python3 build_assets/universal_icon_generator_ascii.py

# 清理之前的构建
rm -rf dist build

# 构建 .app 包
pyinstaller --noconfirm entrypoint.macos.app.spec

# 测试应用
open dist/学生成绩分析器.app
```

## 🔧 手动触发构建

### 通过 GitHub Web界面
1. 进入项目的 GitHub 页面
2. 点击 "Actions" 标签
3. 选择对应的工作流
4. 点击 "Run workflow" 按钮

### 通过 GitHub CLI
```bash
# 触发优化Tauri构建
gh workflow run build-release-optimized.yml

# 触发传统Tauri构建
gh workflow run build-release.yml

# 触发PyInstaller构建
gh workflow run build-pyinstaller.yml -f create_release=true
```

## 🎨 跨平台兼容性

### ASCII兼容图标生成

项目使用ASCII兼容的图标生成器确保Windows兼容性：

```bash
# 生成跨平台兼容的图标
python3 build_assets/universal_icon_generator_ascii.py
```

**优势:**
- ✅ Windows无Unicode编码错误
- ✅ 跨平台控制台输出兼容性  
- ✅ GitHub Actions Windows构建支持
- ✅ 生成所有需要的格式: ICO、ICNS、PNG

## 🐛 故障排除

### 构建失败常见原因

**1. UV安装问题**
```bash
# 如果找不到UV，安装它：
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或使用pip回退
pip install uv
```

**2. Unicode错误 (Windows)**
- ✅ **已解决**: 项目使用纯ASCII输出
- 使用 `universal_icon_generator_ascii.py` 而不是Unicode版本

**3. Tauri构建失败**
```bash
# 确保所有平台配置存在：
ls tauri/src-tauri/tauri*.conf.json

# 如果图标丢失，重新生成：
python3 build_assets/universal_icon_generator_ascii.py
```

**4. 依赖冲突**
```bash
# 使用UV清理并重新安装：
rm -rf .venv
uv venv
uv sync --all-extras --group build
```

**5. Python依赖问题**
   - 检查 `requirements.txt` 是否包含所有必需的依赖
   - 确保依赖版本兼容
   - 考虑升级到 `pyproject.toml` + UV

**6. Rust/Tauri构建问题**
   - 检查 `tauri/src-tauri/Cargo.toml` 配置
   - 确保Rust目标平台支持
   - 验证平台特定配置文件

**7. 图标文件问题**
   - 运行 `python3 build_assets/universal_icon_generator_ascii.py` 确保图标存在
   - 检查图标文件格式和尺寸
   - 确保macOS上有iconutil工具

### 本地测试构建
```bash
# 测试PyInstaller构建
pyinstaller entrypoint.pyinstaller.onefile.spec

# 测试Tauri构建
cd tauri
pnpm tauri build

# 测试UV环境
uv sync --all-extras --group build
```

### macOS常见问题

**应用无法启动**:
1. 权限问题: 右键点击应用 → "打开"
2. 安全设置: 系统偏好设置 → 安全性与隐私 → 允许来自身份不明开发者的应用
3. 依赖缺失: 确保运行了完整的构建流程

## 🛠️ 开发建议

### 推荐工作流

1. **日常开发**
   ```bash
   # 使用快速UV进行依赖管理
   uv sync --all-extras --group build
   cd tauri && pnpm tauri dev
   ```

2. **功能测试**  
   ```bash
   # 推送到main进行自动测试
   git push origin main
   ```

3. **正式发布**
   ```bash
   # 更新pyproject.toml中的版本
   # 使用规范化提交自动生成变更日志
   git commit -m "feat: 添加新功能"
   git tag v1.0.0 && git push origin v1.0.0
   ```

4. **调试版本**
   ```bash
   # PyInstaller版本用于详细控制台输出
   git push origin pyinstaller
   git tag py-v1.0.0 && git push origin py-v1.0.0
   ```

### 规范化提交

使用规范化提交格式自动生成变更日志：

```bash
git commit -m "feat: 添加分数趋势分析功能"
git commit -m "fix: 修复数据导入编码问题"  
git commit -m "docs: 更新安装指南"
git commit -m "perf: 优化图表渲染性能"
```

### 版本管理

- **统一来源**: 版本定义在 `pyproject.toml`
- **自动提取**: GitHub Actions自动读取版本
- **一致发布**: 无需手动同步版本号

### 性能提示

- **使用UV**: 比pip快10倍的依赖管理
- **平台特定构建**: 利用Tauri的平台配置
- **并行CI**: GitHub Actions同时运行所有平台

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支: `git checkout -b feature/amazing-feature`  
3. 使用规范化提交: `git commit -m "feat: 添加惊人功能"`
4. 推送到分支: `git push origin feature/amazing-feature`
5. 提交Pull Request

## 📝 变更日志

变更日志基于规范化提交使用 `git-cliff` 自动生成。查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史。

## 🐛 问题反馈

发现Bug？请在 [GitHub Issues](https://github.com/yingzixiaoyuan/st_score/issues) 中反馈。

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 了解详情。