# 🔄 工作流使用指南

## 📁 工作流文件说明

### 1. `.github/workflows/build-release.yml`
**Tauri 桌面应用构建工作流**

- **用途**: 构建跨平台原生桌面应用
- **触发条件**:
  - 推送到 `main` 或 `new` 分支 (仅构建，不发布)
  - 推送 `v*.*.*` 标签 (构建并创建Release)
  - 手动触发 (workflow_dispatch)

### 2. `.github/workflows/build-pyinstaller.yml`
**PyInstaller 简化版构建工作流**

- **用途**: 构建Python可执行文件
- **触发条件**:
  - 推送到 `pyinstaller` 分支 (仅构建，不发布)
  - 推送 `py-v*.*.*` 标签 (构建并创建Release)
  - 手动触发 (可选择是否发布)

## 🚀 发布流程

### Tauri桌面应用发布
```bash
# 1. 确保在main分支
git checkout main
git pull origin main

# 2. 更新版本号 (可选，在tauri.conf.json中)
# 编辑 tauri/src-tauri/tauri.conf.json 中的 version 字段

# 3. 提交更改
git add .
git commit -m "Release v1.0.0"

# 4. 创建并推送标签
git tag v1.0.0
git push origin main
git push origin v1.0.0

# 5. GitHub Actions 会自动构建并创建Release
```

### PyInstaller版本发布
```bash
# 1. 创建或切换到pyinstaller分支
git checkout -b pyinstaller
# 或
git checkout pyinstaller

# 2. 提交更改
git add .
git commit -m "Release PyInstaller v1.0.0"

# 3. 创建并推送标签
git tag py-v1.0.0
git push origin pyinstaller
git push origin py-v1.0.0

# 4. GitHub Actions 会自动构建并创建Release
```

## 🔧 手动触发构建

### 通过 GitHub Web界面
1. 进入项目的 GitHub 页面
2. 点击 "Actions" 标签
3. 选择对应的工作流
4. 点击 "Run workflow" 按钮
5. 选择分支并配置参数

### 通过 GitHub CLI
```bash
# 触发Tauri构建
gh workflow run build-release.yml

# 触发PyInstaller构建 (带发布)
gh workflow run build-pyinstaller.yml -f create_release=true
```

## 📦 构建产物说明

### Tauri版本构建产物
- **Linux**: 
  - `.deb` - Debian/Ubuntu安装包
  - `.AppImage` - 通用Linux可执行文件
- **Windows**:
  - `.exe` - NSIS安装程序 
  - `.msi` - Windows安装包
- **macOS**:
  - `.dmg` - macOS磁盘映像文件

### PyInstaller版本构建产物
- **Linux**: 
  - `st_score-x86_64-unknown-linux-gnu` - 单个可执行文件
- **Windows**:
  - `st_score-x86_64-pc-windows-msvc.zip` - 包含可执行文件的压缩包
- **macOS**:
  - `st_score-*-apple-darwin.tar.gz` - 包含可执行文件的压缩包

## 🐛 故障排除

### 构建失败常见原因

1. **Python依赖问题**
   - 检查 `requirements.txt` 是否包含所有必需的依赖
   - 确保依赖版本兼容

2. **Rust/Tauri构建问题**
   - 检查 `tauri/src-tauri/Cargo.toml` 配置
   - 确保Rust目标平台支持

3. **图标文件问题**
   - 运行 `python build_assets/make_icon.py` 确保图标存在
   - 检查图标文件格式和尺寸

### 构建日志查看
1. 进入 GitHub Actions 页面
2. 点击失败的工作流运行
3. 展开对应步骤查看详细日志
4. 搜索 "ERROR" 或 "FAILED" 关键词

### 本地测试构建
```bash
# 测试PyInstaller构建
pyinstaller entrypoint.pyinstaller.onefile.spec

# 测试Tauri构建
cd tauri
pnpm tauri build
```

## 📊 工作流监控

### 构建状态徽章
可以在README中添加构建状态徽章：

```markdown
![Tauri Build](https://github.com/你的用户名/st_score/workflows/Build%20Student%20Score%20Analyzer%20Desktop%20App%20&%20Release/badge.svg)
![PyInstaller Build](https://github.com/你的用户名/st_score/workflows/Build%20PyInstaller%20App%20&%20Release/badge.svg)
```

### 通知设置
在GitHub仓库设置中配置构建失败通知：
1. Settings → Notifications
2. 勾选 "Actions" 相关通知选项

## 🔐 权限说明

工作流需要以下权限：
- `contents: read` - 读取仓库内容
- `actions: read` - 读取Actions状态  
- `packages: write` - 上传构建产物
- `releases: write` - 创建和编辑Release

这些权限通过 `GITHUB_TOKEN` 自动提供，无需额外配置。
