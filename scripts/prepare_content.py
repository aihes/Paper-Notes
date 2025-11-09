# scripts/prepare_content.py
import os
import shutil
import sys
import glob

def find_twitter_post_file(source_dir):
    """在源目录中查找包含 'twitter' 的文本文件。"""
    # 优先查找 txt 文件，其次是 md 文件
    for extension in ["*.txt", "*.md"]:
        for filepath in glob.glob(os.path.join(source_dir, f"**/*twitter*{extension}"), recursive=True):
            return filepath
    return None

def find_image_files(source_dir):
    """查找源目录下的所有图片文件。"""
    image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp"]
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(source_dir, f"**/{ext}"), recursive=True))
    return image_files

def main(source_dir):
    x_content_dir = "x_content"
    images_target_dir = os.path.join(x_content_dir, "images")
    text_target_path = os.path.join(x_content_dir, "twitter_post.txt")

    # 1. 清空 x_content 目录，但保留 images 子目录
    for item in os.listdir(x_content_dir):
        item_path = os.path.join(x_content_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
    
    # 清空 images 子目录
    if os.path.exists(images_target_dir):
        for item in os.listdir(images_target_dir):
            item_path = os.path.join(images_target_dir, item)
            os.remove(item_path)
    else:
        os.makedirs(images_target_dir)

    # 2. 查找并复制 twitter 文本文件
    text_file_source = find_twitter_post_file(source_dir)
    if text_file_source:
        shutil.copy(text_file_source, text_target_path)
        print(f"已将 {text_file_source} 复制到 {text_target_path}")
    else:
        print(f"警告：在 '{source_dir}' 中未找到带有 'twitter' 的文本文件。")

    # 3. 查找并复制图片文件
    image_files = find_image_files(source_dir)
    if image_files:
        for image_src in image_files:
            shutil.copy(image_src, images_target_dir)
            print(f"已将 {image_src} 复制到 {images_target_dir}")
    else:
        print(f"警告：在 '{source_dir}' 中未找到图片文件。")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("错误：请提供源目录作为参数。")
        sys.exit(1)
