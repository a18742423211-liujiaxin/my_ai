// 全局变量
let currentTutorial = null;
let regressionData = null;
let isTraining = false;
let trainingInterval = null;
let networkStructure = { input: 3, hidden: 4, output: 2 };

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    updateTensorVisualization();
    updateNetworkStructure();
    initializeRegressionData();
    setupEventListeners();
});

// 初始化应用
function initializeApp() {
    console.log('PyTorch 学习平台已加载');
    
    // 初始化回到顶部按钮
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
    }
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 设置事件监听器
function setupEventListeners() {
    // 张量大小滑块
    const tensorSizeSlider = document.getElementById('tensorSize');
    if (tensorSizeSlider) {
        tensorSizeSlider.addEventListener('input', function() {
            document.getElementById('tensorSizeValue').textContent = this.value;
        });
    }
    
    // 学习率滑块
    const learningRateSlider = document.getElementById('learningRate');
    if (learningRateSlider) {
        learningRateSlider.addEventListener('input', function() {
            document.getElementById('learningRateValue').textContent = this.value;
        });
    }
    
    // 训练轮数滑块
    const epochsSlider = document.getElementById('epochs');
    if (epochsSlider) {
        epochsSlider.addEventListener('input', function() {
            document.getElementById('epochsValue').textContent = this.value;
        });
    }
    
    // 数据点数滑块
    const dataPointsSlider = document.getElementById('dataPoints');
    if (dataPointsSlider) {
        dataPointsSlider.addEventListener('input', function() {
            document.getElementById('dataPointsValue').textContent = this.value;
        });
    }
    
    // 神经网络结构滑块
    ['inputNodes', 'hiddenNodes', 'outputNodes'].forEach(id => {
        const slider = document.getElementById(id);
        if (slider) {
            slider.addEventListener('input', function() {
                document.getElementById(id + 'Value').textContent = this.value;
            });
        }
    });
}

// 滚动到指定部分
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// 回到顶部
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// 张量可视化功能
function updateTensorVisualization() {
    const shape = document.getElementById('tensorShape').value;
    const size = parseInt(document.getElementById('tensorSize').value);
    const container = document.getElementById('tensorVisualization');
    
    if (!container) return;
    
    // 生成示例数据
    let data, layout;
    
    switch(shape) {
        case '1d':
            data = [{
                y: Array.from({length: size}, () => Math.random() * 10 - 5),
                type: 'scatter',
                mode: 'lines+markers',
                line: {color: '#ee6730'},
                marker: {size: 8}
            }];
            layout = {
                title: `1D 张量 (长度: ${size})`,
                xaxis: {title: '索引'},
                yaxis: {title: '值'},
                margin: {t: 50, r: 30, l: 50, b: 50}
            };
            break;
            
        case '2d':
            const matrix = Array.from({length: size}, () => 
                Array.from({length: size}, () => Math.random() * 10 - 5)
            );
            data = [{
                z: matrix,
                type: 'heatmap',
                colorscale: 'Viridis'
            }];
            layout = {
                title: `2D 张量 (${size}x${size})`,
                xaxis: {title: '列'},
                yaxis: {title: '行'},
                margin: {t: 50, r: 30, l: 50, b: 50}
            };
            break;
            
        case '3d':
            const points = Array.from({length: size * size}, () => ({
                x: Math.random() * 10 - 5,
                y: Math.random() * 10 - 5,
                z: Math.random() * 10 - 5
            }));
            data = [{
                x: points.map(p => p.x),
                y: points.map(p => p.y),
                z: points.map(p => p.z),
                mode: 'markers',
                marker: {
                    size: 5,
                    color: points.map(p => p.z),
                    colorscale: 'Viridis'
                },
                type: 'scatter3d'
            }];
            layout = {
                title: `3D 张量 (${size}x${size} 点)`,
                scene: {
                    xaxis: {title: 'X'},
                    yaxis: {title: 'Y'},
                    zaxis: {title: 'Z'}
                },
                margin: {t: 50, r: 30, l: 50, b: 50}
            };
            break;
    }
    
    Plotly.newPlot(container, data, layout, {responsive: true});
}

// 生成随机张量
function generateRandomTensor() {
    updateTensorVisualization();
    
    // 显示生成信息
    const shape = document.getElementById('tensorShape').value;
    const size = document.getElementById('tensorSize').value;
    
    console.log(`生成了新的 ${shape} 张量，大小: ${size}`);
    
    // 可以在这里添加更多的张量操作演示
    showToast(`已生成新的 ${shape.toUpperCase()} 张量！`);
}

// 初始化回归数据
function initializeRegressionData() {
    const numPoints = parseInt(document.getElementById('dataPoints')?.value || 50);
    
    // 生成线性回归的真实数据
    const trueSlope = 2.5;
    const trueIntercept = 1.0;
    const noise = 0.5;
    
    const x = Array.from({length: numPoints}, (_, i) => (i / numPoints) * 10 - 5);
    const y = x.map(xi => trueSlope * xi + trueIntercept + (Math.random() - 0.5) * noise * 2);
    
    regressionData = {
        x: x,
        y: y,
        trueSlope: trueSlope,
        trueIntercept: trueIntercept,
        currentSlope: Math.random() * 2,
        currentIntercept: Math.random() * 2,
        losses: []
    };
    
    plotRegressionData();
}

// 绘制回归数据
function plotRegressionData() {
    if (!regressionData) return;
    
    const container = document.getElementById('regressionPlot');
    if (!container) return;
    
    const { x, y, currentSlope, currentIntercept } = regressionData;
    const predictedY = x.map(xi => currentSlope * xi + currentIntercept);
    
    const data = [
        {
            x: x,
            y: y,
            mode: 'markers',
            type: 'scatter',
            name: '训练数据',
            marker: {
                color: '#ee6730',
                size: 8
            }
        },
        {
            x: x,
            y: predictedY,
            mode: 'lines',
            type: 'scatter',
            name: '预测线',
            line: {
                color: '#f7931e',
                width: 3
            }
        }
    ];
    
    const layout = {
        title: '线性回归训练过程',
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' },
        margin: {t: 50, r: 30, l: 50, b: 50},
        showlegend: true
    };
    
    Plotly.newPlot(container, data, layout, {responsive: true});
}

// 开始回归训练
function startRegressionTraining() {
    if (isTraining) {
        stopTraining();
        return;
    }
    
    const learningRate = parseFloat(document.getElementById('learningRate').value);
    const maxEpochs = parseInt(document.getElementById('epochs').value);
    const trainBtn = document.getElementById('trainBtn');
    
    isTraining = true;
    trainBtn.innerHTML = '<i class="fas fa-stop"></i> 停止训练';
    
    let currentEpoch = 0;
    
    trainingInterval = setInterval(() => {
        if (currentEpoch >= maxEpochs) {
            stopTraining();
            return;
        }
        
        // 执行一步梯度下降
        performGradientStep(learningRate);
        currentEpoch++;
        
        // 更新显示
        document.getElementById('currentEpoch').textContent = currentEpoch;
        
        // 每10步更新一次图表
        if (currentEpoch % 10 === 0 || currentEpoch === maxEpochs) {
            plotRegressionData();
        }
        
    }, 100); // 每100ms一步
}

// 执行梯度下降步骤
function performGradientStep(learningRate) {
    if (!regressionData) return;
    
    const { x, y } = regressionData;
    const m = x.length;
    
    // 计算预测值
    const predictions = x.map(xi => regressionData.currentSlope * xi + regressionData.currentIntercept);
    
    // 计算损失
    const loss = predictions.reduce((sum, pred, i) => sum + Math.pow(pred - y[i], 2), 0) / (2 * m);
    regressionData.losses.push(loss);
    
    // 计算梯度
    const slopeGradient = predictions.reduce((sum, pred, i) => sum + (pred - y[i]) * x[i], 0) / m;
    const interceptGradient = predictions.reduce((sum, pred, i) => sum + (pred - y[i]), 0) / m;
    
    // 更新参数
    regressionData.currentSlope -= learningRate * slopeGradient;
    regressionData.currentIntercept -= learningRate * interceptGradient;
    
    // 更新损失显示
    document.getElementById('currentLoss').textContent = loss.toFixed(3);
}

// 停止训练
function stopTraining() {
    if (trainingInterval) {
        clearInterval(trainingInterval);
        trainingInterval = null;
    }
    
    isTraining = false;
    const trainBtn = document.getElementById('trainBtn');
    if (trainBtn) {
        trainBtn.innerHTML = '<i class="fas fa-play"></i> 开始训练';
    }
}

// 重置回归
function resetRegression() {
    stopTraining();
    initializeRegressionData();
    document.getElementById('currentEpoch').textContent = '0';
    document.getElementById('currentLoss').textContent = '0.000';
}

// 更新神经网络结构
function updateNetworkStructure() {
    const inputNodes = parseInt(document.getElementById('inputNodes')?.value || 3);
    const hiddenNodes = parseInt(document.getElementById('hiddenNodes')?.value || 4);
    const outputNodes = parseInt(document.getElementById('outputNodes')?.value || 2);
    const activation = document.getElementById('activationFunction')?.value || 'relu';
    
    networkStructure = { input: inputNodes, hidden: hiddenNodes, output: outputNodes, activation: activation };
    
    // 计算参数数量
    const totalParams = (inputNodes * hiddenNodes) + hiddenNodes + (hiddenNodes * outputNodes) + outputNodes;
    
    // 更新显示
    if (document.getElementById('totalParams')) {
        document.getElementById('totalParams').textContent = totalParams;
    }
    
    // 绘制网络结构
    drawNetworkStructure();
}

// 绘制神经网络结构
function drawNetworkStructure() {
    const container = document.getElementById('networkStructure');
    if (!container) return;
    
    const { input, hidden, output } = networkStructure;
    
    // 创建SVG
    container.innerHTML = `
        <svg width="100%" height="100%" viewBox="0 0 400 300">
            <!-- 输入层 -->
            <g class="input-layer">
                <text x="50" y="20" text-anchor="middle" font-size="12" fill="#666">输入层</text>
                ${Array.from({length: input}, (_, i) => {
                    const y = 50 + (i * (200 / Math.max(input - 1, 1)));
                    return `<circle cx="50" cy="${y}" r="15" fill="#ee6730" opacity="0.8"/>`;
                }).join('')}
            </g>
            
            <!-- 隐藏层 -->
            <g class="hidden-layer">
                <text x="200" y="20" text-anchor="middle" font-size="12" fill="#666">隐藏层</text>
                ${Array.from({length: hidden}, (_, i) => {
                    const y = 50 + (i * (200 / Math.max(hidden - 1, 1)));
                    return `<circle cx="200" cy="${y}" r="15" fill="#f7931e" opacity="0.8"/>`;
                }).join('')}
            </g>
            
            <!-- 输出层 -->
            <g class="output-layer">
                <text x="350" y="20" text-anchor="middle" font-size="12" fill="#666">输出层</text>
                ${Array.from({length: output}, (_, i) => {
                    const y = 50 + (i * (200 / Math.max(output - 1, 1)));
                    return `<circle cx="350" cy="${y}" r="15" fill="#ff6b35" opacity="0.8"/>`;
                }).join('')}
            </g>
            
            <!-- 连接线 -->
            <g class="connections" opacity="0.3">
                ${Array.from({length: input}, (_, i) => {
                    const inputY = 50 + (i * (200 / Math.max(input - 1, 1)));
                    return Array.from({length: hidden}, (_, j) => {
                        const hiddenY = 50 + (j * (200 / Math.max(hidden - 1, 1)));
                        return `<line x1="65" y1="${inputY}" x2="185" y2="${hiddenY}" stroke="#666" stroke-width="1"/>`;
                    }).join('');
                }).join('')}
                
                ${Array.from({length: hidden}, (_, i) => {
                    const hiddenY = 50 + (i * (200 / Math.max(hidden - 1, 1)));
                    return Array.from({length: output}, (_, j) => {
                        const outputY = 50 + (j * (200 / Math.max(output - 1, 1)));
                        return `<line x1="215" y1="${hiddenY}" x2="335" y2="${outputY}" stroke="#666" stroke-width="1"/>`;
                    }).join('');
                }).join('')}
            </g>
            
            <!-- 激活函数标注 -->
            <text x="200" y="280" text-anchor="middle" font-size="11" fill="#999">激活函数: ${networkStructure.activation.toUpperCase()}</text>
        </svg>
    `;
}

// 教程相关功能
function openTutorial(tutorialType) {
    const modal = document.getElementById('tutorialModal');
    const title = document.getElementById('tutorialTitle');
    const content = document.getElementById('tutorialContent');
    
    if (!modal || !title || !content) return;
    
    const tutorials = {
        'basic': {
            title: 'PyTorch 基础操作',
            content: `
                <h3>学习目标</h3>
                <ul>
                    <li>了解什么是张量(Tensor)</li>
                    <li>学习张量的创建和基本操作</li>
                    <li>掌握张量的形状变换</li>
                </ul>
                
                <h3>核心概念</h3>
                <p><strong>张量(Tensor)</strong>是PyTorch中最基本的数据结构，类似于NumPy的数组，但可以在GPU上运行。</p>
                
                <h3>代码示例</h3>
                <pre><code>import torch

# 创建张量
x = torch.tensor([1, 2, 3, 4, 5])
print(f"张量: {x}")
print(f"形状: {x.shape}")
print(f"数据类型: {x.dtype}")

# 创建随机张量
y = torch.randn(3, 4)
print(f"随机张量: {y}")

# 张量运算
z = x * 2
print(f"乘法运算: {z}")</code></pre>
                
                <h3>练习</h3>
                <p>尝试在右侧的实验室中运行这些代码，观察结果的变化。</p>
            `
        },
        'regression': {
            title: '线性回归',
            content: `
                <h3>学习目标</h3>
                <ul>
                    <li>理解线性回归的基本原理</li>
                    <li>学习梯度下降算法</li>
                    <li>掌握损失函数的概念</li>
                </ul>
                
                <h3>核心概念</h3>
                <p><strong>线性回归</strong>试图找到一条直线来最好地拟合数据点。</p>
                <p>数学表达式: y = wx + b</p>
                
                <h3>梯度下降</h3>
                <p>通过不断调整参数w和b来最小化预测误差。</p>
                
                <h3>代码示例</h3>
                <pre><code>import torch
import torch.nn as nn

# 准备数据
x = torch.randn(100, 1)
y = 2 * x + 1 + torch.randn(100, 1) * 0.1

# 定义模型
model = nn.Linear(1, 1)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练循环
for epoch in range(100):
    # 前向传播
    pred = model(x)
    loss = criterion(pred, y)
    
    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')</code></pre>
            `
        },
        'neural-network': {
            title: '神经网络',
            content: `
                <h3>学习目标</h3>
                <ul>
                    <li>了解神经网络的基本结构</li>
                    <li>学习激活函数的作用</li>
                    <li>掌握多层网络的构建</li>
                </ul>
                
                <h3>核心概念</h3>
                <p><strong>神经网络</strong>由多个神经元组成，每个神经元接收输入，进行加权求和，然后通过激活函数输出。</p>
                
                <h3>激活函数</h3>
                <ul>
                    <li><strong>ReLU</strong>: f(x) = max(0, x) - 最常用</li>
                    <li><strong>Sigmoid</strong>: f(x) = 1/(1+e^(-x)) - 输出0-1</li>
                    <li><strong>Tanh</strong>: f(x) = tanh(x) - 输出-1到1</li>
                </ul>
                
                <h3>代码示例</h3>
                <pre><code>import torch
import torch.nn as nn
import torch.nn.functional as F

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 创建网络
model = NeuralNetwork(3, 4, 2)
print(model)

# 前向传播
input_data = torch.randn(1, 3)
output = model(input_data)
print(f"输出: {output}")</code></pre>
            `
        }
    };
    
    const tutorial = tutorials[tutorialType];
    if (tutorial) {
        title.textContent = tutorial.title;
        content.innerHTML = tutorial.content;
        modal.style.display = 'block';
        currentTutorial = tutorialType;
    }
}

// 关闭教程模态框
function closeTutorialModal() {
    const modal = document.getElementById('tutorialModal');
    if (modal) {
        modal.style.display = 'none';
        currentTutorial = null;
    }
}

// 代码编辑器功能
const codeExamples = {
    'basic': `# PyTorch 基础操作示例
import torch
import numpy as np

# 创建张量
x = torch.tensor([1, 2, 3, 4, 5])
print(f"张量 x: {x}")
print(f"张量形状: {x.shape}")
print(f"张量数据类型: {x.dtype}")

# 基本运算
y = x * 2
print(f"x * 2 = {y}")

# 矩阵运算
A = torch.randn(3, 4)
B = torch.randn(4, 2)
C = torch.matmul(A, B)
print(f"矩阵乘法结果形状: {C.shape}")`,

    'regression': `# 线性回归示例
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# 生成训练数据
torch.manual_seed(42)
x = torch.randn(100, 1)
y = 2 * x + 1 + torch.randn(100, 1) * 0.1

# 定义线性模型
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)
    
    def forward(self, x):
        return self.linear(x)

# 创建模型实例
model = LinearRegression()
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 训练模型
losses = []
for epoch in range(1000):
    # 前向传播
    y_pred = model(x)
    loss = criterion(y_pred, y)
    
    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    losses.append(loss.item())
    
    if epoch % 100 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')

print(f"训练完成! 最终损失: {losses[-1]:.4f}")`,

    'neural': `# 神经网络分类示例
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# 定义神经网络
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

# 创建模型
input_size = 784  # 28x28 图像
hidden_size = 128
num_classes = 10
model = NeuralNetwork(input_size, hidden_size, num_classes)

# 打印模型结构
print(model)

# 计算参数数量
total_params = sum(p.numel() for p in model.parameters())
print(f"总参数数量: {total_params}")

# 模拟前向传播
x = torch.randn(32, input_size)  # 批次大小为32
output = model(x)
print(f"输出形状: {output.shape}")
print(f"输出示例: {output[0]}")`
};

// 切换代码标签
function switchTab(tabType) {
    // 更新标签样式
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // 更新代码内容
    const codeDisplay = document.getElementById('codeDisplay');
    if (codeDisplay && codeExamples[tabType]) {
        codeDisplay.innerHTML = `<code>${codeExamples[tabType]}</code>`;
    }
}

// 运行代码
function runCode() {
    const output = document.getElementById('outputConsole');
    if (!output) return;
    
    // 模拟代码执行
    const timestamp = new Date().toLocaleTimeString();
    
    output.innerHTML = `
        <div class="console-line">[${timestamp}] 开始执行代码...</div>
        <div class="console-line">PyTorch 版本: 2.0.0</div>
        <div class="console-line">CUDA 可用: ${Math.random() > 0.5 ? 'True' : 'False'}</div>
        <div class="console-line">────────────────────────────────</div>
        <div class="console-line">张量 x: tensor([1, 2, 3, 4, 5])</div>
        <div class="console-line">张量形状: torch.Size([5])</div>
        <div class="console-line">张量数据类型: torch.int64</div>
        <div class="console-line">x * 2 = tensor([ 2,  4,  6,  8, 10])</div>
        <div class="console-line">矩阵乘法结果形状: torch.Size([3, 2])</div>
        <div class="console-line">────────────────────────────────</div>
        <div class="console-line" style="color: #48bb78;">[${timestamp}] 代码执行完成!</div>
    `;
    
    // 滚动到底部
    output.scrollTop = output.scrollHeight;
}

// 复制代码
function copyCode() {
    const codeDisplay = document.getElementById('codeDisplay');
    if (!codeDisplay) return;
    
    const code = codeDisplay.textContent;
    navigator.clipboard.writeText(code).then(() => {
        showToast('代码已复制到剪贴板!');
    }).catch(() => {
        showToast('复制失败，请手动选择复制', 'error');
    });
}

// 下载代码
function downloadCode() {
    const codeDisplay = document.getElementById('codeDisplay');
    if (!codeDisplay) return;
    
    const code = codeDisplay.textContent;
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pytorch_example.py';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('代码文件已下载!');
}

// 打开本地项目
function openLocalProject() {
    // 这里可以集成与本地PyTorch项目的交互
    showToast('正在打开本地PyTorch项目...', 'info');
    
    // 模拟项目信息
    setTimeout(() => {
        const output = document.getElementById('outputConsole');
        if (output) {
            const timestamp = new Date().toLocaleTimeString();
            output.innerHTML = `
                <div class="console-line">[${timestamp}] 连接到本地项目...</div>
                <div class="console-line">项目路径: C:\\Users\\Administrator\\Desktop\\test\\pytorch_demo</div>
                <div class="console-line">发现文件:</div>
                <div class="console-line">  - index.html</div>
                <div class="console-line">  - styles.css</div>
                <div class="console-line">  - script.js</div>
                <div class="console-line">────────────────────────────────</div>
                <div class="console-line">建议创建 Python 文件:</div>
                <div class="console-line">  - basic_operations.py</div>
                <div class="console-line">  - linear_regression.py</div>
                <div class="console-line">  - neural_network.py</div>
                <div class="console-line" style="color: #48bb78;">本地项目集成完成!</div>
            `;
            output.scrollTop = output.scrollHeight;
        }
    }, 1000);
}

// 显示提示消息
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 3000;
        animation: slideIn 0.3s ease-out;
        ${type === 'success' ? 'background: #48bb78;' : ''}
        ${type === 'error' ? 'background: #f56565;' : ''}
        ${type === 'info' ? 'background: #4299e1;' : ''}
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// 移动端导航菜单
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    const navToggle = document.getElementById('navToggle');
    
    if (navMenu && navToggle) {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    }
}

// 页面滚动时的视差效果
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.hero');
    
    if (parallax) {
        const speed = scrolled * 0.5;
        parallax.style.transform = `translateY(${speed}px)`;
    }
});

// 监听窗口大小变化，重绘图表
window.addEventListener('resize', function() {
    setTimeout(() => {
        if (typeof Plotly !== 'undefined') {
            Plotly.Plots.resize(document.getElementById('tensorVisualization'));
            Plotly.Plots.resize(document.getElementById('regressionPlot'));
        }
    }, 100);
});

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    // Esc 键关闭模态框
    if (e.key === 'Escape') {
        closeTutorialModal();
    }
    
    // Ctrl+Enter 运行代码
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        runCode();
    }
});

// 初始化图表主题
if (typeof Plotly !== 'undefined') {
    Plotly.setPlotConfig({
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false,
        responsive: true
    });
} 