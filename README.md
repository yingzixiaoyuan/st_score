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
- **构建**: GitHub Actions自动化CI/CD

## 🚀 快速开始

### 前提条件

- Python 3.11+
- Node.js 18+
- pnpm
- Rust (最新稳定版)

### 安装依赖

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
# 一键生成所有平台图标
python3 build_assets/universal_icon_generator.py
```

### 构建发布版本

```bash
# 构建所有平台
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

## 📝 项目结构

```
st_score/
├── .github/workflows/          # GitHub Actions工作流
│   ├── build-release.yml             # Tauri桌面应用构建
│   ├── build-pyinstaller.yml         # PyInstaller构建
│   └── build-windows-exe.yml         # Windows专用构建
├── webapp/                     # Streamlit应用源码
│   ├── pages/                 # Streamlit页面模块
│   ├── app.py                # 主应用程序
│   ├── analyzer.py           # 成绩分析器
│   ├── database.py           # 数据库管理
│   └── ...                   # 其他应用文件
├── tauri/                      # Tauri桌面应用
│   ├── src-tauri/             # Rust后端代码
│   ├── public/                # 静态资源
│   └── package.json           # 前端依赖
├── build_assets/              # 构建资源和图标
│   ├── universal_icon_generator.py   # 统一图标生成器
│   └── icon*.*               # 各种格式的应用图标
├── config/                    # 配置文件
├── hooks/                     # PyInstaller钩子文件
├── entrypoint.py             # Python应用入口
├── entrypoint*.spec          # PyInstaller配置文件
└── requirements.txt          # Python依赖
```

## 🔄 发布流程

### Tauri桌面应用发布

```bash
# 1. 确保在main分支
git checkout main
git pull origin main

# 2. 提交更改
git add .
git commit -m "Release v1.0.0"

# 3. 创建并推送标签
git tag v1.0.0
git push origin main
git push origin v1.0.0

# 4. GitHub Actions 会自动构建并创建Release
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

## 🛠️ 开发建议

1. **日常开发**: 使用 `pnpm tauri dev` 进行开发
2. **功能测试**: 推送到 `pyinstaller` 分支快速验证
3. **正式发布**: 推送 `v*.*.*` 标签发布Tauri版本
4. **调试版本**: 推送 `py-v*.*.*` 标签发布PyInstaller版本

## 📊 GitHub Actions 工作流

项目包含三个主要工作流：

1. **`build-release.yml`** - Tauri桌面应用构建
   - 触发: 推送 `v*.*.*` 标签或 `main`/`new` 分支
   - 输出: `.exe`, `.msi`, `.dmg`, `.deb`, `.AppImage`

2. **`build-pyinstaller.yml`** - PyInstaller简化版构建
   - 触发: 推送 `py-v*.*.*` 标签或 `pyinstaller` 分支
   - 输出: 跨平台可执行文件

3. **`build-windows-exe.yml`** - Windows专用构建
   - 触发: 推送 `release` 分支或手动触发
   - 输出: Windows可执行文件

## 🐛 问题反馈

如有问题，请在GitHub Issues中反馈。

## 📄 许可证

MIT License