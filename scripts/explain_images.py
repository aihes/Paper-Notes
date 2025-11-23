import os
import sys
from typing import List

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.ollama_client import OllamaClient

def explain_images_in_directory(image_dir: str, model: str, output_file: str):
    """
    使用 Ollama 解释指定目录中的所有图片，并将结果保存到文件中。

    Args:
        image_dir (str): 包含图片的目录路径。
        model (str): 用于解释图片的 Ollama 模型名称。
        output_file (str): 用于保存解释结果的 Markdown 文件路径。
    """
    if not os.path.isdir(image_dir):
        print(f"错误: 目录不存在 -> {image_dir}")
        return

    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not image_files:
        print(f"目录中未找到图片文件: {image_dir}")
        return

    print(f"找到了 {len(image_files)} 张图片。开始解释...")

    try:
        client = OllamaClient(model=model)
        # 验证模型是否可用
        available_models = client.list_models()
        if model not in available_models:
            print(f"错误: 模型 '{model}' 不可用。请确保已通过 `ollama pull {model}` 拉取。")
            print(f"可用模型: {available_models}")
            return
    except Exception as e:
        print(f"初始化 Ollama 客户端失败: {e}")
        return

    explanations = []

    for image_file in sorted(image_files):
        image_path = os.path.join(image_dir, image_file)
        print(f"正在处理图片: {image_file}...")
        
        prompt = "你是一位资深的行业分析师。请用中文详细解释这张PPT图片。分析应包括：1. 图片的核心内容和数据是什么？2. 它试图传达的关键信息或观点是什么？3. 这张图在整个关于AI平台变迁的演讲中可能扮演什么角色？"

        try:
            # 每次对话前清空历史，确保是对单个图片的独立分析
            client.clear_history()
            response = client.chat(prompt, image_paths=[image_path])
            
            explanations.append(f"## 图片: `{image_file}`\n\n")
            explanations.append(f"![{image_file}]({os.path.join('..', 'blog', 'ai-eat-world', 'images', image_file)})\n\n")
            explanations.append("### AI 模型解释\n\n")
            explanations.append(f"{response}\n\n---\n\n")
            print(f"  -> 解释完成。")

        except Exception as e:
            error_message = f"处理图片 {image_file} 时发生错误: {e}"
            print(error_message)
            explanations.append(f"## 图片: `{image_file}`\n\n")
            explanations.append(f"### 解释失败\n\n`{error_message}`\n\n---\n\n")

    print("所有图片处理完毕。正在写入结果文件...")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# AI 图片解释汇总\n\n")
        f.write("本文档使用多模态模型对 `blog/ai-eat-world/images` 目录下的所有图片进行了自动分析和解释。\n\n")
        f.write("---\n\n")
        f.writelines(explanations)
    
    print(f"解释已成功保存到: {output_file}")


if __name__ == "__main__":
    IMAGE_DIRECTORY = "blog/ai-eat-world/images"
    OLLAMA_MODEL = "gemma3:4b"  # 确保你已经拉取了这个模型
    OUTPUT_MARKDOWN_FILE = "blog/ai-eat-world/image_explanations.md"
    
    explain_images_in_directory(IMAGE_DIRECTORY, OLLAMA_MODEL, OUTPUT_MARKDOWN_FILE)
