from openai import OpenAI
import os
import json

class QwenNormalAPI:
    def __init__(self):
        self.api_key = os.getenv('DASHSCOPE_API_KEY', 'sk-2d5c7dbf8a624240a39f59e3e5d382cf')
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
    
    def get_model_info(self):
        """
        获取模型信息
        """
        return {
            "name": "通义千问(普通模式)",
            "description": "阿里云通义千问大语言模型 - 普通对话模式",
            "type": "chat"
        }
    
    def chat(self, messages, model="qwen-plus-2025-04-28", stream=True, **kwargs):
        """
        调用通义千问API进行普通对话（不开启思考模式）
        """
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream,
                # 普通模式不开启思考
                extra_body={"enable_thinking": False}
            )
            
            if stream:
                return self._handle_stream_response(completion)
            else:
                # 将OpenAI响应转换为字典格式
                return {
                    "choices": [{
                        "message": {
                            "content": completion.choices[0].message.content,
                            "role": "assistant"
                        },
                        "finish_reason": completion.choices[0].finish_reason
                    }],
                    "usage": completion.usage.dict() if hasattr(completion.usage, 'dict') else completion.usage
                }
                
        except Exception as e:
            return {"error": f"API请求失败: {str(e)}"}
    
    def _handle_stream_response(self, completion):
        """
        处理流式响应
        """
        try:
            for chunk in completion:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content:
                        yield {
                            "choices": [{
                                "delta": {
                                    "content": delta.content
                                }
                            }]
                        }
                elif hasattr(chunk, 'usage') and chunk.usage:
                    # 处理usage信息
                    yield {
                        "usage": chunk.usage
                    }
        except Exception as e:
            yield {"error": f"流式响应处理失败: {str(e)}"} 