from openai import OpenAI
import os
import json

class QwenThinkingAPI:
    def __init__(self):
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise RuntimeError('Missing environment variable DASHSCOPE_API_KEY')
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
    
    def get_model_info(self):
        """
        获取模型信息
        """
        return {
            "name": "通义千问(深度思考)",
            "description": "阿里云通义千问大语言模型 - 深度思考模式",
            "type": "chat"
        }
    
    def chat(self, messages, model="qwen-plus-2025-04-28", stream=True, thinking_budget=None, **kwargs):
        """
        调用通义千问API进行深度思考对话
        """
        try:
            extra_body = {"enable_thinking": True}
            
            # 如果设置了思考预算，添加到请求中
            if thinking_budget:
                extra_body["thinking_budget"] = thinking_budget
            
            if stream:
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                    extra_body=extra_body
                )
                return self._handle_stream_response(completion)
            else:
                # 深度思考模式只支持流式调用，我们需要强制使用流式然后收集结果
                stream_completion = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,  # 强制流式
                    extra_body=extra_body
                )
                
                # 收集所有流式数据
                reasoning_content = ""
                answer_content = ""
                usage_info = None
                
                for chunk in stream_completion:
                    if not chunk.choices:
                        if hasattr(chunk, 'usage') and chunk.usage:
                            usage_info = chunk.usage
                        continue
                    
                    delta = chunk.choices[0].delta
                    
                    # 收集思考内容
                    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                        reasoning_content += delta.reasoning_content
                    
                    # 收集回复内容
                    if hasattr(delta, "content") and delta.content:
                        answer_content += delta.content
                
                # 返回统一格式
                result = {
                    "choices": [{
                        "message": {
                            "content": answer_content,
                            "role": "assistant"
                        },
                        "finish_reason": "stop"
                    }]
                }
                
                # 添加思考内容
                if reasoning_content:
                    result["choices"][0]["message"]["reasoning_content"] = reasoning_content
                
                # 添加使用信息
                if usage_info:
                    result["usage"] = usage_info.dict() if hasattr(usage_info, 'dict') else usage_info
                
                return result
                
        except Exception as e:
            return {"error": f"API请求失败: {str(e)}"}
    
    def _handle_stream_response(self, completion):
        """
        处理流式响应，分别处理思考过程和回复内容
        """
        try:
            reasoning_content = ""
            answer_content = ""
            is_answering = False
            
            for chunk in completion:
                if not chunk.choices:
                    # 处理usage信息
                    if hasattr(chunk, 'usage') and chunk.usage:
                        yield {
                            "usage": chunk.usage
                        }
                    continue
                
                delta = chunk.choices[0].delta
                
                # 处理思考内容
                if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                    reasoning_content += delta.reasoning_content
                    yield {
                        "choices": [{
                            "delta": {
                                "reasoning_content": delta.reasoning_content
                            }
                        }]
                    }
                
                # 一旦开始输出正式答案，就只输出答案内容
                if hasattr(delta, "content") and delta.content:
                    is_answering = True
                    yield {
                        "choices": [{
                            "delta": {
                                "content": delta.content
                            }
                        }]
                    }
            
            # 结束时输出一个汇总，包含完整的思考内容和回答内容（如有需要）
            if reasoning_content or answer_content:
                yield {
                    "summary": {
                        "reasoning": reasoning_content if reasoning_content else None,
                        "answer": answer_content if answer_content else None
                    }
                }
        except Exception as e:
            yield {"error": f"流式响应处理失败: {str(e)}"} 