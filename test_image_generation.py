#!/usr/bin/env python3
"""
测试万象文生图API
"""

import os
import sys
from apis.wanx_image_api import WanxImageAPI

def test_image_generation():
    print("正在测试万象文生图API...")
    
    # 检查API密钥
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("错误: 缺少 DASHSCOPE_API_KEY 环境变量")
        print("请设置: $env:DASHSCOPE_API_KEY='your_api_key'")
        return False
    
    try:
        # 初始化API
        api = WanxImageAPI()
        print("✓ API初始化成功")
        
        # 测试创建任务
        prompt = "一只可爱的橘猫在阳光下打盹"
        style = "<photography>"
        size = "1024*1024"
        
        print(f"📝 测试提示词: {prompt}")
        print(f"🎭 测试风格: {style}")
        print(f"📐 测试尺寸: {size}")
        
        # 创建任务（异步模式）
        print("\n=== 测试异步任务创建 ===")
        task_result = api.create_image_task(prompt, style, size)
        
        if task_result['success']:
            task_id = task_result['task_id']
            print(f"✅ 任务创建成功!")
            print(f"📋 任务ID: {task_id}")
            
            # 查询任务状态
            print("\n=== 测试任务状态查询 ===")
            status_result = api.query_task_status(task_id)
            
            print(f"📊 任务状态: {status_result.get('status', 'unknown')}")
            
            if status_result.get('success') and status_result.get('status') == 'completed':
                print("🎉 图片生成完成!")
                image_urls = status_result.get('image_urls', [])
                if image_urls:
                    print(f"🖼️ 图片URL: {image_urls[0]}")
                else:
                    print("⚠️ 未获取到图片URL")
            elif status_result.get('status') in ['running', 'pending']:
                print("⏳ 任务还在处理中，这是正常的")
            else:
                print(f"❌ 任务状态异常: {status_result}")
        else:
            print(f"❌ 任务创建失败: {task_result.get('error', '未知错误')}")
            return False
            
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_image_generation()
    sys.exit(0 if success else 1) 