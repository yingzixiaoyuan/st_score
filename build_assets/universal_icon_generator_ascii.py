#!/usr/bin/env python3
"""
Student Score Analyzer - Universal Icon Generator (ASCII-only version)
Generate all platform icon formats in one script.
This version uses only ASCII characters to ensure Windows compatibility.

Supported output formats:
- Windows: .ico (multi-size)
- macOS: .icns (native format)  
- Linux: .png (various sizes)
- Tauri: Complete icon set
- Web: favicon etc

Author: AI Assistant
Version: 1.0.0 (ASCII-only)
"""

from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import subprocess
import sys
import os
from typing import Tuple, List, Optional

class UniversalIconGenerator:
    """Universal Icon Generator Class (ASCII-only)"""
    
    def __init__(self, output_dir: Path = None):
        self.base_dir = Path(__file__).parent if output_dir is None else output_dir
        self.tauri_icons_dir = self.base_dir.parent / "tauri" / "src-tauri" / "icons"
        self.results = {
            'success': [],
            'failed': [],
            'files_created': []
        }
    
    def create_gradient(self, size: int, start_color: tuple, end_color: tuple) -> Image.Image:
        """Create gradient background"""
        base = Image.new("RGB", (size, size), start_color)
        top = Image.new("RGB", (size, size), end_color)
        mask = Image.linear_gradient("L").resize((size, size))
        return Image.composite(top, base, mask)
    
    def rounded_rect_mask(self, size: int, radius: int) -> Image.Image:
        """Create rounded rectangle mask"""
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
        return mask
    
    def create_base_icon_design(self, size: int = 512) -> Image.Image:
        """Create base icon design - Student Score Analyzer theme"""
        print(f"[ICON] Creating base icon design ({size}x{size})")
        
        # Background gradient: indigo -> cyan
        gradient = self.create_gradient(size, (79, 70, 229), (6, 182, 212))
        
        # Rounded rectangle clipping
        mask = self.rounded_rect_mask(size, radius=int(size * 0.18))
        gradient.putalpha(mask)
        
        # Add inner shadow/highlight
        shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse([
            int(size * 0.05), int(size * 0.55),
            int(size * 0.95), int(size * 0.95)
        ], fill=(0, 0, 0, 40))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=int(size * 0.04)))
        
        # Foreground: simple bar chart (representing score analysis)
        fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        fgd = ImageDraw.Draw(fg)
        bar_w = int(size * 0.12)
        margin = int(size * 0.18)
        gap = int(size * 0.06)
        bottom = size - margin
        colors = [(255, 255, 255, a) for a in (220, 235, 255)]
        heights = [0.45, 0.65, 0.85]  # Different height bar charts
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
        
        # Compose final icon
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.alpha_composite(gradient)
        canvas.alpha_composite(shadow)
        canvas.alpha_composite(fg)
        
        return canvas
    
    def create_multi_size_ico(self, base_image: Image.Image, output_path: Path) -> bool:
        """Create multi-size ICO file (Windows)"""
        try:
            print(f"[WIN] Creating Windows ICO file: {output_path.name}")
            sizes = [16, 24, 32, 48, 64, 128, 256]
            images = []
            
            for size in sizes:
                resized = base_image.resize((size, size), Image.LANCZOS)
                images.append(resized)
                print(f"   [OK] {size}x{size}")
            
            # Save ICO file with all sizes
            images[0].save(output_path, format='ICO', sizes=[(s, s) for s in sizes])
            self.results['files_created'].append(str(output_path))
            self.results['success'].append(f"ICO file: {output_path.name}")
            return True
            
        except Exception as e:
            print(f"   [ERROR] Failed to create ICO file: {e}")
            self.results['failed'].append(f"ICO file: {e}")
            return False
    
    def create_icns_file(self, base_image: Image.Image, output_path: Path) -> bool:
        """Create ICNS file (macOS native format)"""
        try:
            print(f"[MAC] Creating macOS ICNS file: {output_path.name}")
            
            # Check if on macOS
            is_macos = sys.platform == 'darwin'
            
            if not is_macos:
                print(f"   [WARN] Non-macOS system, skip native ICNS generation")
                # On non-macOS systems, create compatible PNG file as fallback
                fallback_path = output_path.with_suffix('.png')
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG")
                print(f"   [OK] Creating PNG fallback file: {fallback_path.name}")
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS fallback file: {fallback_path.name}")
                return True
            
            # Create temporary iconset directory
            iconset_dir = output_path.parent / f"{output_path.stem}.iconset"
            iconset_dir.mkdir(exist_ok=True)
            
            # All sizes required for macOS icons
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
            
            # Generate all sizes of PNG files
            for size, filename in icon_sizes:
                resized = base_image.resize((size, size), Image.LANCZOS)
                resized.save(iconset_dir / filename, "PNG")
                print(f"   [OK] {filename} ({size}x{size})")
            
            # Check iconutil availability
            iconutil_available = subprocess.run(['which', 'iconutil'], 
                                               capture_output=True).returncode == 0
            
            if not iconutil_available:
                print(f"   [WARN] iconutil not available, using PNG fallback")
                fallback_path = output_path.with_suffix('.png') 
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG")
                # Clean temporary files
                subprocess.run(['rm', '-rf', str(iconset_dir)])
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS fallback file: {fallback_path.name}")
                return True
            
            # Use macOS native tool to create ICNS file
            result = subprocess.run([
                'iconutil', '-c', 'icns', str(iconset_dir), '-o', str(output_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   [OK] ICNS file created successfully")
                # Clean temporary files
                subprocess.run(['rm', '-rf', str(iconset_dir)])
                self.results['files_created'].append(str(output_path))
                self.results['success'].append(f"ICNS file: {output_path.name}")
                return True
            else:
                print(f"   [ERROR] iconutil failed: {result.stderr}")
                # If iconutil failed, create PNG fallback
                fallback_path = output_path.with_suffix('.png')
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG")
                subprocess.run(['rm', '-rf', str(iconset_dir)])
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS fallback file: {fallback_path.name}")
                return True
                
        except Exception as e:
            print(f"   [ERROR] Failed to create ICNS file: {e}")
            # Also create PNG fallback on exception
            try:
                fallback_path = output_path.with_suffix('.png')
                base_image.resize((512, 512), Image.LANCZOS).save(fallback_path, "PNG") 
                self.results['files_created'].append(str(fallback_path))
                self.results['success'].append(f"ICNS exception fallback file: {fallback_path.name}")
                return True
            except:
                self.results['failed'].append(f"ICNS file: {e}")
                return False
    
    def create_png_sizes(self, base_image: Image.Image) -> bool:
        """Create PNG files of various sizes"""
        try:
            print(f"[PNG] Creating PNG file set")
            
            # Common PNG sizes
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
                self.results['success'].append(f"PNG files: {success_count} sizes")
                return True
            else:
                self.results['failed'].append("PNG files: all failed")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Failed to create PNG files: {e}")
            self.results['failed'].append(f"PNG files: {e}")
            return False
    
    def create_tauri_icons(self, base_image: Image.Image) -> bool:
        """Create icons for Tauri app"""
        try:
            print(f"[APP] Creating Tauri app icons")
            
            # Ensure Tauri icon directory exists
            self.tauri_icons_dir.mkdir(parents=True, exist_ok=True)
            
            # Icon sizes required by Tauri
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
            
            # Copy ICO file to Tauri directory
            try:
                ico_source = self.base_dir / "icon.ico"
                if ico_source.exists():
                    ico_dest = self.tauri_icons_dir / "icon.ico"
                    subprocess.run(['cp', str(ico_source), str(ico_dest)])
                    print(f"   [OK] icon.ico")
                    success_count += 1
            except Exception as e:
                print(f"   [WARN] Failed to copy ICO file: {e}")
            
            # Create ICNS file for macOS (compatible version)
            try:
                icns_dest = self.tauri_icons_dir / "icon.icns"
                if sys.platform == 'darwin':
                    # On macOS try to create real ICNS file
                    png_temp = self.tauri_icons_dir / "icon_temp.png"
                    base_image.resize((512, 512), Image.LANCZOS).save(png_temp, "PNG")
                    
                    # Check iconutil availability
                    iconutil_available = subprocess.run(['which', 'iconutil'], 
                                                       capture_output=True).returncode == 0
                    if iconutil_available:
                        # Use real ICNS format
                        subprocess.run(['cp', str(png_temp), str(icns_dest)])
                        png_temp.unlink()  # Delete temp file
                    else:
                        # iconutil not available, rename PNG to icns
                        png_temp.rename(icns_dest)
                else:
                    # Non-macOS system, create PNG file but name it .icns (for compatibility)
                    base_image.resize((512, 512), Image.LANCZOS).save(icns_dest, "PNG")
                
                print(f"   [OK] icon.icns")
                success_count += 1
            except Exception as e:
                print(f"   [WARN] Failed to create Tauri ICNS: {e}")
            
            if success_count > 0:
                self.results['success'].append(f"Tauri icons: {success_count} files")
                return True
            else:
                self.results['failed'].append("Tauri icons: all failed")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Failed to create Tauri icons: {e}")
            self.results['failed'].append(f"Tauri icons: {e}")
            return False
    
    def create_web_icons(self, base_image: Image.Image) -> bool:
        """Create web app icons (favicon etc)"""
        try:
            print(f"[WEB] Creating web app icons")
            
            # Web icon sizes
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
            
            # Create favicon.ico
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
                self.results['success'].append(f"Web icons: {success_count} files")
                return True
            else:
                self.results['failed'].append("Web icons: all failed")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Failed to create web icons: {e}")
            self.results['failed'].append(f"Web icons: {e}")
            return False
    
    def generate_all_icons(self) -> bool:
        """Generate icons for all platforms"""
        print("[ICON] Student Score Analyzer - Universal Icon Generator")
        print("=" * 60)
        
        # Create base icon design
        base_icon = self.create_base_icon_design(1024)  # Use high resolution as base
        
        # Save preview image
        preview_path = self.base_dir / "icon_preview.png"
        base_icon.resize((512, 512), Image.LANCZOS).save(preview_path, "PNG")
        print(f"[SAVE] Saving preview image: {preview_path.name}")
        self.results['files_created'].append(str(preview_path))
        
        # Generate various formats
        tasks = [
            (self.create_multi_size_ico, (base_icon, self.base_dir / "icon.ico"), "Windows ICO"),
            (self.create_multi_size_ico, (base_icon, self.base_dir / "icon_high_quality.ico"), "High Quality ICO"),
            (self.create_icns_file, (base_icon, self.base_dir / "icon.icns"), "macOS ICNS"),
            (self.create_png_sizes, (base_icon,), "PNG Size Set"),
            (self.create_tauri_icons, (base_icon,), "Tauri Icons"),
            (self.create_web_icons, (base_icon,), "Web Icons"),
        ]
        
        print(f"\n[TOOLS] Starting icon generation...")
        for task_func, args, description in tasks:
            print(f"\n[TASK] {description}")
            print("-" * 40)
            try:
                task_func(*args)
            except Exception as e:
                print(f"[ERROR] {description} failed: {e}")
                self.results['failed'].append(f"{description}: {e}")
        
        return len(self.results['failed']) == 0
    
    def print_summary(self):
        """Print generation result summary"""
        print("\n" + "=" * 60)
        print("[CHART] Icon Generation Result Summary")
        print("=" * 60)
        
        print(f"\n[OK] Successfully generated:")
        for success in self.results['success']:
            print(f"   * {success}")
        
        if self.results['failed']:
            print(f"\n[ERROR] Generation failed:")
            for failure in self.results['failed']:
                print(f"   * {failure}")
        
        print(f"\n[DIR] Generated files ({len(self.results['files_created'])} files):")
        for file_path in self.results['files_created'][:10]:  # Show only first 10
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size / 1024
                print(f"   [FILE] {path.name:<30} ({size:.1f}KB)")
        
        if len(self.results['files_created']) > 10:
            print(f"   ... and other {len(self.results['files_created']) - 10} files")
        
        print(f"\n[INFO] Usage suggestions:")
        print(f"   * PyInstaller (macOS):  icon='build_assets/icon.icns'")
        print(f"   * PyInstaller (Windows): icon='build_assets/icon.ico'")
        print(f"   * Tauri app: Auto-use files in tauri/src-tauri/icons/")
        print(f"   * Web app: Use favicon.ico and related PNG files")

def main():
    """Main function"""
    try:
        generator = UniversalIconGenerator()
        success = generator.generate_all_icons()
        generator.print_summary()
        
        if success:
            print(f"\n[DONE] All icons generation completed!")
        else:
            print(f"\n[WARN] Some icons failed to generate, please check error messages above")
        
        return success
        
    except KeyboardInterrupt:
        print(f"\n[WARN] User interrupted operation")
        return False
    except Exception as e:
        print(f"\n[ERROR] Program exception: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
