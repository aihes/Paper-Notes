#!/usr/bin/env python3
"""
网页分段完整截图工具

功能:
- 使用 Playwright 启动浏览器并访问指定 URL。
- 循环截图并向下滚动，直到页面底部。
- 将所有截图保存在以时间戳命名的独立目录中。
- 支持自定义输出目录，默认为项目根目录下的 `logs` 文件夹。
- 优化了页面加载逻辑，以处理动态内容和避免不必要的超时。
- 函数 `capture_full_page` 返回一个包含结果的字典，以便在其他模块中调用。
"""

import asyncio
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from typing import Dict, Any, List

async def capture_full_page(url: str, output_base_dir: str, width: int, limit: int) -> Dict[str, Any]:
    """
    对指定 URL 进行分段截图，并返回结果。

    Args:
        url: 目标网页的 URL。
        output_base_dir: 保存截图的根目录。
        width: 浏览器视口的宽度。
        limit: 截图数量限制 (0 表示不限制)。

    Returns:
        一个包含截图结果的字典:
        {
            "success": bool,
            "output_dir": str,
            "screenshot_paths": List[str],
            "text_content": str,
            "text_content_path": str,
            "logs": List[str],
            "error": Optional[str]
        }
    """
    logs: List[str] = []
    
    # 1. 在基础目录下创建以时间戳命名的输出目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(output_base_dir) / f"screenshots_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    logs.append(f"🖼️ 截图将保存在目录: {output_dir}")

    screenshot_paths: List[Path] = []
    page_text = ""
    text_file_path = None
    
    async with async_playwright() as p:
        browser = None
        try:
            # 2. 启动浏览器
            logs.append("🚀 正在启动浏览器...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 设置视口大小
            await page.set_viewport_size({"width": width, "height": 900})
            logs.append(f"📏 浏览器视口宽度已设置为: {width}px")
            
            logs.append(f"🔗 正在打开页面: {url}")
            
            # 使用更灵活的加载策略
            # 使用更健壮的 networkidle 策略，等待网络活动基本停止
            logs.append("   ⏳ 正在等待网络空闲(networkidle)，最长等待90秒...")
            await page.goto(url, wait_until="networkidle", timeout=90000)
            logs.append("   ✅ 页面网络活动已稳定。")

        except PlaywrightTimeoutError as e:
            logs.append(f"⚠️  警告：页面加载在90秒内未完全空闲，但仍将继续尝试截图。错误: {e}")
        except Exception as e:
            logs.append(f"❌ 错误：无法启动浏览器或导航到页面 {url}")
            logs.append(f"   原因: {e}")
            if browser:
                await browser.close()
            return {
                "success": False, "output_dir": str(output_dir), "screenshot_paths": [], 
                "text_content": "", "text_content_path": None, "logs": logs, "error": str(e)
            }

        # 3. 循环截图和滚动
        screenshot_count = 0
        previous_scroll_position = -1

        try:
            while True:
                # 检查是否到达页面底部
                current_scroll_position = await page.evaluate("window.scrollY")
                if abs(current_scroll_position - previous_scroll_position) < 1 and screenshot_count > 0:
                    logs.append("🏁 已到达页面底部。")
                    break
                
                previous_scroll_position = current_scroll_position

                # 截图
                screenshot_path = output_dir / f"screenshot_{screenshot_count:02d}.png"
                await page.screenshot(path=screenshot_path)
                logs.append(f"   📸 已保存截图: {screenshot_path}")
                screenshot_paths.append(screenshot_path)
                screenshot_count += 1

                # 检查是否已达到截图数量限制
                if limit > 0 and screenshot_count >= limit:
                    logs.append(f"📸 已达到截图数量上限 ({limit} 张)，任务提前结束。")
                    break
                
                # 向下滚动一个视口的高度
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await asyncio.sleep(1)

        except Exception as e:
            logs.append(f"❌ 截图过程中发生错误: {e}")
            # Even if screenshot fails, try to get text and close browser
        finally:
            # 4. 提取并保存文本内容
            try:
                logs.append("📝 正在提取页面文本内容...")
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(0.5)
                
                page_text = await page.evaluate("document.body.innerText") or ""
                text_file_path = output_dir / "page_content.txt"
                with open(text_file_path, "w", encoding="utf-8") as f:
                    f.write(page_text)
                logs.append(f"   ✅ 文本内容已保存到: {text_file_path}")
            except Exception as e:
                logs.append(f"⚠️  提取文本内容失败: {e}")

            # 5. 关闭浏览器
            if browser:
                await browser.close()
            logs.append(f"\n🎉 截图完成！共生成 {screenshot_count} 张图片。")

    return {
        "success": True,
        "output_dir": str(output_dir),
        "screenshot_paths": [str(p) for p in screenshot_paths],
        "text_content": page_text,
        "text_content_path": str(text_file_path) if text_file_path else None,
        "logs": logs,
        "error": None
    }


async def main():
    """
    主函数，用于解析命令行参数并启动截图流程。
    """
    parser = argparse.ArgumentParser(
        description="网页分段完整截图工具。",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
使用示例:
  # 完整截图 (默认宽度 800px)
  python src/utils/capture_full_page.py https://www.bytedance.com

  # 只截取首屏 (限制为1张)
  python src/utils/capture_full_page.py https://www.bytedance.com --limit 1

  # 截取前3屏，并使用移动端宽度
  python src/utils/capture_full_page.py https://www.bytedance.com -l 3 --width 375
"""
    )
    parser.add_argument("url", help="要截图的目标网页URL")
    parser.add_argument(
        "-o", "--output",
        help="截图保存的根目录。如果未指定，将默认保存在项目根目录下的 `logs` 文件夹中。"
    )
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=750,
        help="浏览器视口宽度 (默认: 750px)"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=0,
        help="限制截图张数。0 表示不限制，截取整个页面 (默认: 0)"
    )
    args = parser.parse_args()

    # 确定输出目录
    if args.output:
        output_base_dir = Path(args.output)
    else:
        # 脚本位于 src/utils/，项目根目录是上二级
        project_root = Path(__file__).resolve().parent.parent
        output_base_dir = project_root / "logs"

    result = await capture_full_page(args.url, str(output_base_dir), args.width, args.limit)

    # 打印脚本执行的日志
    for log_message in result.get("logs", []):
        print(log_message)
    
    if result.get("error"):
        print(f"❌ 任务出错: {result['error']}")


if __name__ == "__main__":
    # 检查 Playwright 是否已安装
    try:
        from playwright.async_api import Error
    except ImportError:
        print("⚠️ Playwright 库未安装。请先运行以下命令安装:")
        print("   pip install playwright")
        print("   playwright install")
        sys.exit(1)

    # 运行主程序
    asyncio.run(main())