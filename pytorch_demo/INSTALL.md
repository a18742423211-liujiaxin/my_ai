# PyTorch 安装指南 📦

## 快速安装 (推荐)

### 1. 安装PyTorch (CPU版本)
```bash
pip install torch torchvision torchaudio
```

### 2. 安装其他依赖
```bash
pip install matplotlib scikit-learn numpy jupyter
```

### 3. 一键安装所有依赖
```bash
pip install -r requirements.txt
```

## 验证安装

运行以下命令验证PyTorch是否正确安装：

```bash
python -c "import torch; print('PyTorch版本:', torch.__version__); print('安装成功!')"
```

## 开始学习

安装完成后，您可以：

1. **逐个运行示例**：
   ```bash
   python 01_basic_operations.py
   python 02_simple_linear_regression.py
   python 03_neural_network_demo.py
   ```

2. **一键运行所有示例**：
   ```bash
   python run_all_examples.py
   ```

## 故障排除

如果遇到问题：

1. **确保Python版本**：建议使用Python 3.8+
2. **网络问题**：如果下载慢，可以使用国内镜像：
   ```bash
   pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
3. **权限问题**：在命令前加 `--user`：
   ```bash
   pip install --user torch
   ```

## GPU版本 (可选)

如果您有NVIDIA GPU且想体验GPU加速：

1. 访问 https://pytorch.org/
2. 选择您的系统配置
3. 复制相应的安装命令

祝您学习愉快！🎉 