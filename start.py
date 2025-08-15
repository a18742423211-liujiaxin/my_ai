#!/usr/bin/env python3
import os
import sys
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """检查环境变量和依赖"""
    required_vars = ['DASHSCOPE_API_KEY', 'HUNYUAN_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Application will use default/placeholder API keys")
    
    return True

def main():
    """主启动函数"""
    try:
        logger.info("🚀 Starting My AI Chatbot...")
        
        # 检查环境
        check_environment()
        
        # 导入并启动应用
        from app import app
        
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('HOST', '0.0.0.0')
        debug = os.getenv('FLASK_ENV') != 'production'
        
        logger.info(f"🌐 Server starting on {host}:{port}")
        logger.info(f"🔧 Debug mode: {debug}")
        
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 