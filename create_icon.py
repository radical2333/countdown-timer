#!/usr/bin/env python3
# 创建应用程序图标
from PIL import Image, ImageDraw, ImageFont
import os

# 创建64x64像素的图标
size = 64
image = Image.new('RGBA', (size, size), (52, 152, 219, 255))  # 蓝色背景
draw = ImageDraw.Draw(image)

# 绘制时钟外圈
draw.ellipse([4, 4, size-4, size-4], outline=(44, 62, 80, 255), width=3)

# 绘制时针和分针
center = size // 2
draw.line([center, 14, center, center], fill=(44, 62, 80, 255), width=3)  # 时针
draw.line([center, center, center+12, center], fill=(44, 62, 80, 255), width=2)  # 分针

# 绘制中心点
draw.ellipse([center-3, center-3, center+3, center+3], fill=(44, 62, 80, 255))

# 保存图标
image.save('icon.png', 'PNG')
print("图标创建完成: icon.png")
