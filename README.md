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

## 🚀 开发环境设置

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
# 生成应用图标
python3 build_assets/make_icon.py
python3 build_assets/generate_tauri_icons.py
```

### 构建发布版本

```bash
# 构建所有平台
cd tauri
pnpm tauri build
```

## 📦 构建和发布选项

本项目提供两种构建方式：

### 🖥️ Tauri桌面应用版本 (推荐)
推送版本标签会自动触发构建和发布：

```bash
git tag v1.0.0
git push origin v1.0.0
```

构建产物包括：
- **Windows**: `.exe`安装包和`.msi`文件
- **macOS**: `.dmg`磁盘映像文件
- **Linux**: `.deb`包和`.AppImage`可执行文件

### 💻 PyInstaller简化版本
适合快速部署和测试：

```bash
# 推送到pyinstaller分支进行构建
git checkout -b pyinstaller
git push origin pyinstaller

# 或创建PyInstaller版本标签
git tag py-v1.0.0
git push origin py-v1.0.0
```

构建产物包括：
- **Windows**: `.zip`压缩包（含可执行文件）
- **macOS**: `.tar.gz`压缩包
- **Linux**: 单个可执行文件

详细说明请查看 [构建选项文档](docs/BUILD_OPTIONS.md)

## 🎯 使用方法

1. 下载对应平台的安装包
2. 安装并启动应用程序
3. 等待启动画面加载完成
4. 应用会自动打开内置的Web界面
5. 开始导入和分析学生成绩数据

## 📝 项目结构

```
st_score/
├── .github/workflows/     # GitHub Actions工作流
│   ├── build-release.yml        # Tauri桌面应用构建
│   └── build-pyinstaller.yml    # PyInstaller构建
├── webapp/               # Streamlit应用源码
├── tauri/               # Tauri桌面应用
│   ├── src-tauri/      # Rust后端代码
│   ├── public/         # 静态资源
│   └── package.json    # 前端依赖
├── docs/                # 项目文档
│   ├── BUILD_OPTIONS.md        # 构建选项说明
│   └── WORKFLOW_GUIDE.md       # 工作流使用指南
├── build_assets/        # 构建资源和图标
├── config/             # 配置文件
├── hooks/              # PyInstaller钩子文件
├── entrypoint.py       # Python应用入口
├── entrypoint*.spec    # PyInstaller配置文件
└── requirements.txt    # Python依赖
```

## 🔄 工作流程

1. **开发**: 使用`pnpm tauri dev`进行开发
2. **测试**: 推送到main分支触发构建测试
3. **发布**: 推送版本标签触发正式发布

## 🐛 问题反馈

如有问题，请在GitHub Issues中反馈。

## 📄 许可证

MIT License
