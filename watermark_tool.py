#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags
import piexif


def get_image_creation_date(image_path):
    """从图片的EXIF信息中提取拍摄日期时间"""
    try:
        img = Image.open(image_path)
        # 尝试通过piexif库获取EXIF信息
        try:
            exif_dict = piexif.load(img.info['exif'])
            if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
                date_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
                # 格式通常是"YYYY:MM:DD HH:MM:SS"
                try:
                    date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    # 尝试其他常见格式
                    pass
        except (KeyError, AttributeError, piexif.InvalidImageDataError):
            # 如果piexif失败，尝试使用PIL的ExifTags
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        try:
                            date_obj = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                            return date_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            pass
        
        # 如果无法获取EXIF信息，返回文件的修改时间
        file_mtime = os.path.getmtime(image_path)
        date_obj = datetime.fromtimestamp(file_mtime)
        return date_obj.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"无法获取图片{image_path}的拍摄日期: {e}")
        # 返回当前日期作为后备选项
        return datetime.now().strftime('%Y-%m-%d')

def add_watermark(image_path, output_path, text, font_size, color, position):
    """给图片添加文字水印"""
    try:
        # 打开图片
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # 尝试加载系统字体，如果失败则使用默认字体
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
            except IOError:
                font = ImageFont.load_default()
        
        # 获取文本大小
        text_width, text_height = draw.textsize(text, font=font)
        
        # 确定水印位置
        img_width, img_height = img.size
        
        if position == 'top_left':
            x, y = 10, 10
        elif position == 'top_right':
            x, y = img_width - text_width - 10, 10
        elif position == 'bottom_left':
            x, y = 10, img_height - text_height - 10
        elif position == 'bottom_right':
            x, y = img_width - text_width - 10, img_height - text_height - 10
        elif position == 'center':
            x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
        else:
            # 默认位置为右下角
            x, y = img_width - text_width - 10, img_height - text_height - 10
        
        # 绘制水印（添加阴影效果增强可读性）
        draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, 128))  # 阴影
        draw.text((x, y), text, font=font, fill=color)
        
        # 保存图片
        img.save(output_path)
        print(f"已保存带水印的图片到: {output_path}")
        return True
    except Exception as e:
        print(f"处理图片{image_path}时出错: {e}")
        return False

def process_images(input_path, font_size, color, position):
    """处理指定路径下的所有图片文件"""
    # 检查输入路径是否存在
    if not os.path.exists(input_path):
        print(f"错误：路径 {input_path} 不存在")
        return
    
    # 创建输出目录
    output_dir = f"{input_path}_watermark"
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取要处理的文件列表
    if os.path.isfile(input_path):
        # 如果输入是单个文件
        files_to_process = [os.path.basename(input_path)]
        input_dir = os.path.dirname(input_path)
        if not input_dir:
            input_dir = '.'
    else:
        # 如果输入是目录
        files_to_process = [f for f in os.listdir(input_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        input_dir = input_path
    
    # 处理每个文件
    for filename in files_to_process:
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path):
            continue
        
        # 获取拍摄日期作为水印文本
        watermark_text = get_image_creation_date(file_path)
        
        # 创建输出文件路径
        base_name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{base_name}_watermark{ext}")
        
        # 添加水印并保存
        add_watermark(file_path, output_path, watermark_text, font_size, color, position)


def parse_color(color_str):
    """解析颜色字符串为RGBA元组"""
    # 支持的预定义颜色
    colors = {
        'black': (0, 0, 0, 255),
        'white': (255, 255, 255, 255),
        'red': (255, 0, 0, 255),
        'green': (0, 255, 0, 255),
        'blue': (0, 0, 255, 255),
        'yellow': (255, 255, 0, 255),
        'cyan': (0, 255, 255, 255),
        'magenta': (255, 0, 255, 255)
    }
    
    # 检查是否是预定义颜色
    if color_str.lower() in colors:
        return colors[color_str.lower()]
    
    # 尝试解析HEX颜色代码
    if color_str.startswith('#'):
        try:
            # 去除#号
            color_str = color_str.lstrip('#')
            # 解析RGB值
            r = int(color_str[0:2], 16)
            g = int(color_str[2:4], 16)
            b = int(color_str[4:6], 16)
            # 如果有alpha通道
            a = 255
            if len(color_str) == 8:
                a = int(color_str[6:8], 16)
            return (r, g, b, a)
        except ValueError:
            pass
    
    # 默认返回白色
    print(f"警告：无法解析颜色 '{color_str}'，使用默认颜色白色")
    return (255, 255, 255, 255)

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='给图片添加基于拍摄日期的水印')
    parser.add_argument('path', help='图片文件路径或包含图片的目录路径')
    parser.add_argument('--font-size', type=int, default=30, help='水印字体大小（默认：30）')
    parser.add_argument('--color', default='white', help='水印颜色，可以是预定义颜色或HEX代码（默认：white）')
    parser.add_argument('--position', choices=['top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'], 
                        default='bottom_right', help='水印位置（默认：bottom_right）')
    
    args = parser.parse_args()
    
    # 解析颜色
    color = parse_color(args.color)
    
    # 处理图片
    process_images(args.path, args.font_size, color, args.position)


if __name__ == "__main__":
    main()