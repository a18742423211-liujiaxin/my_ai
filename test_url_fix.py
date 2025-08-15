#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试API URL端点修复
"""

import re
from apis.cogvideo_api import CogVideoAPI

def test_api_url_fix():
    """测试API URL是否已修复为正确的端点"""
    print("🔍 测试API URL端点修复...")
    
    # 读取API源码
    with open('apis/cogvideo_api.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含旧的错误URL
    old_urls = [
        "api.minimax.chat",  # 旧的错误URL
    ]
    
    # 检查是否包含正确的新URL
    correct_urls = [
        "api.minimaxi.chat",  # 新的正确URL
    ]
    
    issues = []
    
    # 检查是否还有旧URL
    for old_url in old_urls:
        if old_url in content:
            issues.append(f"❌ 仍包含旧URL: {old_url}")
    
    # 检查是否包含正确URL
    found_correct = False
    for correct_url in correct_urls:
        if correct_url in content:
            found_correct = True
            print(f"✅ 发现正确URL: {correct_url}")
    
    if not found_correct:
        issues.append("❌ 未发现正确的API URL")
    
    # 检查具体的API端点
    api_endpoints = [
        r"https://api\.minimaxi\.chat/v1/paas/v4/videos/generations",  # 视频生成
        r"https://api\.minimaxi\.chat/query/",  # 任务查询
    ]
    
    for endpoint_pattern in api_endpoints:
        if re.search(endpoint_pattern, content):
            print(f"✅ 发现正确的API端点: {endpoint_pattern}")
        else:
            issues.append(f"❌ 未发现API端点: {endpoint_pattern}")
    
    return len(issues) == 0, issues

def test_model_name():
    """测试模型名称是否正确"""
    print("\n🔍 测试模型名称...")
    
    with open('apis/cogvideo_api.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查模型名称
    if "cogvideox-3" in content:
        print("✅ 模型名称正确: cogvideox-3")
        return True
    else:
        print("❌ 模型名称错误或未找到")
        return False

def test_config_endpoint():
    """测试配置文件中的端点"""
    print("\n🔍 测试配置文件端点...")
    
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查配置文件中的API base是否正确
    if "api.minimaxi.chat" in content:
        print("✅ 配置文件URL正确")
        return True
    elif "api.minimax.chat" in content:
        print("❌ 配置文件仍使用旧URL")
        return False
    else:
        print("⚠️ 配置文件中未找到相关URL")
        return False

def main():
    """主测试函数"""
    print("🧪 测试API URL端点修复...")
    print("=" * 50)
    
    all_passed = True
    
    # 测试1: API URL修复
    url_ok, issues = test_api_url_fix()
    if not url_ok:
        all_passed = False
        for issue in issues:
            print(issue)
    
    # 测试2: 模型名称
    model_ok = test_model_name()
    if not model_ok:
        all_passed = False
    
    # 测试3: 配置文件端点
    config_ok = test_config_endpoint()
    if not config_ok:
        all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 所有URL端点测试通过！API修复成功")
        print("✅ API主机地址已修复为: api.minimaxi.chat")
        print("✅ 模型名称已更新为: cogvideox-3")
        return True
    else:
        print("❌ 部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 