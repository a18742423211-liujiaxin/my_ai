#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单线性回归示例
===============

这个文件将教您：
1. 什么是线性回归
2. 如何生成训练数据
3. 如何定义模型和损失函数
4. 如何训练模型
5. 如何可视化训练过程

这是机器学习的"Hello World"！
"""

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

def main():
    print("🚀 欢迎来到线性回归学习！")
    print("=" * 50)
    
    # ========================================
    # 第1部分：理解线性回归
    # ========================================
    print("\n📚 第1部分：什么是线性回归？")
    print("-" * 30)
    print("线性回归就是找一条直线来拟合数据点")
    print("比如：房子面积 -> 房价，学习时间 -> 考试成绩")
    print("公式：y = w * x + b")
    print("其中：w是权重(斜率)，b是偏置(截距)")
    
    # ========================================
    # 第2部分：生成训练数据
    # ========================================
    print("\n📚 第2部分：生成训练数据")
    print("-" * 30)
    
    # 设置随机种子，确保每次运行结果一致
    torch.manual_seed(42)
    
    # 生成一些示例数据：y = 2 * x + 1 + 噪声
    # 比如：x是房子面积，y是房价
    true_w = 2.0  # 真实的权重
    true_b = 1.0  # 真实的偏置
    
    # 生成100个数据点
    n_samples = 100
    x = torch.randn(n_samples, 1) * 2  # x是从-4到4的随机数
    noise = torch.randn(n_samples, 1) * 0.5  # 添加一些噪声让数据更真实
    y = true_w * x + true_b + noise  # 真实的关系加上噪声
    
    print(f"生成了 {n_samples} 个数据点")
    print(f"真实关系：y = {true_w} * x + {true_b} + 噪声")
    print(f"数据范围：x从{x.min():.2f}到{x.max():.2f}")
    print(f"数据范围：y从{y.min():.2f}到{y.max():.2f}")
    
    # ========================================
    # 第3部分：定义模型
    # ========================================
    print("\n📚 第3部分：定义线性回归模型")
    print("-" * 30)
    
    # 在PyTorch中，nn.Linear就是线性层，它会自动学习w和b
    model = nn.Linear(1, 1)  # 输入1个特征，输出1个值
    
    # 查看模型的初始参数
    print("模型的初始参数：")
    for name, param in model.named_parameters():
        print(f"{name}: {param.data}")
    
    # ========================================
    # 第4部分：定义损失函数和优化器
    # ========================================
    print("\n📚 第4部分：定义损失函数和优化器")
    print("-" * 30)
    
    # 损失函数：均方误差(MSE)，衡量预测值和真实值的差距
    criterion = nn.MSELoss()
    print("损失函数：均方误差(MSE)")
    
    # 优化器：随机梯度下降(SGD)，用来更新模型参数
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    print("优化器：随机梯度下降(SGD)，学习率=0.01")
    
    # ========================================
    # 第5部分：训练模型
    # ========================================
    print("\n📚 第5部分：训练模型")
    print("-" * 30)
    
    # 记录训练过程
    num_epochs = 1000  # 训练1000轮
    losses = []  # 记录每轮的损失
    
    print(f"开始训练，共{num_epochs}轮...")
    
    for epoch in range(num_epochs):
        # 前向传播：计算预测值
        predictions = model(x)
        
        # 计算损失
        loss = criterion(predictions, y)
        
        # 反向传播：计算梯度
        optimizer.zero_grad()  # 清零之前的梯度
        loss.backward()        # 计算新的梯度
        optimizer.step()       # 更新参数
        
        # 记录损失
        losses.append(loss.item())
        
        # 每100轮打印一次结果
        if (epoch + 1) % 100 == 0:
            print(f"第{epoch+1}轮，损失：{loss.item():.4f}")
    
    # ========================================
    # 第6部分：查看训练结果
    # ========================================
    print("\n📚 第6部分：训练结果")
    print("-" * 30)
    
    # 查看学到的参数
    learned_params = list(model.parameters())
    learned_w = learned_params[0].item()
    learned_b = learned_params[1].item()
    
    print(f"真实参数：w={true_w}, b={true_b}")
    print(f"学到参数：w={learned_w:.4f}, b={learned_b:.4f}")
    print(f"参数误差：w误差={abs(learned_w-true_w):.4f}, b误差={abs(learned_b-true_b):.4f}")
    
    # ========================================
    # 第7部分：可视化结果
    # ========================================
    print("\n📚 第7部分：可视化训练结果")
    print("-" * 30)
    
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 左图：数据点和拟合直线
    model.eval()  # 设置为评估模式
    with torch.no_grad():
        # 生成一些测试点来画直线
        x_test = torch.linspace(-4, 4, 100).reshape(-1, 1)
        y_test = model(x_test)
        
        # 画数据点
        ax1.scatter(x.numpy(), y.numpy(), alpha=0.6, label='训练数据', color='blue')
        # 画拟合直线
        ax1.plot(x_test.numpy(), y_test.numpy(), 'r-', linewidth=2, 
                label=f'学到的直线: y={learned_w:.2f}x+{learned_b:.2f}')
        # 画真实直线
        y_true_line = true_w * x_test + true_b
        ax1.plot(x_test.numpy(), y_true_line.numpy(), 'g--', linewidth=2,
                label=f'真实直线: y={true_w}x+{true_b}')
    
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('线性回归结果')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 右图：训练损失曲线
    ax2.plot(losses, color='orange', linewidth=2)
    ax2.set_xlabel('训练轮数')
    ax2.set_ylabel('损失值')
    ax2.set_title('训练过程中的损失变化')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pytorch_demo/linear_regression_result.png', dpi=150, bbox_inches='tight')
    print("✅ 图表已保存为 'linear_regression_result.png'")
    
    try:
        plt.show()
    except:
        print("💡 如果无法显示图表，请查看保存的PNG文件")
    
    # ========================================
    # 第8部分：测试模型
    # ========================================
    print("\n📚 第8部分：用模型进行预测")
    print("-" * 30)
    
    # 测试几个新的输入
    test_inputs = torch.tensor([[0.0], [1.0], [2.0], [-1.0]])
    
    model.eval()
    with torch.no_grad():
        predictions = model(test_inputs)
        
        print("新数据预测测试：")
        for i, (input_val, pred_val) in enumerate(zip(test_inputs, predictions)):
            true_val = true_w * input_val + true_b
            print(f"输入: {input_val.item():4.1f} -> 预测: {pred_val.item():6.3f}, 真实: {true_val.item():6.3f}")
    
    # ========================================
    # 练习时间！
    # ========================================
    print("\n🎯 练习时间！")
    print("-" * 30)
    print("尝试修改这个文件中的参数：")
    print("1. 改变true_w和true_b的值，看看能否学到新的关系")
    print("2. 调整学习率(lr)，看看训练速度的变化")
    print("3. 改变训练轮数(num_epochs)")
    print("4. 调整噪声的大小，看看对训练的影响")
    
    print("\n✅ 恭喜！您已经完成了线性回归的学习！")
    print("💡 下一步：运行 03_neural_network_demo.py 学习神经网络")

if __name__ == "__main__":
    # 检查依赖
    try:
        import torch
        import matplotlib.pyplot as plt
        print(f"✅ PyTorch版本: {torch.__version__}")
        main()
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install torch matplotlib") 