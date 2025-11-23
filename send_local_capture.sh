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
# ./send_local_capture.sh <URL> [WIDTH]
#
# 示例:
# ./send_local_capture.sh "https://github.com/features/actions" 800
# =================================================================

# 默认参数
DEFAULT_ACCOUNT="aihe"
DEFAULT_LIMIT=10
URL=$1
WIDTH=$2

# 检查是否提供了 URL
if [ -z "$URL" ]; then
  echo "错误: 未提供 URL。"
  echo "用法: $0 <URL> [WIDTH]"
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

# 构建参数列表
ARGS=("--url" "$URL" "--account" "$DEFAULT_ACCOUNT" "--limit" "$DEFAULT_LIMIT")

# 如果提供了宽度，则将其添加到参数列表中
if [ -n "$WIDTH" ]; then
  ARGS+=("--width" "$WIDTH")
fi

# 如果 URL 是 GitHub 域名，则添加交换顺序的标志
if [[ "$URL" == *"github.com"* ]]; then
  ARGS+=("--swap-first-two")
fi

# 执行 Python 脚本并传递所有参数
echo "正在执行: python3 $PYTHON_SCRIPT ${ARGS[@]}"
python3 "$PYTHON_SCRIPT" "${ARGS[@]}"