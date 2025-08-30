from PIL import Image
from pathlib import Path
import shutil

def generate_tauri_icons():
    """为Tauri应用生成各种尺寸的图标"""
    base_icon = Path("build_assets/icon_preview.png")
    tauri_icons_dir = Path("tauri/src-tauri/icons")
    
    # 确保图标存在
    if not base_icon.exists():
        print(f"基础图标文件不存在: {base_icon}")
        return
        
    # 加载基础图标
    icon = Image.open(base_icon)
    
    # 定义需要生成的尺寸
    icon_sizes = {
        "32x32.png": (32, 32),
        "128x128.png": (128, 128),
        "128x128@2x.png": (256, 256),
        "icon.png": (512, 512),
    }
    
    # 生成PNG图标
    for filename, size in icon_sizes.items():
        resized = icon.resize(size, Image.LANCZOS)
        output_path = tauri_icons_dir / filename
        resized.save(output_path, "PNG")
        print(f"生成PNG图标: {output_path}")
    
    # 复制ICO文件
    ico_source = Path("build_assets/icon.ico")
    if ico_source.exists():
        ico_dest = tauri_icons_dir / "icon.ico"
        shutil.copy2(ico_source, ico_dest)
        print(f"复制ICO图标: {ico_dest}")
    
    # 为macOS生成ICNS文件（简化版本，实际可能需要更复杂的工具）
    # 这里我们暂时复制PNG文件作为占位符
    icns_dest = tauri_icons_dir / "icon.icns"
    shutil.copy2(tauri_icons_dir / "icon.png", icns_dest)
    print(f"生成ICNS图标: {icns_dest}")
    
    print("所有Tauri图标生成完成！")

if __name__ == "__main__":
    generate_tauri_icons()
