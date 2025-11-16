#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地截图并远程发布工作流

功能:
1.  调用 capture_full_page.py 在本地对指定 URL 进行截图并提取文本内容。
2.  调用 upload_image.py 将本地截图上传到远程服务器，获取图片链接。
3.  调用 send_xiaohongshu.py 将文本内容和图片链接发布出去。
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# --- 设置项目根目录 ---
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

# --- 导入项目内模块 ---
from src.utils.capture_full_page import capture_full_page
from src.utils.upload_image import image_path_to_base64_uri, upload_image_from_base64
from src.utils.send_xiaohongshu import publish_to_xiaohongshu, ACCOUNT_PRESETS

# ============================================================================
# 配置
# ============================================================================
load_dotenv()
LOGS_DIR = project_root / "logs"

# ============================================================================
# 颜色输出
# ============================================================================
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_step(msg: str):
    print(f"\n{Colors.BLUE}➡️  {msg}{Colors.NC}")

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.NC}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.NC}")

def print_info(msg: str):
    print(f"   {Colors.BLUE}ℹ️  {msg}{Colors.NC}")

# ============================================================================
# 核心工作流
# ============================================================================

async def run_local_capture_and_publish(url: str, account: str, width: int, limit: int):
    """
    执行完整的本地截图、上传和发布流程。
    """
    try:
        # --- 步骤 1: 本地截图和内容提取 ---
        print_step("步骤 1/3: 正在本地进行截图和内容提取...")
        capture_result = await capture_full_page(
            url=url,
            output_base_dir=str(LOGS_DIR),
            width=width,
            limit=limit
        )

        for log in capture_result.get("logs", []):
            print(f"   {log}")

        if not capture_result.get("success"):
            raise Exception(f"截图失败: {capture_result.get('error', '未知错误')}")
        
        screenshot_paths = capture_result.get("screenshot_paths", [])
        text_content = capture_result.get("text_content", "")

        if not screenshot_paths:
            print_warning("未生成任何截图，将只发布文本内容。")
        if not text_content.strip():
            print_warning("提取的文本内容为空。")

        # --- 步骤 2: 上传图片 ---
        print_step("步骤 2/3: 正在上传截图到服务器...")
        uploaded_image_urls = []
        for image_path_str in screenshot_paths:
            image_path = Path(image_path_str)
            print_info(f"正在处理图片: {image_path.name}")
            
            # 1. 转换为 Base64
            base64_uri = image_path_to_base64_uri(image_path)
            if not base64_uri:
                print_warning(f"转换 Base64 失败: {image_path.name}")
                continue
            
            # 2. 上传
            image_url = upload_image_from_base64(base64_uri, image_path.name)
            if image_url:
                uploaded_image_urls.append(image_url)
                print_info(f"上传成功: {image_url}")
            else:
                print_warning(f"上传失败: {image_path.name}")
        
        if screenshot_paths and not uploaded_image_urls:
             raise Exception("所有图片都上传失败，任务终止。")
        
        print_success(f"成功上传 {len(uploaded_image_urls)} 张图片。")

        # --- 步骤 3: 发布内容 ---
        print_step("步骤 3/3: 正在发布内容到小红书...")

        # 获取账号预设标签
        account_preset = ACCOUNT_PRESETS.get(account.lower())
        tags = None
        if account_preset:
            tags = account_preset.get('default_tags')
            print_info(f"使用预设账号 '{account}' 的标签: {tags}")
        else:
            print_warning(f"账号 '{account}' 没有预设配置，不使用默认标签。")
        
        # 执行发布
        publish_result = publish_to_xiaohongshu(
            content=text_content,
            account=account,
            tags=tags,
            enable_cover=False,  # 根据业务逻辑，这里通常不需要再生成封面
            content_images=uploaded_image_urls
        )
        
        print_success("发布请求已发送！")
        print_info("服务器响应:")
        print(json.dumps(publish_result, ensure_ascii=False, indent=2))

    except Exception as e:
        print_error(f"工作流执行失败: {e}")
        sys.exit(1)


# ============================================================================
# 主函数
# ============================================================================

async def main():
    parser = argparse.ArgumentParser(
        description="本地截图并远程发布工作流。",
        epilog="示例: python src/utils/local_capture_and_publish.py --url https://www.example.com --account aihe --limit 10"
    )
    parser.add_argument('--url', '-u', required=True, help='需要截图和发布的URL')
    parser.add_argument('--account', '-a', required=True, help=f'发布账号 (可选: {", ".join(ACCOUNT_PRESETS.keys())})')
    parser.add_argument('--width', '-w', type=int, default=800, help='截图宽度 (默认: 800)')
    parser.add_argument('--limit', '-l', type=int, default=10, help='最大截图数量 (0为不限制, 默认: 10)')
    
    args = parser.parse_args()

    print("=" * 70)
    print(f"{Colors.GREEN}🚀 开始执行本地截图并远程发布工作流 🚀{Colors.NC}")
    print("=" * 70)

    await run_local_capture_and_publish(
        url=args.url,
        account=args.account,
        width=args.width,
        limit=args.limit
    )

    print("\n" + "=" * 70)
    print(f"{Colors.GREEN}🎉 工作流执行完毕！ 🎉{Colors.NC}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())