#!/bin/bash
set -e

# 1. 检查参数
if [ -z "$1" ]; then
  echo "错误：请提供源目录作为第一个参数。"
  echo "用法: ./send_all.sh <path_to_source_directory>"
  exit 1
fi

SOURCE_DIR=$1
TEMP_CONTENT_DIR="./x_content"
TEXT_FILE="$TEMP_CONTENT_DIR/twitter_post.txt"
IMAGE_DIR="$TEMP_CONTENT_DIR/images"
IMAGE_URLS_FILE="$TEMP_CONTENT_DIR/image_urls.txt"

# 2. 激活虚拟环境
VENV_PATH="./.venv"
if [ -d "$VENV_PATH" ]; then
  echo "激活虚拟环境..."
  source "$VENV_PATH/bin/activate"
else
  echo "警告：未找到虚拟环境 '.venv'。将使用系统默认 Python。"
fi

# 3. 内容预处理
echo "--- 1. 内容预处理 ---"
python scripts/prepare_content.py "$SOURCE_DIR"
if [ $? -ne 0 ]; then
  echo "错误：内容预处理失败。"
  exit 1
fi
echo "预处理完成。"

# 4. 上传图片
echo "--- 2. 上传图片 ---"
if [ -d "$IMAGE_DIR" ] && [ -n "$(ls -A "$IMAGE_DIR")" ]; then
  python src/utils/upload_image.py --image-dir "$IMAGE_DIR" --output-file "$IMAGE_URLS_FILE"
  if [ $? -ne 0 ]; then
    echo "错误：图片上传失败。"
    exit 1
  fi
  echo "图片上传完成。"
else
  echo "未发现图片，将创建空的 URL 文件。"
  touch "$IMAGE_URLS_FILE"
fi

# 5. 发布到 X (Twitter)
echo "--- 3. 发布到 X (Twitter) ---"
./send_x.sh "$TEXT_FILE" "$IMAGE_URLS_FILE"
if [ $? -ne 0 ]; then
  echo "错误：发布到 X (Twitter) 失败。"
  exit 1
fi
echo "X (Twitter) 发布成功。"

# 等待10秒
echo "等待 10 秒..."
sleep 10

# 6. 发布到小红书
echo "--- 4. 发布到小红书 ---"
./send_xiaohongshu.sh "$TEXT_FILE" "$IMAGE_URLS_FILE"
if [ $? -ne 0 ]; then
  echo "错误：发布到小红书失败。"
  exit 1
fi
echo "小红书发布成功。"

echo "---"
echo "所有平台的发布任务均已成功完成！"