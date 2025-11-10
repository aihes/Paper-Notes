#!/usr/bin/env python3
"""
小红书远程发布工具 (Refactored)

功能：读取固定路径的文本文件，通过 API 发送到远程服务器进行发布。
作者：AI Assistant
版本：v2.0
日期：2025-01-22
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

# Add project root to Python path
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

# 固定的输入文件路径
INPUT_FILE_PATH = project_root / "x_content" / "twitter_post.txt"

# 预设账号配置
ACCOUNT_PRESETS = {
    "he": {
        "account_type": "default",
        "watermark": "@AI贺",
        "default_tags": "分享,干货"
    },
    "eric": {
        "account_type": "product_manager",
        "watermark": "@Eric.AI",
        "default_tags": "产品经理,职场"
    },
    "conrad": {
        "account_type": "default",
        "watermark": "@Conrad",
        "default_tags": "分享,学习"
    },
    "aihe": {
        "account_type": "default",
        "watermark": "@AI贺",
        "default_tags": "AI,技术"
    }
}

# ============================================================================
# 颜色输出 (保持不变)
# ============================================================================

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.NC}")

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.NC}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.NC}")

# ============================================================================
# 核心功能
# ============================================================================

def read_input_file(file_path: Path) -> str:
    """读取输入文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            raise ValueError("文件内容为空")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}")
    except Exception as e:
        raise Exception(f"读取文件失败: {e}")


def publish_to_xiaohongshu(
    content: str,
    account: str,
    title: Optional[str] = None,
    tags: Optional[str] = None,
    enable_cover: bool = True
) -> dict:
    """发布内容到小红书远程服务器"""
    if not REMOTE_API_URL or not API_KEY:
        raise ValueError("请在 .env 文件中或环境变量里设置 XHS_API_URL 和 XHS_API_KEY")

    endpoint = urljoin(REMOTE_API_URL, "api/ai-publish")
    
    data = {
        "content": content,
        "account": account,
        "enable_cover": enable_cover
    }
    
    if title:
        data["title"] = title
    if tags:
        data["tags"] = tags
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    try:
        print_info(f"正在发送请求到: {endpoint}")
        print_info(f"账号: {account}")
        
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        error_msg = f"请求失败: {e}"
        if e.response:
            error_msg += f"\n状态码: {e.response.status_code}\n响应: {e.response.text}"
        raise Exception(error_msg)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="小红书远程发布工具 (Refactored)")
    parser.add_argument('--account', '-a', required=True, help='账号名称 (例如: eric, he, conrad, aihe)')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print(f"{Colors.GREEN}小红书远程发布工具 (Refactored){Colors.NC}")
    print("=" * 70 + "\n")
    
    try:
        # 1. 读取固定文件
        print_info(f"读取输入文件: {INPUT_FILE_PATH}")
        content = read_input_file(INPUT_FILE_PATH)
        print_success(f"成功读取文件，内容长度: {len(content)} 字符")
        
        # 2. 获取账号预设
        account_preset = ACCOUNT_PRESETS.get(args.account.lower())
        tags = None
        if account_preset:
            print_info(f"使用预设账号配置: {args.account}")
            tags = account_preset.get('default_tags')
            if tags:
                print_info(f"使用预设标签: {tags}")
        else:
            print_warning(f"账号 '{args.account}' 没有预设配置，不使用默认标签")
        
        # 3. 发布
        result = publish_to_xiaohongshu(
            content=content,
            account=args.account,
            tags=tags
        )
        
        # 4. 显示结果
        print("\n" + "-" * 70)
        print_info("服务器响应:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("-" * 70 + "\n")

        task_id = result.get('task_id')
        message = result.get('message', '无详细信息')

        if task_id:
            print_success("发布任务已成功创建或入队！")
            print_info(f"任务 ID: {task_id}")
            print_info(f"消息: {message}")
            if REMOTE_API_URL:
                screenshot_path = f"screenshots?taskId={task_id}"
                screenshot_url = urljoin(REMOTE_API_URL, screenshot_path)
                print_info(f"任务状态链接: {screenshot_url}")
        elif result.get('success'):
             print_success(f"操作成功: {message}")
        else:
            print_error(f"发布失败: {message}")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"发生严重错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
