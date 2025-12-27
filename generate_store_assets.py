#!/usr/bin/env python3
"""
生成 Edge 商店需要的素材
"""

from PIL import Image, ImageDraw
import os

def create_store_icon(size, output_path):
    """创建商店图标 (300x300)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    padding = size // 10
    radius = size // 4
    
    # 微信绿背景
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
    
    draw.polygon([
        (doc_left, doc_top),
        (doc_left + doc_w - fold, doc_top),
        (doc_left + doc_w, doc_top + fold),
        (doc_left + doc_w, doc_top + doc_h),
        (doc_left, doc_top + doc_h),
    ], fill=(255, 255, 255, 255))
    
    draw.polygon([
        (doc_left + doc_w - fold, doc_top),
        (doc_left + doc_w, doc_top + fold),
        (doc_left + doc_w - fold, doc_top + fold),
    ], fill=(220, 240, 230, 255))
    
    # Markdown # 符号
    hash_color = (7, 193, 96, 255)
    hash_x = center_x
    hash_y = center_y + size * 0.03
    hash_size = size * 0.22
    line_w = max(2, size // 16)
    
    draw.rectangle([
        hash_x - hash_size * 0.3, hash_y - hash_size * 0.4,
        hash_x - hash_size * 0.3 + line_w, hash_y + hash_size * 0.4
    ], fill=hash_color)
    draw.rectangle([
        hash_x + hash_size * 0.15, hash_y - hash_size * 0.4,
        hash_x + hash_size * 0.15 + line_w, hash_y + hash_size * 0.4
    ], fill=hash_color)
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


def create_promotional_tile(output_path):
    """创建宣传图 (440x280)"""
    width, height = 440, 280
    img = Image.new('RGBA', (width, height), (7, 193, 96, 255))
    draw = ImageDraw.Draw(img)
    
    # 中心文档图标（大号）
    center_x, center_y = width // 2, height // 2
    doc_w, doc_h = 100, 130
    doc_left = center_x - doc_w // 2
    doc_top = center_y - doc_h // 2 - 10
    fold = 20
    
    draw.polygon([
        (doc_left, doc_top),
        (doc_left + doc_w - fold, doc_top),
        (doc_left + doc_w, doc_top + fold),
        (doc_left + doc_w, doc_top + doc_h),
        (doc_left, doc_top + doc_h),
    ], fill=(255, 255, 255, 255))
    
    draw.polygon([
        (doc_left + doc_w - fold, doc_top),
        (doc_left + doc_w, doc_top + fold),
        (doc_left + doc_w - fold, doc_top + fold),
    ], fill=(220, 240, 230, 255))
    
    # # 符号
    hash_color = (7, 193, 96, 255)
    hash_x = center_x
    hash_y = center_y
    line_w = 6
    
    draw.rectangle([hash_x - 15, hash_y - 25, hash_x - 15 + line_w, hash_y + 25], fill=hash_color)
    draw.rectangle([hash_x + 8, hash_y - 25, hash_x + 8 + line_w, hash_y + 25], fill=hash_color)
    draw.rectangle([hash_x - 25, hash_y - 10, hash_x + 25, hash_y - 10 + line_w], fill=hash_color)
    draw.rectangle([hash_x - 25, hash_y + 8, hash_x + 25, hash_y + 8 + line_w], fill=hash_color)
    
    img.save(output_path, 'PNG')
    print(f"Created: {output_path}")


def main():
    store_dir = os.path.join(os.path.dirname(__file__), 'store_assets')
    os.makedirs(store_dir, exist_ok=True)
    
    # 商店图标 300x300
    create_store_icon(300, os.path.join(store_dir, 'icon_300x300.png'))
    
    # 宣传图 440x280 (可选)
    create_promotional_tile(os.path.join(store_dir, 'promo_440x280.png'))
    
    print("\n✅ 商店素材已生成到 store_assets/ 文件夹")
    print("\n还需要：")
    print("1. 截图 (1280x800): 在浏览器中使用插件，然后截图")
    print("2. 描述文案: 见下方")
    
    print("\n" + "="*50)
    print("【简短描述】(不超过132字符)")
    print("="*50)
    print("一键将微信公众号文章转换为 Markdown 格式，保留段落格式和图片。")
    
    print("\n" + "="*50)
    print("【详细描述】")
    print("="*50)
    description = """微信公众号转 Markdown 是一款实用的浏览器扩展，帮助你快速将微信公众号文章转换为 Markdown 格式。

✨ 主要功能：
• 一键提取文章标题、作者、发布时间
• 自动转换正文为 Markdown 格式
• 保留段落空行，格式清晰
• 支持图片、表格、代码块等元素
• 可选择是否包含元信息

📝 使用方法：
1. 在浏览器中打开微信公众号文章
2. 点击插件图标
3. 点击"开始转换"按钮
4. 复制或下载生成的 Markdown 文件

🎯 适用场景：
• 保存公众号文章到本地
• 将文章转移到其他平台
• 整理文章内容
• 二次编辑和排版

注意：由于微信限制，评论区内容只能在微信客户端内查看，无法通过浏览器获取。"""
    
    print(description)


if __name__ == '__main__':
    main()

