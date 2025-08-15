import requests
import json
import os

class HunyuanAPI:
    def __init__(self):
        self.api_key = os.getenv('HUNYUAN_API_KEY')
        if not self.api_key:
            raise RuntimeError('Missing environment variable HUNYUAN_API_KEY')
        self.base_url = "https://api.hunyuan.cloud.tencent.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_model_info(self):
        """
        获取模型信息
        """
        return {
            "name": "腾讯混元",
            "description": "腾讯混元大语言模型",
            "type": "chat"
        }
    
    def chat(self, messages, model="hunyuan-turbos-latest", stream=True, enable_enhancement=True, **kwargs):
        """
        调用腾讯混元API进行对话
        """
        url = f"{self.base_url}/chat/completions"
        
        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "enable_enhancement": enable_enhancement
        }
        
        # 处理其他可选参数
        if "temperature" in kwargs:
            data["temperature"] = kwargs["temperature"]
        if "top_p" in kwargs:
            data["top_p"] = kwargs["top_p"]
        if "max_tokens" in kwargs:
            data["max_tokens"] = kwargs["max_tokens"]
        
        try:
            response = requests.post(url, headers=self.headers, json=data, stream=stream)
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                return response.json()
                
        except requests.exceptions.RequestException as e:
            return {"error": f"API请求失败: {str(e)}"}
    
    def _handle_stream_response(self, response):
        """
        处理流式响应
        """
        try:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # 移除 'data: ' 前缀
                        if data == '[DONE]':
                            break
                        try:
                            json_data = json.loads(data)
                            # 转换为统一格式
                            if "choices" in json_data:
                                yield json_data
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            yield {"error": f"流式响应处理失败: {str(e)}"} 