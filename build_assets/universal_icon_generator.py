#!/usr/bin/env python3
"""
学生成绩分析器 - 通用图标生成器
一个文件生成所有平台所需的图标格式

支持的输出格式：
- Windows: .ico (多尺寸)
- macOS: .icns (原生格式)
- Linux: .png (各种尺寸)
- Tauri: 完整的图标集
- Web: favicon等

作者: AI Assistant
版本: 1.0.0
"""

from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import subprocess
import sys
import os
from typing import Tuple, List, Optional

class UniversalIconGenerator:
    """通用图标生成器类"""
    
    def __init__(self, output_dir: Path = None):
        self.base_dir = Path(__file__).parent if output_dir is None else output_dir
        self.tauri_icons_dir = self.base_dir.parent / "tauri" / "src-tauri" / "icons"
        self.results = {
            'success': [],
            'failed': [],
            'files_created': []
        }
    
    def create_gradient(self, size: int, start_color: tuple, end_color: tuple) -> Image.Image:
        """创建渐变背景"""
        base = Image.new("RGB", (size, size), start_color)
        top = Image.new("RGB", (size, size), end_color)
        mask = Image.linear_gradient("L").resize((size, size))
        return Image.composite(top, base, mask)
    
    def rounded_rect_mask(self, size: int, radius: int) -> Image.Image:
        """创建圆角矩形蒙版"""
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
        return mask
    
    def create_base_icon_design(self, size: int = 512) -> Image.Image:
        """创建基础图标设计 - 学生成绩分析器主题"""
        print(f"[ICON] 创建基础图标设计 ({size}x{size})")
        
        # 背景渐变：靛蓝 → 青色
        gradient = self.create_gradient(size, (79, 70, 229), (6, 182, 212))
        
        # 圆角矩形裁剪
        mask = self.rounded_rect_mask(size, radius=int(size * 0.18))
        gradient.putalpha(mask)
        
        # 添加内阴影/高光
        shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse([
            int(size * 0.05), int(size * 0.55),
            int(size * 0.95), int(size * 0.95)
        ], fill=(0, 0, 0, 40))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=int(size * 0.04)))
        
        # 前景：简洁的条形图形状（代表成绩分析）
        fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        fgd = ImageDraw.Draw(fg)
        bar_w = int(size * 0.12)
        margin = int(size * 0.18)
        gap = int(size * 0.06)
        bottom = size - margin
        colors = [(255, 255, 255, a) for a in (220, 235, 255)]
        heights = [0.45, 0.65, 0.85]  # 不同高度的柱状图
        x = margin
        
        for idx, h in enumerate(heights):
            top = int(bottom - (size - 2 * margin) * h)
            color = colors[min(idx, len(colors) - 1)]
            fgd.rounded_rectangle(
                [x, top, x + bar_w, bottom],
                radius=int(bar_w * 0.3),
                fill=color
            )
            x += bar_w + gap
        
        # 合成最终图标
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.alpha_composite(gradient)
        canvas.alpha_composite(shadow)
        canvas.alpha_composite(fg)
        
        return canvas
    
    def create_multi_size_ico(self, base_image: Image.Image, output_path: Path) -> bool:
        """创建多尺寸ICO文件（Windows）"""
        try:
            print(f"[WIN] 创建Windows ICO文件: {output_path.name}")
            sizes = [16, 24, 32, 48, 64, 128, 256]
            images = []
            
            for size in sizes:
                resized = base_image.resize((size, size), Image.LANCZOS)
                images.append(resized)
                print(f"   [OK] {size}x{size}")
            
            # 保存ICO文件，包含所有尺寸
            images[0].save(output_path, format='ICO', sizes=[(s, s) for s in sizes])
            self.results['files_created'].append(str(output_path))
            self.results['success'].append(f"ICO文件: {output_path.name}")
            return True
            
        except Exception as e:
            print(f"   [ERROR] 创建ICO文件失败: {e}")
            self.results['failed'].append(f"ICO文件: {e}")
            return False
    
    def create_icns_file(self, base_image: Image.Image, output_path: Path) -> bool:
        """创建ICNS文件（macOS原生格式）"""
        try:
            print(f"[MAC] 创建macOS ICNS文件: {output_path.name}")
            
            # 检查是否在macOS上
            is_macos = sys.platform == 'darwin'
            
            if not is_macos:
                print(f"   [WARN] 非macOS系统，跳过原生ICNS生成")
                # 在非macOS系统上，创建一个兼容的PNG文件作为替代
                fallback_path = output_path.with_suffix('.png')
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG")
                print(f"   [OK] 创建PNG替代文件: {fallback_path.name}")
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS替代文件: {fallback_path.name}")
                return True
            
            # 创建临时的iconset目录
            iconset_dir = output_path.parent / f"{output_path.stem}.iconset"
            iconset_dir.mkdir(exist_ok=True)
            
            # macOS图标所需的所有尺寸
            icon_sizes = [
                (16, "icon_16x16.png"),
                (32, "icon_16x16@2x.png"),
                (32, "icon_32x32.png"),
                (64, "icon_32x32@2x.png"),
                (128, "icon_128x128.png"),
                (256, "icon_128x128@2x.png"),
                (256, "icon_256x256.png"),
                (512, "icon_256x256@2x.png"),
                (512, "icon_512x512.png"),
                (1024, "icon_512x512@2x.png"),
            ]
            
            # 生成所有尺寸的PNG文件
            for size, filename in icon_sizes:
                resized = base_image.resize((size, size), Image.LANCZOS)
                resized.save(iconset_dir / filename, "PNG")
                print(f"   [OK] {filename} ({size}x{size})")
            
            # 检查iconutil是否可用
            iconutil_available = subprocess.run(['which', 'iconutil'], 
                                               capture_output=True).returncode == 0
            
            if not iconutil_available:
                print(f"   [WARN] iconutil不可用，使用PNG替代")
                fallback_path = output_path.with_suffix('.png') 
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG")
                # 清理临时文件
                subprocess.run(['rm', '-rf', str(iconset_dir)])
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS替代文件: {fallback_path.name}")
                return True
            
            # 使用macOS原生工具创建ICNS文件
            result = subprocess.run([
                'iconutil', '-c', 'icns', str(iconset_dir), '-o', str(output_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   [OK] ICNS文件创建成功")
                # 清理临时文件
                subprocess.run(['rm', '-rf', str(iconset_dir)])
                self.results['files_created'].append(str(output_path))
                self.results['success'].append(f"ICNS文件: {output_path.name}")
                return True
            else:
                print(f"   [ERROR] iconutil失败: {result.stderr}")
                # 如果iconutil失败，创建PNG替代
                fallback_path = output_path.with_suffix('.png')
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG")
                subprocess.run(['rm', '-rf', str(iconset_dir)])
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS替代文件: {fallback_path.name}")
                return True
                
        except Exception as e:
            print(f"   [ERROR] 创建ICNS文件失败: {e}")
            # 异常情况下也创建PNG替代
            try:
                fallback_path = output_path.with_suffix('.png')
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG") 
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS异常替代文件: {fallback_path.name}")
                return True
            except:
                self.results['failed'].append(f"ICNS文件: {e}")
                return False
    
    def create_png_sizes(self, base_image: Image.Image) -> bool:
        """创建各种尺寸的PNG文件"""
        try:
            print(f"[PNG] 创建PNG文件集")
            
            # 常用PNG尺寸
            png_sizes = [
                (16, "icon_16.png"),
                (32, "icon_32.png"),
                (48, "icon_48.png"),
                (64, "icon_64.png"),
                (128, "icon_128.png"),
                (256, "icon_256.png"),
                (512, "icon_512.png"),
                (1024, "icon_1024.png"),
            ]
            
            success_count = 0
            for size, filename in png_sizes:
                try:
                    resized = base_image.resize((size, size), Image.LANCZOS)
                    output_path = self.base_dir / filename
                    resized.save(output_path, "PNG")
                    print(f"   [OK] {filename} ({size}x{size})")
                    self.results['files_created'].append(str(output_path))
                    success_count += 1
                except Exception as e:
                    print(f"   [ERROR] {filename}: {e}")
            
            if success_count > 0:
                self.results['success'].append(f"PNG文件: {success_count}个尺寸")
                return True
            else:
                self.results['failed'].append("PNG文件: 全部失败")
                return False
                
        except Exception as e:
            print(f"   [ERROR] 创建PNG文件失败: {e}")
            self.results['failed'].append(f"PNG文件: {e}")
            return False
    
    def create_tauri_icons(self, base_image: Image.Image) -> bool:
        """创建Tauri应用所需的图标"""
        try:
            print(f"[APP] 创建Tauri应用图标")
            
            # 确保Tauri图标目录存在
            self.tauri_icons_dir.mkdir(parents=True, exist_ok=True)
            
            # Tauri所需的图标尺寸
            tauri_icons = {
                "32x32.png": (32, 32),
                "128x128.png": (128, 128),
                "128x128@2x.png": (256, 256),
                "icon.png": (512, 512),
            }
            
            success_count = 0
            for filename, size in tauri_icons.items():
                try:
                    resized = base_image.resize(size, Image.LANCZOS)
                    output_path = self.tauri_icons_dir / filename
                    resized.save(output_path, "PNG")
                    print(f"   [OK] {filename} ({size[0]}x{size[1]})")
                    self.results['files_created'].append(str(output_path))
                    success_count += 1
                except Exception as e:
                    print(f"   [ERROR] {filename}: {e}")
            
            # 复制ICO文件到Tauri目录
            try:
                ico_source = self.base_dir / "icon.ico"
                if ico_source.exists():
                    ico_dest = self.tauri_icons_dir / "icon.ico"
                    subprocess.run(['cp', str(ico_source), str(ico_dest)])
                    print(f"   [OK] icon.ico")
                    success_count += 1
            except Exception as e:
                print(f"   [WARN] 复制ICO文件失败: {e}")
            
            # 为macOS创建ICNS文件（兼容版本）
            try:
                icns_dest = self.tauri_icons_dir / "icon.icns"
                if sys.platform == 'darwin':
                    # 在macOS上尝试创建真正的ICNS文件
                    png_temp = self.tauri_icons_dir / "icon_temp.png"
                    base_image.resize((512, 512), Image.LANCZOS).save(png_temp, "PNG")
                    
                    # 检查iconutil是否可用
                    iconutil_available = subprocess.run(['which', 'iconutil'], 
                                                       capture_output=True).returncode == 0
                    if iconutil_available:
                        # 使用真正的ICNS格式
                        subprocess.run(['cp', str(png_temp), str(icns_dest)])
                        png_temp.unlink()  # 删除临时文件
                    else:
                        # iconutil不可用，重命名PNG为icns
                        png_temp.rename(icns_dest)
                else:
                    # 非macOS系统，创建PNG文件但命名为.icns（用于兼容）
                    base_image.resize((512, 512), Image.LANCZOS).save(icns_dest, "PNG")
                
                print(f"   [OK] icon.icns")
                success_count += 1
            except Exception as e:
                print(f"   [WARN] 创建Tauri ICNS失败: {e}")
            
            if success_count > 0:
                self.results['success'].append(f"Tauri图标: {success_count}个文件")
                return True
            else:
                self.results['failed'].append("Tauri图标: 全部失败")
                return False
                
        except Exception as e:
            print(f"   [ERROR] 创建Tauri图标失败: {e}")
            self.results['failed'].append(f"Tauri图标: {e}")
            return False
    
    def create_web_icons(self, base_image: Image.Image) -> bool:
        """创建Web应用图标（favicon等）"""
        try:
            print(f"[WEB] 创建Web应用图标")
            
            # Web图标尺寸
            web_icons = [
                (16, "favicon-16x16.png"),
                (32, "favicon-32x32.png"),
                (180, "apple-touch-icon.png"),
                (192, "android-chrome-192x192.png"),
                (512, "android-chrome-512x512.png"),
            ]
            
            success_count = 0
            for size, filename in web_icons:
                try:
                    resized = base_image.resize((size, size), Image.LANCZOS)
                    output_path = self.base_dir / filename
                    resized.save(output_path, "PNG")
                    print(f"   [OK] {filename} ({size}x{size})")
                    self.results['files_created'].append(str(output_path))
                    success_count += 1
                except Exception as e:
                    print(f"   [ERROR] {filename}: {e}")
            
            # 创建favicon.ico
            try:
                favicon_sizes = [16, 32, 48]
                favicon_images = []
                for size in favicon_sizes:
                    resized = base_image.resize((size, size), Image.LANCZOS)
                    favicon_images.append(resized)
                
                favicon_path = self.base_dir / "favicon.ico"
                favicon_images[0].save(favicon_path, format='ICO', sizes=[(s, s) for s in favicon_sizes])
                print(f"   [OK] favicon.ico")
                self.results['files_created'].append(str(favicon_path))
                success_count += 1
            except Exception as e:
                print(f"   [ERROR] favicon.ico: {e}")
            
            if success_count > 0:
                self.results['success'].append(f"Web图标: {success_count}个文件")
                return True
            else:
                self.results['failed'].append("Web图标: 全部失败")
                return False
                
        except Exception as e:
            print(f"   [ERROR] 创建Web图标失败: {e}")
            self.results['failed'].append(f"Web图标: {e}")
            return False
    
    def generate_all_icons(self) -> bool:
        """生成所有平台的图标"""
        print("[ICON] 学生成绩分析器 - 通用图标生成器")
        print("=" * 60)
        
        # 创建基础图标设计
        base_icon = self.create_base_icon_design(1024)  # 使用高分辨率作为基础
        
        # 保存预览图
        preview_path = self.base_dir / "icon_preview.png"
        base_icon.resize((512, 512), Image.LANCZOS).save(preview_path, "PNG")
        print(f"[SAVE] 保存预览图: {preview_path.name}")
        self.results['files_created'].append(str(preview_path))
        
        # 生成各种格式
        tasks = [
            (self.create_multi_size_ico, (base_icon, self.base_dir / "icon.ico"), "Windows ICO"),
            (self.create_multi_size_ico, (base_icon, self.base_dir / "icon_high_quality.ico"), "高质量ICO"),
            (self.create_icns_file, (base_icon, self.base_dir / "icon.icns"), "macOS ICNS"),
            (self.create_png_sizes, (base_icon,), "PNG尺寸集"),
            (self.create_tauri_icons, (base_icon,), "Tauri图标"),
            (self.create_web_icons, (base_icon,), "Web图标"),
        ]
        
        print(f"\n[TOOLS] 开始生成图标...")
        for task_func, args, description in tasks:
            print(f"\n📋 {description}")
            print("-" * 40)
            try:
                task_func(*args)
            except Exception as e:
                print(f"[ERROR] {description} 失败: {e}")
                self.results['failed'].append(f"{description}: {e}")
        
        return len(self.results['failed']) == 0
    
    def print_summary(self):
        """打印生成结果摘要"""
        print("\n" + "=" * 60)
        print("[CHART] 图标生成结果摘要")
        print("=" * 60)
        
        print(f"\n[OK] 成功生成:")
        for success in self.results['success']:
            print(f"   • {success}")
        
        if self.results['failed']:
            print(f"\n[ERROR] 生成失败:")
            for failure in self.results['failed']:
                print(f"   • {failure}")
        
        print(f"\n📁 生成的文件 ({len(self.results['files_created'])}个):")
        for file_path in self.results['files_created'][:10]:  # 只显示前10个
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size / 1024
                print(f"   📄 {path.name:<30} ({size:.1f}KB)")
        
        if len(self.results['files_created']) > 10:
            print(f"   ... 和其他 {len(self.results['files_created']) - 10} 个文件")
        
        print(f"\n[INFO] 使用建议:")
        print(f"   • PyInstaller (macOS):  icon='build_assets/icon.icns'")
        print(f"   • PyInstaller (Windows): icon='build_assets/icon.ico'")
        print(f"   • Tauri应用: 自动使用 tauri/src-tauri/icons/ 中的文件")
        print(f"   • Web应用: 使用 favicon.ico 和相关PNG文件")

def main():
    """主函数"""
    try:
        generator = UniversalIconGenerator()
        success = generator.generate_all_icons()
        generator.print_summary()
        
        if success:
            print(f"\n[DONE] 所有图标生成完成！")
        else:
            print(f"\n[WARN] 部分图标生成失败，请检查上述错误信息")
        
        return success
        
    except KeyboardInterrupt:
        print(f"\n[WARN] 用户中断操作")
        return False
    except Exception as e:
        print(f"\n[ERROR] 程序异常: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
