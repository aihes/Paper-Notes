#!/bin/bash
set -e

# 检查是否提供了文本文件路径参数
if [ -z "$1" ]; then
  echo "Usage: $0 <text_file_path> [image_urls_file_path]"
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

CMD="python src/utils/twitter_publisher.py --account \"$ACCOUNT\" --text \"$TEXT_FILE\""

# 如果图片 URL 文件存在，则添加参数
if [ -n "$IMAGE_URLS_FILE" ] && [ -f "$IMAGE_URLS_FILE" ]; then
  CMD="$CMD --image-urls-file \"$IMAGE_URLS_FILE\""
fi

eval $CMD
