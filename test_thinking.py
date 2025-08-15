#!/usr/bin/env python3
"""
测试通义千问深度思考API
"""

import os
import sys
from apis.qwen_thinking_api import QwenThinkingAPI

def test_thinking_api():
    print("正在测试通义千问深度思考API...")
    
    # 检查API密钥
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("错误: 缺少 DASHSCOPE_API_KEY 环境变量")
        print("请设置: $env:DASHSCOPE_API_KEY='your_api_key'")
        return False
    
    try:
        # 初始化API
        api = QwenThinkingAPI()
        print("✓ API初始化成功")
        
        # 测试消息
        messages = [
            {"role": "user", "content": "请解释什么是机器学习，并举一个简单的例子"}
        ]
        
        print("正在发送测试请求...")
        
        # 获取流式响应
        response_generator = api.chat(messages, stream=True)
        
        thinking_content = ""
        answer_content = ""
        
        for response in response_generator:
            print(f"[DEBUG] 响应: {response}")
            
            if "choices" in response:
                delta = response["choices"][0].get("delta", {})
                
                if "reasoning_content" in delta:
                    thinking_content += delta["reasoning_content"]
                    print(f"[THINKING] {delta['reasoning_content'][:100]}...")
                    
                if "content" in delta:
                    answer_content += delta["content"]
                    print(f"[ANSWER] {delta['content'][:100]}...")
            
            elif "phase_change" in response:
                print(f"[PHASE] {response['phase_change']}")
                
        print(f"\n=== 最终结果 ===")
        print(f"思考内容长度: {len(thinking_content)}")
        print(f"回答内容长度: {len(answer_content)}")
        
        if thinking_content:
            print(f"思考内容开头: {thinking_content[:200]}...")
        else:
            print("警告: 没有收到思考内容!")
            
        if answer_content:
            print(f"回答内容: {answer_content}")
        else:
            print("警告: 没有收到回答内容!")
            
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    success = test_thinking_api()
    sys.exit(0 if success else 1) 