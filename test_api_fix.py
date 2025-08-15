#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修复后的CogVideoX API调用
"""

import os
import sys
import time
from apis.cogvideo_api import CogVideoAPI

def test_api_endpoints():
    """测试API端点是否正确"""
    print("🔍 测试API端点配置...")
    
    # 检查配置文件
    config_path = "config.py"
    if not os.path.exists(config_path):
        print("❌ 配置文件不存在")
        return False
    
    # 检查环境变量配置
    try:
        from config import COGVIDEO_CONFIG
        if not COGVIDEO_CONFIG.get('api_key'):
            print("❌ API密钥未配置")
            return False
        print("✅ API配置检查通过")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    # 初始化API
    try:
        api = CogVideoAPI()
        print("✅ CogVideoX API初始化成功")
        return True
    except Exception as e:
        print(f"❌ API初始化失败: {e}")
        return False

def test_video_generation():
    """测试视频生成功能"""
    print("\n🎬 测试视频生成功能...")
    
    try:
        api = CogVideoAPI()
        
        # 测试参数
        test_prompt = "一只可爱的小猫在阳光下玩耍"
        
        print(f"📝 测试提示词: {test_prompt}")
        print("🚀 开始生成视频...")
        
        # 调用API
        result = api.generate_video(
            prompt=test_prompt,
            model="cogvideox-3",
            duration=5
        )
        
        if result.get("success"):
            print("✅ API调用成功")
            print(f"📋 请求ID: {result.get('request_id', 'N/A')}")
            print(f"📊 模型: {result.get('model', 'N/A')}")
            
            # 如果有任务ID，测试查询状态
            if "request_id" in result:
                print("\n🔍 测试任务状态查询...")
                status_result = api.query_task_status(result["request_id"])
                
                if status_result.get("success"):
                    print(f"✅ 状态查询成功: {status_result.get('status', 'N/A')}")
                else:
                    print(f"⚠️ 状态查询失败: {status_result.get('error', 'N/A')}")
            
            return True
        else:
            print(f"❌ API调用失败: {result.get('error', 'N/A')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试修复后的CogVideoX API...")
    print("=" * 50)
    
    # 测试1: API端点配置
    endpoint_ok = test_api_endpoints()
    
    if not endpoint_ok:
        print("\n❌ API端点测试失败，停止后续测试")
        return False
    
    # 测试2: 视频生成功能
    generation_ok = test_video_generation()
    
    print("\n" + "=" * 50)
    
    if endpoint_ok and generation_ok:
        print("🎉 所有测试通过！API修复成功")
        return True
    else:
        print("❌ 测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 