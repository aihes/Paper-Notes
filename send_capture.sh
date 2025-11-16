#!/bin/bash

# =================================================================
# 远程截图并发布脚本
#
# 用法:
# ./send_capture.sh <URL>
#
# 示例:
# ./send_capture.sh "https://www.bytedance.com"
# =================================================================

# 默认参数
DEFAULT_ACCOUNT="aihe"
DEFAULT_LIMIT=10
URL=$1

# 检查是否提供了 URL
if [ -z "$URL" ]; then
  echo "错误: 未提供 URL。"
  echo "用法: $0 <URL>"
  exit 1
fi

# 获取脚本所在的目录
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Python 脚本的路径
PYTHON_SCRIPT="$SCRIPT_DIR/src/utils/capture_and_publish.py"

# 检查 Python 脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "错误: Python 脚本未找到于: $PYTHON_SCRIPT"
    exit 1
fi

echo "============================================="
echo "执行截图与发布任务"
echo "============================================="
echo "URL: $URL"
echo "账号: $DEFAULT_ACCOUNT"
echo "图片限制: $DEFAULT_LIMIT"
echo "---------------------------------------------"

# 执行 Python 脚本
python3 "$PYTHON_SCRIPT" \
    --url "$URL" \
    --account "$DEFAULT_ACCOUNT" \
    --limit "$DEFAULT_LIMIT"