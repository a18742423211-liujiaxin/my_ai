# PyTorch 学习展示平台

一个交互式的Web平台，帮助学习和理解PyTorch深度学习框架的核心概念。

## 🚀 功能特性

### 📚 学习路径
- **基础操作**: 学习PyTorch张量的创建、操作和基本运算
- **线性回归**: 理解机器学习的基础 - 线性回归模型
- **神经网络**: 构建和训练多层神经网络模型

### 🎮 交互式演示
- **张量可视化**: 实时可视化1D、2D、3D张量数据
- **线性回归训练**: 可视化梯度下降训练过程
- **神经网络结构设计**: 交互式设计和可视化网络架构

### 🧪 实验室
- **代码编辑器**: 内置PyTorch代码示例
- **实时运行**: 模拟代码执行和结果展示
- **代码下载**: 将示例代码保存为Python文件

### 📖 学习资源
- 官方文档链接
- 本地项目集成
- 社区资源

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **可视化**: Plotly.js
- **图标**: Font Awesome
- **样式**: 现代CSS Grid/Flexbox布局
- **主题**: PyTorch官方配色方案

## 🎨 设计特色

- 🎯 现代化UI设计，采用PyTorch官方配色
- 📱 完全响应式设计，支持移动端
- 🎭 流畅的动画效果和交互反馈
- 🌟 神经网络可视化动画
- 🔧 实时参数调节和即时反馈

## 📁 项目结构

```
pytorch_demo/
├── index.html          # 主页面
├── styles.css          # 样式文件
├── script.js           # 交互功能
└── README.md           # 项目说明
```

## 🚀 快速开始

1. **打开项目**
   ```bash
   # 在浏览器中打开
   open index.html
   ```

2. **本地服务器运行**（推荐）
   ```bash
   # Python 3
   python -m http.server 8000
   
   # 或者使用Node.js
   npx http-server
   ```

3. **访问地址**
   ```
   http://localhost:8000
   ```

## 🎯 使用指南

### 学习路径
1. 点击导航栏中的"教程"
2. 选择感兴趣的主题（基础操作/线性回归/神经网络）
3. 点击"开始学习"查看详细教程

### 交互演示
1. 进入"演示"部分
2. **张量可视化**:
   - 选择张量维度（1D/2D/3D）
   - 调整张量大小
   - 点击"随机生成"查看新数据
3. **线性回归训练**:
   - 调整学习率、训练轮数、数据点数
   - 点击"开始训练"观看训练过程
   - 实时查看损失值变化
4. **神经网络设计**:
   - 调整各层神经元数量
   - 选择激活函数
   - 查看参数统计

### 实验室
1. 进入"实验室"部分
2. 选择代码示例标签
3. 点击"运行代码"查看执行结果
4. 使用"复制代码"或"下载代码"保存示例

## 🎨 自定义配置

### 修改主题颜色
在 `styles.css` 中修改CSS变量:
```css
:root {
    --primary-color: #ee6730;      /* PyTorch 橙色 */
    --secondary-color: #f7931e;    /* 辅助橙色 */
    --accent-color: #ff6b35;       /* 强调色 */
}
```

### 添加新的代码示例
在 `script.js` 中的 `codeExamples` 对象添加:
```javascript
const codeExamples = {
    'basic': '...',
    'regression': '...',
    'neural': '...',
    'new_example': `# 新示例
import torch
# 你的代码...`
};
```

## 🔗 集成指南

### 与现有PyTorch项目集成
1. 将项目文件放在PyTorch项目根目录
2. 修改 `openLocalProject()` 函数
3. 添加实际的文件读取和执行逻辑

### 添加真实的代码执行
```javascript
// 替换 runCode() 函数中的模拟执行
function runCode() {
    // 发送代码到后端Python服务器
    fetch('/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: getCodeFromEditor() })
    })
    .then(response => response.json())
    .then(result => displayOutput(result));
}
```

## 🎓 学习建议

1. **按顺序学习**: 基础操作 → 线性回归 → 神经网络
2. **动手实践**: 在实验室中运行和修改代码
3. **参数调优**: 尝试不同的超参数组合
4. **可视化理解**: 观察训练过程和网络结构变化

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 贡献指南
1. Fork 项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交Pull Request

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🔮 未来规划

- [ ] 添加CNN可视化
- [ ] 集成真实的Python执行环境
- [ ] 添加更多深度学习算法演示
- [ ] 支持数据集上传和可视化
- [ ] 添加模型性能评估工具
- [ ] 集成TensorBoard可视化

## 📞 联系信息

- 项目地址: [GitHub Repository](#)
- 问题报告: [Issues](#)
- 文档: [Wiki](#)

---

**让深度学习变得简单易懂！** 🧠✨ 