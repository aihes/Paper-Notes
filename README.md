# Paper-Notes

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

在浩如烟海的学术论文中，隐藏着推动科技进步的核心思想。本项目不仅致力于解构优秀论文，分享知识，还提供了一套**自动化工具链**，用于将深度解读高效地分发到社交媒体平台，激发更广泛的讨论与创新。

## 📖 项目愿景 (Vision)

*   **降低理解门槛**：通过图文并茂、深入浅出的方式，解构论文的核心思想、实验设计和关键结论。
*   **构建知识网络**：将不同论文中的相关概念联系起来，形成一个结构化的知识体系。
*   **自动化知识传播**：利用自动化脚本，将结构化的笔记快速转换为适合不同社交媒体（X/Twitter, 小红书）的内容格式并发布。

## ✨ 项目特点 (Features)

*   **深度剖析**：从背景、动机、方法到实验结果的全面剖析，而非简单的摘要。
*   **图文并茂**：使用原创图表、流程图解释复杂概念。
*   **自动化发布**：内置 Python 脚本和 Shell 工具，支持一键将笔记内容处理并发布到 X (Twitter) 和小红书。
*   **内容预处理**：自动处理图片尺寸、格式，以及将 Markdown 内容转换为适合社交媒体的纯文本格式。

## 📁 目录结构 (Directory Structure)

```
Paper-Notes/
├── papers/            # 存放所有论文笔记的核心目录
│   └── some-paper/    # 每篇论文一个独立目录
│       ├── README.md  # 笔记正文
│       ├── images/    # 笔记相关图片
│       └── code/      # 笔记相关代码
├── src/               # 自动化工具源代码
│   └── utils/         # 核心功能模块 (发布、图片处理等)
├── scripts/           # 辅助脚本 (内容准备、格式转换等)
├── assets/            # 公共资源
├── x_content/         # 发布前的临时内容生成目录
├── send_all.sh        # 一键发布脚本 (入口)
└── pyproject.toml     # 项目依赖配置
```

## 🚀 快速开始 (Getting Started)

### 环境要求

*   Python >= 3.12
*   [uv](https://github.com/astral-sh/uv) (推荐) 或 pip

### 安装依赖

本项目使用 `uv` 进行依赖管理。

```bash
# 克隆项目
git clone https://github.com/your-username/Paper-Notes.git
cd Paper-Notes

# 安装依赖
uv sync
# 或者使用 pip
# pip install -r requirements.txt (需先生成)
```

### 配置环境

在项目根目录下创建一个 `.env` 文件，并配置以下环境变量（用于自动化发布功能）：

```ini
XHS_API_URL=your_api_url
XHS_API_KEY=your_api_key
```

> 注意：本项目使用一个统一的后端服务 API 来处理图片上传和多平台发布。

## 🛠️ 使用指南 (Usage)

### 1. 撰写笔记

在 `papers/` 目录下创建一个新的文件夹，并在其中编写 `README.md`。

### 2. 自动化发布

使用根目录下的 `send_all.sh` 脚本将笔记发布到社交媒体。

```bash
# 用法: ./send_all.sh <论文目录路径> [平台]

# 发布到所有平台 (X 和 小红书)
./send_all.sh papers/001-example-paper

# 仅发布到 X (Twitter)
./send_all.sh papers/001-example-paper x

# 仅发布到 小红书
./send_all.sh papers/001-example-paper xiaohongshu
```

脚本会自动执行以下步骤：
1.  **内容预处理**：解析 Markdown，提取文本和图片。
2.  **图片上传**：将图片上传到图床/API。
3.  **发布**：调用 API 将内容发布到指定平台。

## 📚 论文目录 (Table of Contents)

*   **[示例]** [论文标题 - 一个简洁且吸引人的副标题](./papers/001-example-paper/README.md)

---

## 🤝 如何贡献 (How to Contribute)

我们欢迎任何形式的贡献！

1.  **Fork** 本仓库。
2.  在 `papers/` 目录下创建你的论文笔记。
3.  提交 **Pull Request**。

## 📄 许可证 (License)

*   本项目的**文本和图片**内容采用 [CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/) 许可。
*   项目中的**代码**部分采用 [MIT 许可证](https://opensource.org/licenses/MIT) 许可。