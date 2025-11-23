from src.utils.ollama_client import OllamaClient
import os

def main():
    """
    使用 OllamaClient 测试解释图片内容。
    """
    # 确保我们使用的是相对于项目根目录的路径
    image_path = "blog/ai-eat-world/images/page_2.png"
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误: 图片文件未找到于 '{image_path}'")
        return

    # 用户的提示
    user_prompt = "请解释这张图片的内容"
    # 使用的模型
    model_name = "gemma3:4b"

    try:
        # 初始化 Ollama 客户端
        ollama_client = OllamaClient()

        print(f"正在使用模型 '{model_name}' 分析图片: {image_path}")
        
        # 调用 chat 方法并传入图片
        response = ollama_client.chat(
            user_input=user_prompt,
            image_paths=[image_path],
            model=model_name
        )

        print("\n模型响应:")
        print(response)

    except FileNotFoundError as fnf_error:
        print(f"\n错误: {fnf_error}")
        print("请确保图片文件路径正确。")
    except Exception as e:
        print(f"\n与 Ollama 服务交互时发生错误: {e}")

if __name__ == "__main__":
    main()