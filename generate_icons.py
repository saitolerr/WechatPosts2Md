#!/usr/bin/env python3
"""
生成插件图标 - 现代风格
运行: python generate_icons.py
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

def create_icon(size, output_path):
    """创建一个现代风格的图标"""
    # 创建图像（带透明背景）
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变背景（圆角矩形）
    padding = max(1, size // 12)
    radius = size // 5
    
    # 使用渐变色背景 - 从绿色到青色（微信风格）
    for i in range(size - 2 * padding):
        # 渐变从上到下
        ratio = i / (size - 2 * padding)
        r = int(7 + (16 - 7) * ratio)      # 07 -> 10
        g = int(193 + (185 - 193) * ratio)  # C1 -> B9
        b = int(96 + (127 - 96) * ratio)    # 60 -> 7F
        
        y = padding + i
        # 绘制水平线
        draw.line([(padding, y), (size - padding, y)], fill=(r, g, b, 255))
    
    # 创建圆角蒙版
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [padding, padding, size - padding, size - padding],
        radius=radius,
        fill=255
    )
    
    # 应用蒙版
    img.putalpha(mask)
    
    # 重新获取 draw 对象
    draw = ImageDraw.Draw(img)
    
    # 绘制 Markdown 符号 "M↓" 或简单的文档图标
    # 使用白色绘制一个简化的 Markdown 标志
    
    center_x = size // 2
    center_y = size // 2
    
    # 方案：绘制 "MD" 文字或 Markdown 的 "#" 符号
    # 这里绘制一个简洁的下载箭头 + 文档图标
    
    # 文档轮廓
    doc_width = size * 0.45
    doc_height = size * 0.55
    doc_left = center_x - doc_width // 2
    doc_top = center_y - doc_height // 2 - size * 0.02
    doc_right = doc_left + doc_width
    doc_bottom = doc_top + doc_height
    fold_size = size * 0.12
    
    # 文档主体（带折角）- 白色半透明
    doc_points = [
        (doc_left, doc_top),
        (doc_right - fold_size, doc_top),
        (doc_right, doc_top + fold_size),
        (doc_right, doc_bottom),
        (doc_left, doc_bottom),
    ]
    draw.polygon(doc_points, fill=(255, 255, 255, 240))
    
    # 折角阴影
    fold_points = [
        (doc_right - fold_size, doc_top),
        (doc_right, doc_top + fold_size),
        (doc_right - fold_size, doc_top + fold_size),
    ]
    draw.polygon(fold_points, fill=(200, 230, 210, 200))
    
    # 在文档上绘制 Markdown 的 "#" 符号
    hash_color = (7, 193, 96, 255)  # 微信绿
    line_width = max(1, size // 20)
    
    # 简化：绘制两条横线代表文本
    line_left = doc_left + size * 0.08
    line_right = doc_right - size * 0.08
    line_y1 = doc_top + doc_height * 0.35
    line_y2 = doc_top + doc_height * 0.50
    line_y3 = doc_top + doc_height * 0.65
    line_height = max(2, size // 18)
    
    # 第一行（较长）
    draw.rounded_rectangle(
        [line_left, line_y1, line_right, line_y1 + line_height],
        radius=line_height // 2,
        fill=hash_color
    )
    # 第二行（中等）
    draw.rounded_rectangle(
        [line_left, line_y2, line_right - size * 0.1, line_y2 + line_height],
        radius=line_height // 2,
        fill=hash_color
    )
    # 第三行（较短）
    draw.rounded_rectangle(
        [line_left, line_y3, line_right - size * 0.18, line_y3 + line_height],
        radius=line_height // 2,
        fill=hash_color
    )
    
    # 保存
    img.save(output_path, 'PNG')
    print(f"Created: {output_path}")


def create_icon_v2(size, output_path):
    """创建第二种风格的图标 - 更简洁"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    padding = max(1, size // 10)
    radius = size // 4
    
    # 深色背景
    draw.rounded_rectangle(
        [padding, padding, size - padding, size - padding],
        radius=radius,
        fill=(30, 41, 59, 255)  # 深蓝灰色
    )
    
    # 绘制 "MD" 文字
    center_x = size // 2
    center_y = size // 2
    
    # M 的绘制
    m_width = size * 0.35
    m_height = size * 0.35
    m_left = center_x - m_width - size * 0.02
    m_top = center_y - m_height // 2
    line_w = max(2, size // 12)
    
    # 简化的 M
    m_color = (74, 222, 128, 255)  # 亮绿色
    
    # M 的左竖线
    draw.rectangle([m_left, m_top, m_left + line_w, m_top + m_height], fill=m_color)
    # M 的右竖线
    draw.rectangle([m_left + m_width - line_w, m_top, m_left + m_width, m_top + m_height], fill=m_color)
    # M 的中间 V
    mid_x = m_left + m_width // 2
    mid_y = m_top + m_height * 0.6
    # 左斜线
    for i in range(int(line_w * 1.5)):
        x1 = m_left + line_w + i
        y1 = m_top
        x2 = mid_x + i - line_w // 2
        y2 = mid_y
        draw.line([(x1, y1), (x2, y2)], fill=m_color, width=1)
    # 右斜线
    for i in range(int(line_w * 1.5)):
        x1 = mid_x + i - line_w // 2
        y1 = mid_y
        x2 = m_left + m_width - line_w + i
        y2 = m_top
        draw.line([(x1, y1), (x2, y2)], fill=m_color, width=1)
    
    # 向下箭头
    arrow_left = center_x + size * 0.05
    arrow_size = size * 0.25
    arrow_color = (96, 165, 250, 255)  # 蓝色
    
    # 箭头竖线
    arrow_x = arrow_left + arrow_size // 2
    draw.rectangle([arrow_x - line_w // 2, m_top, arrow_x + line_w // 2, m_top + m_height * 0.65], fill=arrow_color)
    
    # 箭头头部
    arrow_tip_y = m_top + m_height
    arrow_tip_x = arrow_x
    arrow_head_width = size * 0.12
    
    draw.polygon([
        (arrow_tip_x, arrow_tip_y),
        (arrow_tip_x - arrow_head_width, arrow_tip_y - arrow_head_width),
        (arrow_tip_x + arrow_head_width, arrow_tip_y - arrow_head_width),
    ], fill=arrow_color)
    
    img.save(output_path, 'PNG')
    print(f"Created: {output_path}")


def create_icon_v3(size, output_path):
    """创建第三种风格 - 微信绿 + 简洁文档"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    padding = max(1, size // 10)
    radius = size // 4
    
    # 微信绿渐变背景
    # 从 #07C160 到 #06AD56
    draw.rounded_rectangle(
        [padding, padding, size - padding, size - padding],
        radius=radius,
        fill=(7, 193, 96, 255)
    )
    
    center_x = size // 2
    center_y = size // 2
    
    # 白色文档图标
    doc_w = size * 0.42
    doc_h = size * 0.52
    doc_left = center_x - doc_w // 2
    doc_top = center_y - doc_h // 2
    fold = size * 0.1
    
    # 文档主体
    draw.polygon([
        (doc_left, doc_top),
        (doc_left + doc_w - fold, doc_top),
        (doc_left + doc_w, doc_top + fold),
        (doc_left + doc_w, doc_top + doc_h),
        (doc_left, doc_top + doc_h),
    ], fill=(255, 255, 255, 255))
    
    # 折角
    draw.polygon([
        (doc_left + doc_w - fold, doc_top),
        (doc_left + doc_w, doc_top + fold),
        (doc_left + doc_w - fold, doc_top + fold),
    ], fill=(220, 240, 230, 255))
    
    # 文档内的 "#" 符号代表 Markdown
    hash_color = (7, 193, 96, 255)
    hash_x = center_x
    hash_y = center_y + size * 0.03
    hash_size = size * 0.22
    line_w = max(2, size // 16)
    
    # 绘制 # 符号
    # 两条竖线
    draw.rectangle([
        hash_x - hash_size * 0.3, hash_y - hash_size * 0.4,
        hash_x - hash_size * 0.3 + line_w, hash_y + hash_size * 0.4
    ], fill=hash_color)
    draw.rectangle([
        hash_x + hash_size * 0.15, hash_y - hash_size * 0.4,
        hash_x + hash_size * 0.15 + line_w, hash_y + hash_size * 0.4
    ], fill=hash_color)
    
    # 两条横线
    draw.rectangle([
        hash_x - hash_size * 0.45, hash_y - hash_size * 0.15,
        hash_x + hash_size * 0.45, hash_y - hash_size * 0.15 + line_w
    ], fill=hash_color)
    draw.rectangle([
        hash_x - hash_size * 0.45, hash_y + hash_size * 0.15,
        hash_x + hash_size * 0.45, hash_y + hash_size * 0.15 + line_w
    ], fill=hash_color)
    
    img.save(output_path, 'PNG')
    print(f"Created: {output_path}")


def main():
    icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    # 使用第三种风格（微信绿 + Markdown # 符号）
    sizes = [16, 48, 128]
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon{size}.png')
        create_icon_v3(size, output_path)
    
    print("\n✅ Done! Icons created in 'icons/' folder.")
    print("风格：微信绿背景 + 白色文档 + Markdown # 符号")


if __name__ == '__main__':
    main()
