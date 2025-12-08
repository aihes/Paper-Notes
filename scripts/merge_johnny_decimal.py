#!/usr/bin/env python3
"""
合并 Johnny Decimal 所有 Markdown 文件到一个文件
按照 Johnny Decimal 编号顺序排列
"""

import re
from pathlib import Path
from typing import List, Tuple


def extract_jd_number(filepath: Path) -> Tuple[int, int, int, str]:
    """
    从文件路径中提取 Johnny Decimal 编号用于排序
    
    返回元组 (area, category, id, filename) 用于排序
    例如: 11.01 -> (10, 11, 1, filename)
          22.00.0138 -> (20, 22, 138, filename)
    """
    filename = filepath.stem
    
    # 尝试匹配 XX.XX 格式 (如 11.01)
    match = re.match(r'^(\d{2})\.(\d{2})$', filename)
    if match:
        category = int(match.group(1))
        id_num = int(match.group(2))
        area = (category // 10) * 10
        return (area, category, id_num, filename)
    
    # 尝试匹配 XX.XX.XXXX 格式 (如 22.00.0138)
    match = re.match(r'^(\d{2})\.(\d{2})\.(\d+)', filename)
    if match:
        category = int(match.group(1))
        sub_cat = int(match.group(2))
        id_num = int(match.group(3))
        area = (category // 10) * 10
        return (area, category, id_num, filename)
    
    # 尝试匹配目录名格式 (如 00-09-site-administration)
    match = re.match(r'^(\d{2})-(\d{2})', filename)
    if match:
        area = int(match.group(1))
        return (area, 0, 0, filename)
    
    # 尝试匹配分类目录格式 (如 11-core)
    match = re.match(r'^(\d{2})-', filename)
    if match:
        category = int(match.group(1))
        area = (category // 10) * 10
        return (area, category, 0, filename)
    
    # 其他文件放到最后
    return (999, 999, 999, filename)


def get_sorted_files(base_dir: Path) -> List[Path]:
    """获取按 Johnny Decimal 编号排序的文件列表"""
    md_files = list(base_dir.rglob("*.md"))
    
    # 排除 README.md 和 failed_urls.txt
    md_files = [f for f in md_files if f.name not in ['README.md', 'failed_urls.txt']]
    
    # 按 JD 编号排序
    sorted_files = sorted(md_files, key=extract_jd_number)
    
    return sorted_files


def merge_files(base_dir: Path, output_file: Path):
    """合并所有文件到一个文件"""
    sorted_files = get_sorted_files(base_dir)
    
    print(f"📚 合并 Johnny Decimal 内容...")
    print(f"📁 源目录: {base_dir}")
    print(f"📄 输出文件: {output_file}")
    print(f"📊 文件数量: {len(sorted_files)}")
    print("-" * 50)
    
    total_chars = 0
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # 写入文件头
        out.write("# Johnny Decimal 完整内容\n\n")
        out.write("本文件包含从 [Johnny Decimal](https://johnnydecimal.com) 网站爬取的所有内容。\n\n")
        out.write("---\n\n")
        
        # 生成目录
        out.write("## 目录\n\n")
        current_area = -1
        for filepath in sorted_files:
            jd_num = extract_jd_number(filepath)
            area = jd_num[0]
            
            # 新的区域
            if area != current_area and area < 100:
                current_area = area
                out.write(f"\n### {area:02d}-{area+9:02d}\n\n")
            
            # 读取标题
            title = filepath.stem
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('title:'):
                            title = line.replace('title:', '').strip().strip('"\'')
                            break
                        if line.startswith('# '):
                            title = line.replace('# ', '').strip()
                            break
            except:
                pass
            
            # 创建锚点链接
            anchor = filepath.stem.replace('.', '-').replace(' ', '-').lower()
            out.write(f"- [{filepath.stem}](#{anchor}) - {title}\n")
        
        out.write("\n---\n\n")
        
        # 写入内容
        current_area = -1
        for i, filepath in enumerate(sorted_files):
            jd_num = extract_jd_number(filepath)
            area = jd_num[0]
            
            # 新的区域分隔
            if area != current_area and area < 100:
                current_area = area
                out.write(f"\n# 区域 {area:02d}-{area+9:02d}\n\n")
                out.write("=" * 50 + "\n\n")
            
            # 写入文件分隔符
            anchor = filepath.stem.replace('.', '-').replace(' ', '-').lower()
            out.write(f"<a id=\"{anchor}\"></a>\n\n")
            out.write(f"## 📄 {filepath.stem}\n\n")
            out.write(f"*来源: {filepath.relative_to(base_dir)}*\n\n")
            
            # 读取并写入文件内容
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    total_chars += len(content)
                    
                    # 跳过 YAML 前置元数据（如果有的话）
                    if content.startswith('---'):
                        # 找到第二个 ---
                        end_idx = content.find('---', 3)
                        if end_idx != -1:
                            content = content[end_idx + 3:].strip()
                    
                    out.write(content)
                    out.write("\n\n")
            except Exception as e:
                out.write(f"*读取失败: {e}*\n\n")
            
            out.write("-" * 50 + "\n\n")
            
            # 进度显示
            if (i + 1) % 50 == 0:
                print(f"  已处理: {i + 1}/{len(sorted_files)} 文件")
    
    # 获取输出文件大小
    output_size = output_file.stat().st_size
    
    print("-" * 50)
    print(f"✅ 合并完成!")
    print(f"📊 统计:")
    print(f"   - 合并文件数: {len(sorted_files)}")
    print(f"   - 总字符数: {total_chars:,}")
    print(f"   - 输出文件大小: {output_size / 1024 / 1024:.2f} MB")


def main():
    """主函数"""
    base_dir = Path("blog/johnny-decimal")
    output_file = base_dir / "johnny-decimal-complete.md"
    
    if not base_dir.exists():
        print(f"❌ 目录不存在: {base_dir}")
        return
    
    merge_files(base_dir, output_file)


if __name__ == "__main__":
    main()