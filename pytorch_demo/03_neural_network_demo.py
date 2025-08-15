#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神经网络分类示例
===============

这个文件将教您：
1. 什么是神经网络
2. 如何构建多层神经网络
3. 如何处理分类问题
4. 什么是激活函数
5. 如何评估模型性能

从线性回归进阶到神经网络！
"""

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def main():
    print("🚀 欢迎来到神经网络学习！")
    print("=" * 50)
    
    # ========================================
    # 第1部分：理解神经网络
    # ========================================
    print("\n📚 第1部分：什么是神经网络？")
    print("-" * 30)
    print("神经网络就像大脑中的神经元网络")
    print("每个神经元接收输入，进行计算，然后输出结果")
    print("多个神经元层层连接，就形成了神经网络")
    print("相比线性回归，神经网络可以学习更复杂的模式")
    
    # ========================================
    # 第2部分：生成分类数据
    # ========================================
    print("\n📚 第2部分：生成分类数据")
    print("-" * 30)
    
    # 设置随机种子
    torch.manual_seed(42)
    np.random.seed(42)
    
    # 生成2维分类数据
    X, y = make_classification(
        n_samples=1000,      # 1000个样本
        n_features=2,        # 2个特征(x1, x2)
        n_redundant=0,       # 无冗余特征
        n_informative=2,     # 2个信息特征
        n_clusters_per_class=1,  # 每类1个聚类
        random_state=42
    )
    
    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 转换为PyTorch张量
    X_train = torch.FloatTensor(X_train)
    X_test = torch.FloatTensor(X_test)
    y_train = torch.LongTensor(y_train)
    y_test = torch.LongTensor(y_test)
    
    print(f"训练集大小: {X_train.shape[0]} 个样本")
    print(f"测试集大小: {X_test.shape[0]} 个样本")
    print(f"特征维度: {X_train.shape[1]} 个特征")
    print(f"类别: {torch.unique(y_train).tolist()} (0和1两类)")
    
    # ========================================
    # 第3部分：可视化数据
    # ========================================
    print("\n📚 第3部分：可视化数据分布")
    print("-" * 30)
    
    plt.figure(figsize=(12, 4))
    
    # 训练数据可视化
    plt.subplot(1, 3, 1)
    colors = ['red', 'blue']
    for i, color in enumerate(colors):
        mask = y_train == i
        plt.scatter(X_train[mask, 0], X_train[mask, 1], 
                   c=color, label=f'类别 {i}', alpha=0.7)
    plt.xlabel('特征1')
    plt.ylabel('特征2')
    plt.title('训练数据分布')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # ========================================
    # 第4部分：定义神经网络
    # ========================================
    print("\n📚 第4部分：构建神经网络")
    print("-" * 30)
    
    class SimpleNeuralNetwork(nn.Module):
        def __init__(self, input_size, hidden_size, output_size):
            super(SimpleNeuralNetwork, self).__init__()
            # 第一层：输入层到隐藏层
            self.layer1 = nn.Linear(input_size, hidden_size)
            # 激活函数：ReLU (Rectified Linear Unit)
            self.relu = nn.ReLU()
            # 第二层：隐藏层到输出层
            self.layer2 = nn.Linear(hidden_size, output_size)
        
        def forward(self, x):
            # 前向传播过程
            x = self.layer1(x)     # 线性变换
            x = self.relu(x)       # 激活函数
            x = self.layer2(x)     # 输出层
            return x
    
    # 创建网络
    input_size = 2    # 2个输入特征
    hidden_size = 10  # 隐藏层10个神经元
    output_size = 2   # 2个输出类别
    
    model = SimpleNeuralNetwork(input_size, hidden_size, output_size)
    
    print(f"网络结构:")
    print(f"输入层: {input_size} 个神经元")
    print(f"隐藏层: {hidden_size} 个神经元 (使用ReLU激活函数)")
    print(f"输出层: {output_size} 个神经元")
    print(f"总参数数量: {sum(p.numel() for p in model.parameters())}")
    
    # ========================================
    # 第5部分：定义损失函数和优化器
    # ========================================
    print("\n📚 第5部分：定义损失函数和优化器")
    print("-" * 30)
    
    # 分类问题使用交叉熵损失
    criterion = nn.CrossEntropyLoss()
    print("损失函数：交叉熵损失(CrossEntropyLoss)")
    
    # 使用Adam优化器
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    print("优化器：Adam，学习率=0.01")
    
    # ========================================
    # 第6部分：训练神经网络
    # ========================================
    print("\n📚 第6部分：训练神经网络")
    print("-" * 30)
    
    num_epochs = 500
    train_losses = []
    train_accuracies = []
    
    print(f"开始训练，共{num_epochs}轮...")
    
    for epoch in range(num_epochs):
        # 训练模式
        model.train()
        
        # 前向传播
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # 计算准确率
        with torch.no_grad():
            _, predicted = torch.max(outputs, 1)
            accuracy = (predicted == y_train).float().mean().item()
        
        # 记录训练过程
        train_losses.append(loss.item())
        train_accuracies.append(accuracy)
        
        # 每50轮打印一次结果
        if (epoch + 1) % 50 == 0:
            print(f"第{epoch+1:3d}轮，损失：{loss.item():.4f}，准确率：{accuracy:.4f}")
    
    # ========================================
    # 第7部分：评估模型
    # ========================================
    print("\n📚 第7部分：评估模型性能")
    print("-" * 30)
    
    # 在测试集上评估
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test)
        test_loss = criterion(test_outputs, y_test)
        _, test_predicted = torch.max(test_outputs, 1)
        test_accuracy = (test_predicted == y_test).float().mean().item()
    
    print(f"测试集结果：")
    print(f"损失：{test_loss.item():.4f}")
    print(f"准确率：{test_accuracy:.4f} ({test_accuracy*100:.1f}%)")
    
    # ========================================
    # 第8部分：可视化结果
    # ========================================
    print("\n📚 第8部分：可视化训练结果")
    print("-" * 30)
    
    # 决策边界可视化
    def plot_decision_boundary(model, X, y, title):
        h = 0.01
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))
        
        mesh_points = torch.FloatTensor(np.c_[xx.ravel(), yy.ravel()])
        model.eval()
        with torch.no_grad():
            Z = model(mesh_points)
            _, Z = torch.max(Z, 1)
        Z = Z.reshape(xx.shape)
        
        plt.contourf(xx, yy, Z.numpy(), alpha=0.3, levels=1, colors=['lightcoral', 'lightblue'])
        
        colors = ['red', 'blue']
        for i, color in enumerate(colors):
            mask = y == i
            plt.scatter(X[mask, 0], X[mask, 1], c=color, label=f'类别 {i}', alpha=0.7)
        
        plt.xlabel('特征1')
        plt.ylabel('特征2')
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    # 测试数据和决策边界
    plt.subplot(1, 3, 2)
    plot_decision_boundary(model, X_test.numpy(), y_test.numpy(), 
                          f'测试集预测结果\n准确率: {test_accuracy:.3f}')
    
    # 训练过程
    plt.subplot(1, 3, 3)
    epochs_range = range(1, num_epochs + 1)
    plt.plot(epochs_range, train_losses, 'b-', label='训练损失', alpha=0.8)
    plt.xlabel('训练轮数')
    plt.ylabel('损失值')
    plt.title('训练过程')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pytorch_demo/neural_network_result.png', dpi=150, bbox_inches='tight')
    print("✅ 图表已保存为 'neural_network_result.png'")
    
    try:
        plt.show()
    except:
        print("💡 如果无法显示图表，请查看保存的PNG文件")
    
    # ========================================
    # 第9部分：理解激活函数
    # ========================================
    print("\n📚 第9部分：理解激活函数")
    print("-" * 30)
    
    # 展示不同激活函数的效果
    x = torch.linspace(-5, 5, 100)
    relu = torch.relu(x)
    sigmoid = torch.sigmoid(x)
    tanh = torch.tanh(x)
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.plot(x.numpy(), relu.numpy(), 'r-', linewidth=2, label='ReLU')
    plt.xlabel('输入')
    plt.ylabel('输出')
    plt.title('ReLU激活函数')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(1, 3, 2)
    plt.plot(x.numpy(), sigmoid.numpy(), 'g-', linewidth=2, label='Sigmoid')
    plt.xlabel('输入')
    plt.ylabel('输出')
    plt.title('Sigmoid激活函数')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(1, 3, 3)
    plt.plot(x.numpy(), tanh.numpy(), 'b-', linewidth=2, label='Tanh')
    plt.xlabel('输入')
    plt.ylabel('输出')
    plt.title('Tanh激活函数')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('pytorch_demo/activation_functions.png', dpi=150, bbox_inches='tight')
    print("✅ 激活函数图表已保存为 'activation_functions.png'")
    
    try:
        plt.show()
    except:
        print("💡 如果无法显示图表，请查看保存的PNG文件")
    
    print("\n激活函数说明：")
    print("• ReLU: 负数变0，正数不变，最常用")
    print("• Sigmoid: 压缩到0-1之间，用于概率输出")
    print("• Tanh: 压缩到-1到1之间，零点对称")
    
    # ========================================
    # 练习时间！
    # ========================================
    print("\n🎯 练习时间！")
    print("-" * 30)
    print("尝试修改这个文件中的参数：")
    print("1. 改变隐藏层神经元数量(hidden_size)")
    print("2. 尝试不同的激活函数(sigmoid, tanh)")
    print("3. 调整学习率和训练轮数")
    print("4. 添加更多隐藏层")
    print("5. 改变数据集的复杂度")
    
    print("\n✅ 恭喜！您已经完成了神经网络的学习！")
    print("🎉 您现在已经掌握了PyTorch的基础知识！")

if __name__ == "__main__":
    # 检查依赖
    try:
        import torch
        import matplotlib.pyplot as plt
        import sklearn
        print(f"✅ PyTorch版本: {torch.__version__}")
        print(f"✅ Scikit-learn版本: {sklearn.__version__}")
        main()
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install torch matplotlib scikit-learn") 