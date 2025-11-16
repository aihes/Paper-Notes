#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程截图并发布工具

功能：向远程API发送请求，对指定URL进行截图并发布。
"""

import argparse
import json
import os
import sys
import requests
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from urllib.parse import urljoin

# 将项目根目录添加到Python路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

# ============================================================================
# 配置
# ============================================================================

# 加载环境变量
load_dotenv()

# 从环境变量读取配置
REMOTE_API_URL = os.getenv("XHS_API_URL")
API_KEY = os.getenv("XHS_API_KEY")

# ============================================================================
# 颜色输出
# ============================================================================

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.NC}")

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.NC}")

# ============================================================================
# 核心功能
# ============================================================================

def capture_and_publish(
    url: str,
    account: str,
    width: int,
    limit: int
) -> dict:
    """向远程服务器发送截图和发布请求"""
    if not REMOTE_API_URL or not API_KEY:
        raise ValueError("请在 .env 文件中或环境变量里设置 XHS_API_URL 和 XHS_API_KEY")

    endpoint = urljoin(REMOTE_API_URL, "api/capture-and-publish")

    data = {
        "url": url,
        "account": account,
        "width": width,
        "limit": limit
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    try:
        print_info(f"正在发送请求到: {endpoint}")
        print_info(f"参数: {json.dumps(data, indent=2)}")
        
        response = requests.post(endpoint, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        error_msg = f"请求失败: {e}"
        if e.response:
            error_msg += f"\n状态码: {e.response.status_code}\n响应: {e.response.text}"
        raise Exception(error_msg)

# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="远程截图并发布工具")
    parser.add_argument('--url', '-u', required=True, help='需要截图的URL')
    parser.add_argument('--account', '-a', required=True, help='账号名称')
    parser.add_argument('--width', '-w', type=int, default=750, help='截图宽度，默认为 750')
    parser.add_argument('--limit', '-l', type=int, default=5, help='图片数量限制，默认为 5')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print(f"{Colors.GREEN}远程截图并发布工具{Colors.NC}")
    print("=" * 70 + "\n")
    
    try:
        result = capture_and_publish(
            url=args.url,
            account=args.account,
            width=args.width,
            limit=args.limit
        )
        
        print("\n" + "-" * 70)
        print_info("服务器响应:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("-" * 70 + "\n")

        if result.get('success') or result.get('task_id'):
            print_success("任务已成功创建或执行！")
            if result.get('task_id'):
                 print_info(f"任务 ID: {result.get('task_id')}")
        else:
            print_error(f"操作失败: {result.get('message', '无详细信息')}")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"发生严重错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()