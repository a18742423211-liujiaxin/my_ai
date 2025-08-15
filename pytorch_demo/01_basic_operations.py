#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyTorch 基础操作示例
===================

这个文件将教您PyTorch的最基础操作：
1. 什么是张量(Tensor)
2. 如何创建张量
3. 张量的基本运算
4. 张量形状的变换

适合完全没有PyTorch经验的新手！
"""

import torch
import numpy as np

def main():
    print("🚀 欢迎来到PyTorch基础操作学习！")
    print("=" * 50)
    
    # ========================================
    # 第1部分：什么是张量？
    # ========================================
    print("\n📚 第1部分：认识张量(Tensor)")
    print("-" * 30)
    
    # 张量就像是一个可以存储数字的容器
    # 可以是一个数字(标量)、一行数字(向量)、一个表格(矩阵)等等
    
    # 创建一个简单的张量
    simple_tensor = torch.tensor([1, 2, 3, 4, 5])
    print(f"简单张量: {simple_tensor}")
    print(f"张量的形状: {simple_tensor.shape}")  # 形状告诉我们这个张量有多大
    print(f"张量的类型: {simple_tensor.dtype}")  # 类型告诉我们存储的是什么数据
    
    # ========================================
    # 第2部分：创建不同类型的张量
    # ========================================
    print("\n📚 第2部分：创建各种张量")
    print("-" * 30)
    
    # 1. 创建全零张量
    zeros = torch.zeros(3, 4)  # 3行4列的表格，里面都是0
    print(f"全零张量 (3x4):\n{zeros}")
    
    # 2. 创建全1张量
    ones = torch.ones(2, 3)  # 2行3列的表格，里面都是1
    print(f"\n全1张量 (2x3):\n{ones}")
    
    # 3. 创建随机张量
    random_tensor = torch.rand(2, 2)  # 2x2的表格，里面是0到1之间的随机数
    print(f"\n随机张量 (2x2):\n{random_tensor}")
    
    # 4. 从Python列表创建张量
    from_list = torch.tensor([[1, 2], [3, 4], [5, 6]])
    print(f"\n从列表创建的张量:\n{from_list}")
    
    # ========================================
    # 第3部分：张量的基本运算
    # ========================================
    print("\n📚 第3部分：张量的基本运算")
    print("-" * 30)
    
    # 创建两个简单的张量来做运算
    a = torch.tensor([1, 2, 3])
    b = torch.tensor([4, 5, 6])
    
    print(f"张量 a: {a}")
    print(f"张量 b: {b}")
    
    # 加法运算
    add_result = a + b
    print(f"\na + b = {add_result}")
    
    # 减法运算
    sub_result = a - b
    print(f"a - b = {sub_result}")
    
    # 乘法运算（逐个元素相乘）
    mul_result = a * b
    print(f"a * b = {mul_result}")
    
    # 除法运算
    div_result = a / b
    print(f"a / b = {div_result}")
    
    # 平方运算
    square_result = a ** 2
    print(f"a的平方 = {square_result}")
    
    # ========================================
    # 第4部分：张量的形状操作
    # ========================================
    print("\n📚 第4部分：改变张量的形状")
    print("-" * 30)
    
    # 创建一个1维张量
    original = torch.tensor([1, 2, 3, 4, 5, 6])
    print(f"原始张量: {original}")
    print(f"原始形状: {original.shape}")
    
    # 重新整理成2行3列的表格
    reshaped = original.reshape(2, 3)
    print(f"\n重新整理成2x3:\n{reshaped}")
    
    # 重新整理成3行2列的表格
    reshaped2 = original.reshape(3, 2)
    print(f"\n重新整理成3x2:\n{reshaped2}")
    
    # 转置（行列互换）
    transposed = reshaped.T
    print(f"\n转置后:\n{transposed}")
    
    # ========================================
    # 第5部分：张量的统计信息
    # ========================================
    print("\n📚 第5部分：计算张量的统计信息")
    print("-" * 30)
    
    # 创建一个示例张量
    data = torch.tensor([[1.0, 2.0, 3.0], 
                        [4.0, 5.0, 6.0]])
    print(f"数据张量:\n{data}")
    
    # 计算各种统计值
    print(f"\n最大值: {torch.max(data)}")
    print(f"最小值: {torch.min(data)}")
    print(f"平均值: {torch.mean(data)}")
    print(f"总和: {torch.sum(data)}")
    print(f"标准差: {torch.std(data)}")
    
    # ========================================
    # 第6部分：与NumPy的转换
    # ========================================
    print("\n📚 第6部分：PyTorch张量与NumPy数组的转换")
    print("-" * 30)
    
    # PyTorch张量转换为NumPy数组
    tensor = torch.tensor([1, 2, 3, 4, 5])
    numpy_array = tensor.numpy()
    print(f"PyTorch张量: {tensor}")
    print(f"转换为NumPy数组: {numpy_array}")
    print(f"NumPy数组类型: {type(numpy_array)}")
    
    # NumPy数组转换为PyTorch张量
    numpy_data = np.array([6, 7, 8, 9, 10])
    tensor_from_numpy = torch.from_numpy(numpy_data)
    print(f"\nNumPy数组: {numpy_data}")
    print(f"转换为PyTorch张量: {tensor_from_numpy}")
    print(f"张量类型: {type(tensor_from_numpy)}")
    
    # ========================================
    # 练习时间！
    # ========================================
    print("\n🎯 练习时间！")
    print("-" * 30)
    print("尝试修改这个文件中的代码：")
    print("1. 创建一个4x4的随机张量")
    print("2. 计算这个张量的平均值")
    print("3. 将它重新整理成2x8的形状")
    print("4. 试试看其他的数学运算")
    
    print("\n✅ 恭喜！您已经完成了PyTorch基础操作的学习！")
    print("💡 下一步：运行 02_simple_linear_regression.py 学习简单的机器学习")

if __name__ == "__main__":
    # 检查PyTorch是否正确安装
    try:
        import torch
        print(f"✅ PyTorch版本: {torch.__version__}")
        main()
    except ImportError:
        print("❌ PyTorch未安装！请先运行: pip install torch") 