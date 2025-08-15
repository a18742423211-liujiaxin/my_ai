# 大驴AI - 多模态AI创作平台

## 项目重构说明

本项目已从单页面应用重构为多页面应用，文件结构更加清晰，便于维护和扩展。

## 新的文件结构

```
project/
├── app.py                          # Flask主应用
├── requirements.txt                # Python依赖
├── README.md                       # 项目说明
├── apis/                          # API客户端模块
│   ├── __init__.py
│   ├── qwen_normal_api.py         # 通义千问普通模式
│   ├── qwen_thinking_api.py       # 通义千问深度思考模式
│   ├── hunyuan_new_api.py         # 腾讯混元API
│   ├── wanx_image_api.py          # 万象文生图API
│   └── cogvideo_api.py            # GLM视频生成API
├── static/                        # 静态资源
│   ├── css/
│   │   └── style.css              # 主样式文件
│   └── js/
│       ├── main.js                # 主要JavaScript功能
│       └── chat.js                # 聊天专用JavaScript
└── templates/                     # HTML模板
    ├── base.html                  # 基础模板
    ├── home.html                  # 首页
    ├── chat.html                  # AI对话页面
    ├── image.html                 # 文生图页面
    ├── video.html                 # 视频生成页面
    └── index_backup.html          # 原始单页面备份
```

## 页面说明

### 1. 基础模板 (`templates/base.html`)
- 包含导航栏、动态背景
- 引入CSS和JavaScript资源
- 定义页面的基本结构

### 2. 首页 (`templates/home.html`)
- 展示平台介绍和功能特色
- 美观的卡片布局展示三大功能

### 3. AI对话页面 (`templates/chat.html`)
- 支持多种AI模型切换
- 实现了深度思考模式的流式响应
- 思考过程可折叠显示

### 4. 文生图页面 (`templates/image.html`)
- 万象文生图API集成
- 支持多种图像尺寸选择

### 5. 视频生成页面 (`templates/video.html`)
- GLM CogVideoX API集成
- 支持多种视频参数配置

## 静态资源说明

### CSS (`static/css/style.css`)
- 统一的设计风格
- 深色主题配色
- 响应式设计
- 动画效果和交互样式

### JavaScript
- `main.js`: 页面切换、图像生成、视频生成等核心功能
- `chat.js`: 专门的聊天功能，支持流式响应

## 功能特色

### 🎯 深度思考模式
- 实时显示AI思考过程
- 思考内容可折叠/展开
- 流式响应提升用户体验

### 🎨 AI绘画
- 万象文生图API
- 多种尺寸选择
- 高质量图像生成

### 🎬 视频创作
- GLM CogVideoX视频生成
- 任务状态实时更新
- 支持多种视频参数

### 📱 响应式设计
- 完美适配移动端
- 流畅的动画效果
- 现代化UI设计

## 部署运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置API密钥（在各API文件中）

3. 运行应用：
```bash
python app.py
```

4. 访问地址：http://localhost:5000

## 开发优势

### 🔧 易于维护
- 代码分离，职责明确
- 模块化设计
- 易于调试和修改

### 🚀 易于扩展
- 新页面只需创建对应模板
- 功能模块独立
- 样式统一管理

### 💡 用户体验
- 页面加载更快
- 导航更直观
- 功能更专注

## 技术栈

- **后端**: Flask, Python
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **UI框架**: 自定义CSS框架
- **图标**: Font Awesome
- **AI模型**: 通义千问、腾讯混元、万象、GLM

## 更新日志

### v2.0.0 (当前版本)
- ✅ 重构为多页面应用架构
- ✅ 提取CSS到独立文件
- ✅ 提取JavaScript到模块化文件
- ✅ 优化深度思考模式的用户体验
- ✅ 修复导航栏悬停跳转问题
- ✅ 完善响应式设计

### v1.0.0
- 单页面应用版本
- 基础AI功能集成

---

**注意**: 原始的单页面文件已备份为 `index_backup.html`，如需回滚可以参考。 