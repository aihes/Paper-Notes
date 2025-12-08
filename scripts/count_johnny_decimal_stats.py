#!/usr/bin/env python3
"""
统计 Johnny Decimal 爬取内容的字数和 token 数
使用流式读取，避免一次性加载所有内容到内存
"""

import os
import re
from pathlib import Path
from typing import Tuple


def count_file_stats(filepath: Path) -> Tuple[int, int, int, int]:
    """
    统计单个文件的字符数、单词数、中文字符数和行数
    
    Returns:
        (字符数, 英文单词数, 中文字符数, 行数)
    """
    char_count = 0
    word_count = 0
    chinese_count = 0
    line_count = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line_count += 1
                char_count += len(line)
                
                # 统计英文单词（简单的空格分割）
                words = line.split()
                word_count += len(words)
                
                # 统计中文字符
                chinese_chars = re.findall(r'[\u4e00-\u9fff]', line)
                chinese_count += len(chinese_chars)
    except Exception as e:
        print(f"  ⚠️ 读取失败: {filepath} - {e}")
        return 0, 0, 0, 0
    
    return char_count, word_count, chinese_count, line_count


def estimate_tokens(char_count: int, word_count: int, chinese_count: int) -> int:
    """
    估算 token 数
    
    估算规则：
    - 英文：大约 1 个单词 = 1.3 个 token（考虑到子词分割）
    - 中文：大约 1 个字符 = 1-2 个 token（取 1.5）
    - 其他字符（标点、数字等）：大约 1 个字符 = 0.5 个 token
    """
    # 英文单词的 token 估算
    english_tokens = word_count * 1.3
    
    # 中文字符的 token 估算
    chinese_tokens = chinese_count * 1.5
    
    # 其他字符（总字符 - 中文字符 - 英文单词平均长度*单词数）
    avg_word_len = 5  # 英文单词平均长度
    other_chars = max(0, char_count - chinese_count - (word_count * avg_word_len))
    other_tokens = other_chars * 0.3
    
    return int(english_tokens + chinese_tokens + other_tokens)


def main():
    """主函数"""
    base_dir = Path("blog/johnny-decimal")
    
    if not base_dir.exists():
        print(f"❌ 目录不存在: {base_dir}")
        return
    
    print("📊 统计 Johnny Decimal 内容...")
    print("-" * 50)
    
    total_files = 0
    total_chars = 0
    total_words = 0
    total_chinese = 0
    total_lines = 0
    total_bytes = 0
    
    # 遍历所有 Markdown 文件
    md_files = list(base_dir.rglob("*.md"))
    
    for filepath in md_files:
        total_files += 1
        total_bytes += filepath.stat().st_size
        
        chars, words, chinese, lines = count_file_stats(filepath)
        total_chars += chars
        total_words += words
        total_chinese += chinese
        total_lines += lines
    
    # 估算 token 数
    estimated_tokens = estimate_tokens(total_chars, total_words, total_chinese)
    
    print(f"📁 文件统计:")
    print(f"   - Markdown 文件数: {total_files}")
    print(f"   - 总大小: {total_bytes / 1024 / 1024:.2f} MB ({total_bytes:,} bytes)")
    print()
    print(f"📝 内容统计:")
    print(f"   - 总字符数: {total_chars:,}")
    print(f"   - 总行数: {total_lines:,}")
    print(f"   - 英文单词数: {total_words:,}")
    print(f"   - 中文字符数: {total_chinese:,}")
    print()
    print(f"🔢 Token 估算:")
    print(f"   - 估算 Token 数: ~{estimated_tokens:,}")
    print(f"   - 估算方法: 英文单词×1.3 + 中文字符×1.5 + 其他字符×0.3")
    print()
    print(f"💡 参考信息:")
    print(f"   - GPT-4 上下文窗口: 128K tokens")
    print(f"   - Claude 上下文窗口: 200K tokens")
    print(f"   - 内容占比 (GPT-4): {estimated_tokens / 128000 * 100:.1f}%")
    print(f"   - 内容占比 (Claude): {estimated_tokens / 200000 * 100:.1f}%")


if __name__ == "__main__":
    main()