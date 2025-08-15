# API配置文件
import os
from dotenv import load_dotenv

# 加载 .env（如果存在）
load_dotenv()

# 通义千问API配置
QWEN_CONFIG = {
    "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "api_key": os.getenv('DASHSCOPE_API_KEY', ''),
    "model": "qwen-plus-2025-04-28",  # 支持深度思考的模型
    "timeout": 30,
    "max_tokens": 2000,
    "temperature": 0.7,
    "top_p": 0.8
}

# 通义万相文生图API配置
WANX_CONFIG = {
    "api_base": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "api_key": os.getenv('DASHSCOPE_API_KEY', ''),
    "model": "wanx-v1",
    "timeout": 60,
    "poll_timeout": 10,
    "max_poll_attempts": 30,
    "poll_interval": 2,
    "default_style": "<auto>",
    "default_size": "1024*1024",
    "default_n": 1
}

# 腾讯混元API配置
HUNYUAN_CONFIG = {
    "api_base": "https://api.hunyuan.cloud.tencent.com/v1",
    "api_key": os.getenv('HUNYUAN_API_KEY', ''),
    "model": "hunyuan-turbos-latest",
    "timeout": 30,
    "max_tokens": 2000,
    "temperature": 0.7,
    "enable_enhancement": True
}

# Flask应用配置
APP_CONFIG = {
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000)),
    'debug': os.getenv('FLASK_ENV') != 'production'
}

# 模型信息配置
MODELS_INFO = {
    'qwen': {
        'name': '通义千问',
        'model': QWEN_CONFIG['model'],
        'api_base': QWEN_CONFIG['api_base']
    },
    'hunyuan': {
        'name': '腾讯混元',
        'model': HUNYUAN_CONFIG['model'],
        'api_base': HUNYUAN_CONFIG['api_base']
    },
    'wanx': {
        'name': '通义万相',
        'model': WANX_CONFIG['model'],
        'api_base': WANX_CONFIG['api_base']
    }
} 