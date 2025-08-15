#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键运行所有PyTorch示例
======================

这个脚本会按顺序运行所有的学习示例，
让您可以一次性体验完整的PyTorch学习之旅！
"""

import os
import sys
import subprocess
import time

def run_example(filename, description):
    """运行单个示例文件"""
    print("\n" + "="*60)
    print(f"🚀 开始运行: {description}")
    print(f"📁 文件: {filename}")
    print("="*60)
    
    try:
        # 运行Python文件
        result = subprocess.run([sys.executable, filename], 
                              capture_output=False, 
                              text=True, 
                              timeout=120)  # 2分钟超时
        
        if result.returncode == 0:
            print(f"\n✅ {description} 运行成功！")
        else:
            print(f"\n❌ {description} 运行失败！")
            print(f"错误代码: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n⏰ {description} 运行超时！")
        return False
    except Exception as e:
        print(f"\n❌ {description} 运行出错: {e}")
        return False
    
    return True

def main():
    print("🎯 PyTorch 学习示例 - 一键运行")
    print("=" * 60)
    print("这个脚本将按顺序运行所有学习示例")
    print("请确保您已经安装了所需的依赖包")
    print("\n依赖包安装命令:")
    print("pip install torch matplotlib scikit-learn")
    
    # 确认是否继续
    response = input("\n是否继续运行所有示例？(y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("已取消运行。")
        return
    
    # 检查文件是否存在
    examples = [
        ("01_basic_operations.py", "PyTorch基础操作"),
        ("02_simple_linear_regression.py", "简单线性回归"),
        ("03_neural_network_demo.py", "神经网络演示")
    ]
    
    # 切换到脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    missing_files = []
    for filename, _ in examples:
        if not os.path.exists(filename):
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n❌ 以下文件不存在:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n请确保所有示例文件都在同一目录下。")
        return
    
    # 运行所有示例
    success_count = 0
    total_count = len(examples)
    
    start_time = time.time()
    
    for i, (filename, description) in enumerate(examples, 1):
        print(f"\n📊 进度: {i}/{total_count}")
        
        if run_example(filename, description):
            success_count += 1
        
        # 在示例之间稍微暂停
        if i < total_count:
            print("\n⏸️  暂停3秒钟，准备下一个示例...")
            time.sleep(3)
    
    # 总结报告
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n" + "="*60)
    print("🎉 所有示例运行完成！")
    print("="*60)
    print(f"✅ 成功运行: {success_count}/{total_count} 个示例")
    print(f"⏱️  总用时: {elapsed_time:.1f} 秒")
    
    if success_count == total_count:
        print("\n🎊 恭喜！您已经完成了所有PyTorch基础学习！")
        print("\n📈 接下来您可以:")
        print("1. 查看生成的图表文件 (.png)")
        print("2. 修改示例代码中的参数进行实验")
        print("3. 尝试解决更复杂的问题")
        print("4. 学习更高级的PyTorch功能")
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个示例运行失败")
        print("建议检查错误信息并确保依赖包正确安装")
    
    # 列出生成的文件
    output_files = [
        "linear_regression_result.png",
        "neural_network_result.png", 
        "activation_functions.png"
    ]
    
    existing_files = [f for f in output_files if os.path.exists(f)]
    if existing_files:
        print(f"\n📁 生成的文件:")
        for file in existing_files:
            print(f"   - {file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了运行")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
    
    input("\n按回车键退出...") 