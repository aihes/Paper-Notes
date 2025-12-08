#!/usr/bin/env python3
"""
Johnny Decimal 网站爬虫脚本
爬取 https://johnnydecimal.com 的所有内容并保存为 Markdown 格式
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import Set, Dict, Optional
import html2text
import json


class JohnnyDecimalCrawler:
    """Johnny Decimal 网站爬虫"""
    
    BASE_URL = "https://johnnydecimal.com"
    START_URL = "https://johnnydecimal.com/00-09-site-administration/00-index/00.00-index/"
    
    def __init__(self, output_dir: str = "blog/johnny-decimal"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.url_to_file: Dict[str, str] = {}
        
        # 配置 html2text
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0  # 不换行
        self.html_converter.unicode_snob = True
        
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        # 会话
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def normalize_url(self, url: str) -> str:
        """标准化 URL"""
        # 移除锚点
        url = url.split('#')[0]
        # 确保以 / 结尾（如果是目录）
        if url and not url.endswith('/') and '.' not in url.split('/')[-1]:
            url += '/'
        return url
    
    def is_valid_url(self, url: str) -> bool:
        """检查 URL 是否有效且属于目标网站"""
        if not url:
            return False
        
        parsed = urlparse(url)
        
        # 必须是 johnnydecimal.com 域名
        if parsed.netloc and parsed.netloc != "johnnydecimal.com":
            return False
        
        # 排除一些不需要的路径
        excluded_patterns = [
            '/api/',
            '/assets/',
            '/images/',
            '/_astro/',
            '.xml',
            '.json',
            '.css',
            '.js',
            '.png',
            '.jpg',
            '.jpeg',
            '.gif',
            '.svg',
            '.ico',
            '.pdf',
        ]
        
        for pattern in excluded_patterns:
            if pattern in url.lower():
                return False
        
        return True
    
    def url_to_filename(self, url: str) -> str:
        """将 URL 转换为文件名"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path:
            return "index.md"
        
        # 将路径转换为文件名
        # 例如: 00-09-site-administration/00-index/00.00-index -> 00.00-index.md
        parts = path.split('/')
        
        # 使用最后一个部分作为文件名
        filename = parts[-1] if parts[-1] else parts[-2] if len(parts) > 1 else "index"
        
        # 清理文件名
        filename = re.sub(r'[^\w\-\.]', '-', filename)
        
        return f"{filename}.md"
    
    def url_to_filepath(self, url: str) -> Path:
        """将 URL 转换为完整文件路径"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path:
            return self.output_dir / "index.md"
        
        # 保持目录结构
        parts = path.split('/')
        
        # 创建目录结构
        if len(parts) > 1:
            dir_path = self.output_dir / '/'.join(parts[:-1])
        else:
            dir_path = self.output_dir
        
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # 文件名
        filename = parts[-1] if parts[-1] else "index"
        filename = re.sub(r'[^\w\-\.]', '-', filename)
        
        return dir_path / f"{filename}.md"
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """从页面中提取所有链接"""
        links = set()
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # 转换为绝对 URL
            full_url = urljoin(base_url, href)
            full_url = self.normalize_url(full_url)
            
            if self.is_valid_url(full_url):
                links.add(full_url)
        
        return links
    
    def extract_content(self, soup: BeautifulSoup, url: str) -> str:
        """从页面中提取主要内容"""
        # 移除不需要的元素
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # 尝试找到主要内容区域
        main_content = None
        
        # 常见的主内容选择器
        content_selectors = [
            'main',
            'article',
            '.content',
            '.main-content',
            '#content',
            '#main',
            '.post-content',
            '.article-content',
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            # 如果找不到主内容区域，使用 body
            main_content = soup.find('body')
        
        if not main_content:
            return ""
        
        # 提取标题
        title = ""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
        
        h1_tag = soup.find('h1')
        if h1_tag:
            title = h1_tag.get_text().strip()
        
        # 转换为 Markdown
        html_content = str(main_content)
        markdown_content = self.html_converter.handle(html_content)
        
        # 清理 Markdown
        markdown_content = self.clean_markdown(markdown_content)
        
        # 添加元数据
        metadata = f"""---
title: "{title}"
source: "{url}"
crawled_at: "{time.strftime('%Y-%m-%d %H:%M:%S')}"
---

"""
        
        return metadata + markdown_content
    
    def clean_markdown(self, content: str) -> str:
        """清理 Markdown 内容"""
        # 移除多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 移除行首行尾空白
        lines = [line.rstrip() for line in content.split('\n')]
        content = '\n'.join(lines)
        
        return content.strip()
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """获取页面内容"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 检查内容类型
            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type:
                return None
            
            return BeautifulSoup(response.text, 'html.parser')
        
        except requests.RequestException as e:
            print(f"  ❌ 获取失败: {url} - {e}")
            self.failed_urls.add(url)
            return None
    
    def crawl_page(self, url: str) -> Set[str]:
        """爬取单个页面"""
        url = self.normalize_url(url)
        
        if url in self.visited_urls:
            return set()
        
        self.visited_urls.add(url)
        print(f"📄 正在爬取: {url}")
        
        soup = self.fetch_page(url)
        if not soup:
            return set()
        
        # 提取内容
        content = self.extract_content(soup, url)
        
        if content:
            # 保存内容
            filepath = self.url_to_filepath(url)
            filepath.write_text(content, encoding='utf-8')
            self.url_to_file[url] = str(filepath)
            print(f"  ✅ 已保存: {filepath}")
        
        # 提取链接
        links = self.extract_links(soup, url)
        
        # 过滤已访问的链接
        new_links = links - self.visited_urls
        
        return new_links
    
    def crawl(self, max_pages: int = 500, delay: float = 0.5):
        """开始爬取"""
        print(f"🚀 开始爬取 Johnny Decimal 网站")
        print(f"📁 输出目录: {self.output_dir}")
        print(f"🔗 起始 URL: {self.START_URL}")
        print("-" * 50)
        
        # 待爬取的 URL 队列
        to_crawl = {self.START_URL}
        
        while to_crawl and len(self.visited_urls) < max_pages:
            url = to_crawl.pop()
            
            new_links = self.crawl_page(url)
            to_crawl.update(new_links)
            
            # 延迟，避免请求过快
            time.sleep(delay)
        
        print("-" * 50)
        print(f"✅ 爬取完成!")
        print(f"📊 统计:")
        print(f"   - 已爬取页面: {len(self.visited_urls)}")
        print(f"   - 保存文件数: {len(self.url_to_file)}")
        print(f"   - 失败页面数: {len(self.failed_urls)}")
        
        # 保存索引
        self.save_index()
        
        # 保存失败列表
        if self.failed_urls:
            self.save_failed_urls()
    
    def save_index(self):
        """保存索引文件"""
        index_path = self.output_dir / "README.md"
        
        content = """# Johnny Decimal 学习笔记

本目录包含从 [Johnny Decimal](https://johnnydecimal.com) 网站爬取的内容，用于离线学习。

## 目录结构

"""
        
        # 按路径排序
        sorted_files = sorted(self.url_to_file.items(), key=lambda x: x[1])
        
        for url, filepath in sorted_files:
            relative_path = Path(filepath).relative_to(self.output_dir)
            # 从 URL 提取标题
            title = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
            content += f"- [{title}]({relative_path})\n"
        
        content += f"""

## 来源

- 网站: https://johnnydecimal.com
- 爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
- 页面数量: {len(self.url_to_file)}
"""
        
        index_path.write_text(content, encoding='utf-8')
        print(f"📋 已保存索引: {index_path}")
    
    def save_failed_urls(self):
        """保存失败的 URL 列表"""
        failed_path = self.output_dir / "failed_urls.txt"
        
        content = "# 爬取失败的 URL\n\n"
        for url in sorted(self.failed_urls):
            content += f"{url}\n"
        
        failed_path.write_text(content, encoding='utf-8')
        print(f"⚠️ 已保存失败列表: {failed_path}")


def main():
    """主函数"""
    crawler = JohnnyDecimalCrawler(output_dir="blog/johnny-decimal")
    crawler.crawl(max_pages=500, delay=0.3)


if __name__ == "__main__":
    main()