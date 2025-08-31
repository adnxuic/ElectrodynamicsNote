#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片转PDF工具
将imgs文件夹中的所有非PDF图片转换为PDF格式
"""

import os
from PIL import Image
import glob

def convert_images_to_pdf():
    """
    将当前目录下的所有图片文件转换为PDF格式
    支持的图片格式：PNG, JPG, JPEG, GIF, BMP, TIFF
    """
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"正在处理目录: {current_dir}")
    
    # 支持的图片格式
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.tiff', '*.tif']
    
    # 转换计数器
    converted_count = 0
    
    # 遍历所有支持的图片格式
    for extension in image_extensions:
        # 查找匹配的文件（不区分大小写）
        files = glob.glob(os.path.join(current_dir, extension.lower()))
        files.extend(glob.glob(os.path.join(current_dir, extension.upper())))
        
        for image_path in files:
            try:
                # 获取文件名（不包含扩展名）
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                pdf_path = os.path.join(current_dir, f"{base_name}.pdf")
                
                # 检查PDF文件是否已存在
                if os.path.exists(pdf_path):
                    print(f"跳过 {os.path.basename(image_path)} - PDF文件已存在")
                    continue
                
                # 打开图片
                print(f"正在转换: {os.path.basename(image_path)}")
                with Image.open(image_path) as img:
                    # 如果图片是RGBA模式，转换为RGB
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # 创建白色背景
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = rgb_img
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # 保存为PDF
                    img.save(pdf_path, "PDF", quality=95)
                    print(f"✓ 成功转换: {base_name}.pdf")
                    converted_count += 1
                    
            except Exception as e:
                print(f"✗ 转换失败 {os.path.basename(image_path)}: {str(e)}")
    
    print(f"\n转换完成！共转换了 {converted_count} 个文件。")
    
    if converted_count == 0:
        print("没有找到需要转换的图片文件。")
        print("支持的格式：PNG, JPG, JPEG, GIF, BMP, TIFF")

def main():
    """主函数"""
    print("=" * 50)
    print("图片转PDF工具")
    print("=" * 50)
    
    try:
        convert_images_to_pdf()
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {str(e)}")
    
    print("\n按任意键退出...")

if __name__ == "__main__":
    main()
