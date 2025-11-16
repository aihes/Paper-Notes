#!/bin/bash

# =================================================================
# 本地截图并远程发布脚本
#
# 此脚本会调用 Python 工作流，执行以下步骤:
# 1. 本地对 URL 进行截图并提取文本。
# 2. 将截图上传到服务器。
# 3. 将文本和图片链接发布出去。
#
# 用法:
# ./send_local_capture.sh <URL>
#
# 示例:
# ./send_local_capture.sh "https://github.com/features/actions"
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
PYTHON_SCRIPT="$SCRIPT_DIR/src/utils/local_capture_and_publish.py"

# 检查 Python 脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "错误: Python 脚本未找到于: $PYTHON_SCRIPT"
    exit 1
fi

# 执行 Python 脚本
python3 "$PYTHON_SCRIPT" \
    --url "$URL" \
    --account "$DEFAULT_ACCOUNT" \
    --limit "$DEFAULT_LIMIT"