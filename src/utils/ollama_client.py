import base64
import os
from openai import OpenAI, APIConnectionError
from typing import List, Dict, Optional

class OllamaClient:
    """
    一个用于与 Ollama 的 OpenAI 兼容 API 进行交互的客户端。
    这个类封装了对话历史管理，使得进行连续对话更加方便。
    """
    def __init__(self, base_url="http://localhost:11434/v1", api_key="ollama", model=None):
        """
        初始化 OllamaClient。

        Args:
            base_url (str): Ollama 服务的基础 URL。
            api_key (str): API 密钥（对于 Ollama 来说是必需的，但会被忽略）。
            model (str, optional): 默认使用的模型。如果未提供，则需要在调用 chat 方法时指定。
        """
        try:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            self.messages: List[Dict[str, str]] = []
            self.model = model
        except Exception as e:
            raise RuntimeError(f"初始化 OpenAI 客户端失败: {e}")

    def list_models(self) -> List[str]:
        """
        获取本地可用的 Ollama 模型列表。

        Returns:
            List[str]: 可用模型的 ID 列表。
        
        Raises:
            APIConnectionError: 如果无法连接到 Ollama 服务。
            Exception: 如果发生其他 API 错误。
        """
        try:
            models_response = self.client.models.list()
            return [model.id for model in models_response.data]
        except APIConnectionError as e:
            raise APIConnectionError(f"无法连接到 Ollama 服务: {e}")
        except Exception as e:
            raise Exception(f"获取模型列表时发生错误: {e}")

    def _encode_image_to_base64(self, image_path: str) -> str:
        """
        将图片文件编码为 Base64 Data URI。

        Args:
            image_path (str): 图片文件的路径。

        Returns:
            str: Base64 编码的 Data URI。
        
        Raises:
            FileNotFoundError: 如果图片路径不存在。
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件未找到: {image_path}")
        
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 根据文件扩展名确定 MIME 类型
        mime_type = "image/png"  # 默认为 png
        if image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif image_path.lower().endswith(".gif"):
            mime_type = "image/gif"
            
        return f"data:{mime_type};base64,{encoded_string}"

    def chat(self, user_input: str, image_paths: Optional[List[str]] = None, model: Optional[str] = None) -> str:
        """
        与模型进行一次对话，可选地包含一张或多张图片。

        Args:
            user_input (str): 用户输入的文本内容。
            image_paths (Optional[List[str]]): 要包含在对话中的一个或多个图片文件的路径列表。
            model (Optional[str]): 本次对话使用的模型。如果未提供，则使用客户端初始化时设置的默认模型。

        Returns:
            str: 模型生成的响应内容。
            
        Raises:
            ValueError: 如果没有可用的模型。
            APIConnectionError: 如果无法连接到 Ollama 服务。
            Exception: 如果发生其他 API 错误。
        """
        selected_model = model or self.model
        if not selected_model:
            available_models = self.list_models()
            if not available_models:
                raise ValueError("没有可用的模型。请先通过 `ollama pull` 拉取一个模型。")
            selected_model = available_models[0]
            self.model = selected_model
            print(f"未指定模型，自动选择第一个可用模型: {self.model}")

        content_parts = [{"type": "text", "text": user_input}]
        
        if image_paths:
            if "llava" not in selected_model:
                print(f"警告: 模型 '{selected_model}' 可能不是一个多模态模型。处理图片可能会失败。")

            for image_path in image_paths:
                try:
                    base64_image = self._encode_image_to_base64(image_path)
                    content_parts.append({
                        "type": "image_url",
                        "image_url": {"url": base64_image},
                    })
                except FileNotFoundError as e:
                    raise e # 直接向上抛出文件未找到的异常

        self.messages.append({"role": "user", "content": content_parts})
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=self.messages,
                model=selected_model,
            )
            
            assistant_response = chat_completion.choices[0].message.content
            if assistant_response:
                self.messages.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response or ""
        except APIConnectionError as e:
            # 从消息历史中移除失败的用户输入
            self.messages.pop()
            raise APIConnectionError(f"无法连接到 Ollama 服务: {e}")
        except Exception as e:
            # 从消息历史中移除失败的用户输入
            self.messages.pop()
            raise Exception(f"与模型对话时发生错误: {e}")

    def clear_history(self):
        """
        清空对话历史。
        """
        self.messages = []
        print("对话历史已清空。")
