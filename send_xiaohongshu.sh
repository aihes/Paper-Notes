#!/bin/bash
set -e

# 第一个参数作为 account
ACCOUNT=$1

if [ -z "$ACCOUNT" ]; then
  echo "Usage: $0 <account_name>"
  exit 1
fi

python3 src/utils/send_xiaohongshu.py --account "$ACCOUNT"
