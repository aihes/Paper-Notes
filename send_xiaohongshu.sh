#!/bin/bash
set -e

# 检查是否提供了必要的参数
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <text_file_path> <image_urls_file_path>"
  exit 1
fi

TEXT_FILE=$1
IMAGE_URLS_FILE=$2
ACCOUNT="aihe"

# 检查文本文件是否存在
if [ ! -f "$TEXT_FILE" ]; then
  echo "Error: Text file not found at $TEXT_FILE"
  exit 1
fi

CMD="python3 src/utils/send_xiaohongshu.py --account \"$ACCOUNT\" --input-file \"$TEXT_FILE\""

# 如果图片 URL 文件存在，则添加参数
if [ -f "$IMAGE_URLS_FILE" ]; then
    CMD="$CMD --image-urls-file \"$IMAGE_URLS_FILE\""
fi

eval $CMD
