# Render 部署配置指南

## 🚀 部署步骤

### 1. 在 Render 中创建 Web Service

1. 登录 [Render.com](https://render.com)
2. 点击 "New" -> "Web Service"
3. 连接你的 GitHub 仓库: `a18742423211-liujiaxin/my_ai`
4. 配置基本信息：
   - **Name**: `my-ai-chatbot`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

### 2. 配置环境变量

在 Render 的 Environment 选项卡中添加以下环境变量：

#### 必需的 API 密钥

```
DASHSCOPE_API_KEY=你的阿里云DashScope API密钥
HUNYUAN_API_KEY=你的腾讯混元API密钥
```

#### 应用配置

```
FLASK_ENV=production
PORT=10000
PYTHON_VERSION=3.9.16
```

### 3. API 密钥获取方法

#### 阿里云 DashScope API Key

1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 登录后进入 API-KEY 管理
3. 创建新的 API Key
4. 复制密钥并设置为 `DASHSCOPE_API_KEY`

#### 腾讯混元 API Key

1. 访问 [腾讯云混元大模型](https://cloud.tencent.com/product/hunyuan)
2. 开通服务并创建 API Key
3. 复制密钥并设置为 `HUNYUAN_API_KEY`

### 4. 部署后验证

部署完成后，访问你的应用 URL，应该能看到：

- ✅ 聊天界面正常加载
- ✅ 可以选择不同模型
- ✅ 消息发送和接收正常
- ✅ 图像生成功能正常

### 5. 常见问题解决

#### 问题：应用启动失败

**解决方案**：

- 检查环境变量是否正确设置
- 查看 Render 的部署日志
- 确保 API 密钥有效且有足够余额

#### 问题：API 调用失败

**解决方案**：

- 验证 API 密钥是否正确
- 检查 API 服务是否正常
- 查看应用日志中的错误信息

#### 问题：静态文件加载失败

**解决方案**：

- 确保 `templates` 和 `static` 文件夹已推送到 GitHub
- 检查文件路径是否正确

### 6. 监控和维护

- 定期检查 API 余额
- 监控应用性能和错误日志
- 及时更新依赖包版本

## 📝 注意事项

1. **安全性**: 不要在代码中硬编码 API 密钥，使用环境变量
2. **成本控制**: 监控 API 调用量，避免超出预算
3. **备份**: 定期备份重要配置和数据

## 🔗 相关链接

- [Render 官方文档](https://render.com/docs)
- [阿里云百炼平台](https://bailian.console.aliyun.com/)
- [腾讯云混元大模型](https://cloud.tencent.com/product/hunyuan)
