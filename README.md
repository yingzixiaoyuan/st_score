# 📊 Student Score Analyzer Desktop App

A cross-platform student score analysis desktop application built with Tauri and Streamlit.

[English](#english) | [中文](#中文)

---

## English

### ✨ Features

- 📊 **Data Import & Analysis**: Support Excel file import and automatic student score data parsing
- 📈 **Multi-dimensional Statistics**: Rich chart displays including score distribution and trend analysis  
- 🎨 **Custom Configuration**: Color theme settings for personalized interface display
- 📚 **History Management**: Complete data history records for tracking and comparison
- 🖥️ **Native Desktop App**: Built with Tauri for fast startup and low resource usage
- 🌐 **Built-in Web Interface**: Integrated Streamlit app with intuitive operation interface

### 🔧 Technical Architecture

- **Frontend**: Tauri 2.0 + TypeScript + Vite
- **Backend**: Python 3.11 + Streamlit + SQLite
- **Packaging**: Cross-platform native app, no browser dependency required
- **Build System**: GitHub Actions automated CI/CD with UV package manager
- **Configuration**: Modern pyproject.toml + platform-specific Tauri configs

### 🚀 Quick Start

#### Prerequisites

- Python 3.11+
- Node.js 18+
- pnpm
- Rust (latest stable)
- **UV** (recommended for faster dependency management)

#### Install UV (Recommended)

```bash
# Install UV - The fastest Python package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

#### Install Dependencies

**With UV (Recommended - 10x faster):**
```bash
# Set up Python environment with UV
uv python install
uv venv
uv sync --all-extras --group build

# Install Tauri frontend dependencies
cd tauri
pnpm install
```

**Traditional method:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Tauri frontend dependencies  
cd tauri
pnpm install
```

#### Development

```bash
# Start development mode
cd tauri
pnpm tauri dev
```

#### Generate Icons

```bash
# Generate all platform icons with ASCII-only output
python3 build_assets/universal_icon_generator_ascii.py
```

#### Build Release

```bash
# Build for all platforms
cd tauri
pnpm tauri build
```

## 📦 构建和发布选项

本项目提供两种构建方式，满足不同的使用需求：

### 🖥️ Tauri桌面应用版本 (推荐)

**特点**:
- ✨ **原生桌面应用**: 真正的桌面应用体验
- 🚀 **启动速度快**: Rust + Tauri 框架，性能优异
- 🎨 **美观界面**: 自定义启动画面和应用图标
- 💾 **资源占用少**: 比Electron应用更轻量
- 📦 **标准安装包**: 提供各平台的标准安装程序

**发布命令**:
```bash
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

### 🔄 两种版本对比

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

### 🏗️ Modern Development Workflow

#### Project Configuration

The project uses modern Python packaging with `pyproject.toml`:

```toml
[project]
name = "student-score-analyzer"
version = "0.1.0"  # Single source of truth for version
dependencies = [
    "streamlit>=1.28.0",
    "pandas>=2.0.0",
    # ... other dependencies
]

[project.optional-dependencies]
build = ["pyinstaller>=6.0.0"]
```

#### Platform-Specific Tauri Configuration

```
tauri/src-tauri/
├── tauri.conf.json           # Main configuration
├── tauri.linux.conf.json    # Linux-specific: deb + appimage  
└── tauri.windows.conf.json  # Windows-specific: nsis + msi
```

#### Automated Changelog Generation

Uses `git-cliff` for automatic changelog generation based on conventional commits:

```bash
# Install git-cliff
pip install git-cliff

# Generate changelog
git cliff --latest > CHANGELOG.md
```

### 📁 Project Structure

```
st_score/
├── .github/workflows/              # GitHub Actions workflows
│   ├── build-release.yml              # Main Tauri desktop app build  
│   ├── build-release-optimized.yml    # Optimized build with UV
│   ├── build-pyinstaller.yml          # PyInstaller build
│   └── build-windows-exe.yml          # Windows-specific build
├── webapp/                         # Streamlit application source
│   ├── pages/                     # Streamlit page modules
│   ├── app.py                    # Main application
│   ├── analyzer.py               # Score analyzer
│   ├── database.py               # Database management
│   └── ...                       # Other app files
├── tauri/                          # Tauri desktop application
│   ├── src-tauri/                 # Rust backend code
│   │   ├── tauri.conf.json           # Main Tauri config
│   │   ├── tauri.linux.conf.json     # Linux-specific config
│   │   └── tauri.windows.conf.json   # Windows-specific config
│   ├── src/                      # TypeScript frontend source
│   ├── public/                   # Static assets
│   └── package.json              # Frontend dependencies
├── build_assets/                   # Build resources and icons
│   ├── universal_icon_generator_ascii.py  # ASCII-only icon generator
│   └── icon*.*                   # Various format app icons
├── config/                         # Configuration files
├── hooks/                          # PyInstaller hook files
├── entrypoint.py                  # Python app entry point
├── entrypoint*.spec               # PyInstaller config files
├── pyproject.toml                 # Modern Python project config
├── cliff.toml                     # Changelog generation config
├── requirements.txt               # Python dependencies (legacy)
└── README.md                      # This file
```

### 🚀 Release Workflow

#### Modern Release Process

**1. Update Version in pyproject.toml**
```toml
[project]
version = "1.0.0"  # Update this
```

**2. Commit with Conventional Commits**
```bash
# Use conventional commit format for auto-changelog
git add .
git commit -m "feat: add new analysis features

- Add advanced score distribution charts
- Implement trend analysis algorithms
- Update UI for better user experience"
```

**3. Create Release**
```bash
# Push to main branch (triggers build for testing)
git push origin main

# Create and push tag (triggers release)
git tag v1.0.0
git push origin v1.0.0
```

**4. Automated Process**
- GitHub Actions builds all platforms automatically
- Changelog is generated from commit history
- Release is created with all artifacts
- Version is extracted from pyproject.toml

#### Manual Trigger

**Via GitHub Web Interface:**
1. Go to "Actions" tab
2. Select workflow 
3. Click "Run workflow"

**Via GitHub CLI:**
```bash
gh workflow run build-release-optimized.yml
```

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
python3 build_assets/universal_icon_generator.py

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
# 触发Tauri构建
gh workflow run build-release.yml

# 触发PyInstaller构建
gh workflow run build-pyinstaller.yml -f create_release=true
```

## 🐛 故障排除

### 构建失败常见原因

1. **Python依赖问题**
   - 检查 `requirements.txt` 是否包含所有必需的依赖
   - 确保依赖版本兼容

2. **Rust/Tauri构建问题**
   - 检查 `tauri/src-tauri/Cargo.toml` 配置
   - 确保Rust目标平台支持

3. **图标文件问题**
   - 运行 `python3 build_assets/universal_icon_generator.py` 确保图标存在
   - 检查图标文件格式和尺寸

### 本地测试构建
```bash
# 测试PyInstaller构建
pyinstaller entrypoint.pyinstaller.onefile.spec

# 测试Tauri构建
cd tauri
pnpm tauri build
```

### macOS常见问题

**应用无法启动**:
1. 权限问题: 右键点击应用 → "打开"
2. 安全设置: 系统偏好设置 → 安全性与隐私 → 允许来自身份不明开发者的应用
3. 依赖缺失: 确保运行了完整的构建流程

### 🛠️ Development Best Practices

#### Recommended Workflow

1. **Daily Development**
   ```bash
   # Use fast UV for dependency management
   uv sync --all-extras --group build
   cd tauri && pnpm tauri dev
   ```

2. **Feature Testing**  
   ```bash
   # Push to main for automated testing
   git push origin main
   ```

3. **Production Release**
   ```bash
   # Update version in pyproject.toml
   # Use conventional commits for auto-changelog
   git commit -m "feat: add new features"
   git tag v1.0.0 && git push origin v1.0.0
   ```

4. **Debug Version**
   ```bash
   # PyInstaller version for detailed console output
   git push origin pyinstaller
   git tag py-v1.0.0 && git push origin py-v1.0.0
   ```

#### Conventional Commits

Use conventional commit format for automatic changelog generation:

```bash
git commit -m "feat: add score trend analysis"
git commit -m "fix: resolve data import encoding issue"  
git commit -m "docs: update installation guide"
git commit -m "perf: optimize chart rendering performance"
```

#### Version Management

- **Single Source**: Version defined in `pyproject.toml`
- **Automatic Extraction**: GitHub Actions reads version automatically
- **Consistent Releases**: No manual version sync needed

---

## 中文

### 📊 学生成绩分析器桌面应用

基于Tauri和Streamlit构建的跨平台学生成绩分析桌面应用程序。

### 📊 GitHub Actions Workflows

#### Available Workflows

1. **`build-release-optimized.yml`** - Modern Tauri Build (Recommended)
   - **Triggers**: Push `v*.*.*` tags or `main`/`release` branches
   - **Features**: 
     - UV package manager for 10x faster builds
     - Automatic changelog generation with git-cliff
     - Platform-specific configurations
     - Cross-platform artifact generation
   - **Outputs**: `.exe`, `.msi`, `.dmg`, `.deb`, `.AppImage`

2. **`build-release.yml`** - Legacy Tauri Build
   - **Triggers**: Push `v*.*.*` tags or `release` branches  
   - **Features**: Traditional pip-based dependency management
   - **Outputs**: Same as optimized version

3. **`build-pyinstaller.yml`** - PyInstaller Simple Build
   - **Triggers**: Push `py-v*.*.*` tags or `pyinstaller` branch
   - **Features**: Cross-platform executable files
   - **Outputs**: Standalone executables

4. **`build-windows-exe.yml`** - Windows-specific Build
   - **Triggers**: Push `release` branch or manual trigger
   - **Outputs**: Windows executable files

#### Performance Comparison

| Workflow | Dependency Install Time | Total Build Time | Features |
|----------|------------------------|------------------|----------|
| **Optimized (UV)** | ~30-60s | ~8-12min | ⭐⭐⭐⭐⭐ Modern, Fast |
| **Legacy (pip)** | ~2-3min | ~12-18min | ⭐⭐⭐ Traditional |
| **PyInstaller** | ~2-3min | ~10-15min | ⭐⭐⭐ Simple |

#### Recommended Usage

- **Development**: Use optimized workflow for fastest feedback
- **Production**: Use optimized workflow for releases  
- **Debugging**: Use PyInstaller for console output visibility

### 🔧 故障排除

#### 常见构建问题

**1. UV Installation Issues**
```bash
# If UV is not found, install it:
curl -LsSf https://astral.sh/uv/install.sh | sh
# or use pip fallback
pip install uv
```

**2. Unicode Errors (Windows)**
- ✅ **已解决**: 项目使用纯ASCII输出
- Use `universal_icon_generator_ascii.py` instead of the Unicode version

**3. Tauri Build Failures**
```bash
# Ensure all platform configs exist:
ls tauri/src-tauri/tauri*.conf.json

# Regenerate icons if missing:
python3 build_assets/universal_icon_generator_ascii.py
```

**4. Dependency Conflicts**
```bash
# Clear and reinstall with UV:
rm -rf .venv
uv venv
uv sync --all-extras --group build
```

#### Performance Tips

- **Use UV**: 10x faster than pip for dependency management
- **Platform-specific builds**: Leverage Tauri's platform configs
- **Parallel CI**: GitHub Actions runs all platforms simultaneously

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`  
3. Use conventional commits: `git commit -m "feat: add amazing feature"`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### 📝 Changelog

Changelogs are automatically generated using `git-cliff` based on conventional commits. See [CHANGELOG.md](CHANGELOG.md) for version history.

### 🐛 Issue Reporting

Found a bug? Please report it on [GitHub Issues](https://github.com/yingzixiaoyuan/st_score/issues).

### 📄 License

MIT License - see [LICENSE](LICENSE) for details.