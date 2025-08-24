from PIL import Image, ImageDraw, ImageFilter


def create_gradient(
    size: int, start_color: tuple, end_color: tuple
) -> Image.Image:
    base = Image.new("RGB", (size, size), start_color)
    top = Image.new("RGB", (size, size), end_color)
    mask = Image.linear_gradient("L").resize((size, size))
    return Image.composite(top, base, mask)


def rounded_rect_mask(size: int, radius: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return mask


def create_icon_png(size: int = 512) -> Image.Image:
    # 背景渐变：靛蓝 → 青色
    gradient = create_gradient(size, (79, 70, 229), (6, 182, 212))

    # 圆角矩形裁剪
    mask = rounded_rect_mask(size, radius=int(size * 0.18))
    gradient.putalpha(mask)

    # 添加内阴影/高光
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([
        int(size * 0.05),
        int(size * 0.55),
        int(size * 0.95),
        int(size * 0.95)
    ], fill=(0, 0, 0, 40))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=int(size * 0.04)))

    # 前景徽记：简洁的条形图形状
    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fgd = ImageDraw.Draw(fg)
    bar_w = int(size * 0.12)
    margin = int(size * 0.18)
    gap = int(size * 0.06)
    bottom = size - margin
    colors = [(255, 255, 255, a) for a in (220, 235, 255)]
    heights = [0.45, 0.65, 0.85]
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

    # 合成
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(gradient)
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(fg)
    return canvas


def save_ico(img: Image.Image, path: str):
    # 生成多尺寸 ICO
    sizes = [16, 24, 32, 48, 64, 128, 256]
    imgs = [img.resize((s, s), Image.LANCZOS) for s in sizes]
    imgs[0].save(path, format="ICO", sizes=[(s, s) for s in sizes])


if __name__ == "__main__":
    icon_png = create_icon_png(512)
    # 同步输出 ico 到工作目录
    save_ico(icon_png, "icon.ico")
    # 同时保存预览 PNG（可选）
    icon_png.save("icon_preview.png")
