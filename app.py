from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import json
import time
from apis.qwen_normal_api import QwenNormalAPI
from apis.qwen_thinking_api import QwenThinkingAPI
from apis.hunyuan_new_api import HunyuanAPI
from apis.wanx_image_api import WanxImageAPI

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 初始化API客户端
api_clients = {
    'qwen_normal': QwenNormalAPI(),
    'qwen_thinking': QwenThinkingAPI(),
    'hunyuan': HunyuanAPI(),
    'wanx': WanxImageAPI()
}

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    return jsonify({
        'qwen_normal': {
            'name': '通义千问(普通模式)',
            'description': '阿里云通义千问大模型 - 快速对话模式',
            'features': ['chat', 'stream']
        },
        'qwen_thinking': {
            'name': '通义千问(深度思考)',
            'description': '阿里云通义千问大模型 - 深度思考模式',
            'features': ['chat', 'deep_thinking', 'reasoning']
        },
        'hunyuan': {
            'name': '腾讯混元', 
            'description': '腾讯混元大模型，支持功能增强',
            'features': ['chat', 'stream', 'enhancement']
        },
        'default': 'qwen_normal'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """处理对话请求"""
    data = request.json
    message = data.get('message', '')
    history = data.get('history', [])
    model = data.get('model', 'qwen_normal')  # 默认使用通义千问普通模式
    stream = data.get('stream', True)  # 是否使用流式响应
    
    if not message:
        return jsonify({'error': '消息不能为空'}), 400
    
    api_client = api_clients.get(model)
    if not api_client:
        return jsonify({'error': f'不支持的模型: {model}'}), 400
    
    # 构建messages格式
    messages = []
    for h in history:
        if h.get('user'):
            messages.append({"role": "user", "content": h['user']})
        if h.get('assistant'):
            messages.append({"role": "assistant", "content": h['assistant']})
    messages.append({"role": "user", "content": message})
    
    # 如果是流式响应
    if stream:
        return Response(
            chat_stream_internal(messages, model),
            mimetype='text/event-stream',
            headers={
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            }
        )
    
    # 非流式响应
    try:
        result = api_client.chat(messages, stream=False)
        
        if "error" in result:
            return jsonify({
                'error': result['error'],
                'status': 'error',
                'model': model
            }), 500
        
        # 处理不同类型的响应
        if "choices" in result:
            response_content = result["choices"][0]["message"]["content"]
            response_data = {
                'response': response_content,
                'status': 'success',
                'model': model,
                'source': api_client.get_model_info()['name']
            }
            
            # 如果是图片生成，添加图片URL
            if "image_url" in result:
                response_data['image_url'] = result['image_url']
            
            return jsonify(response_data)
        else:
            return jsonify({
                'error': '未知的响应格式',
                'status': 'error',
                'model': model
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'处理请求时发生异常: {str(e)}',
            'status': 'error',
            'model': model
        }), 500

def chat_stream_internal(messages, model):
    """内部流式响应处理函数"""
    api_client = api_clients.get(model)
    if not api_client:
        yield f"data: {json.dumps({'error': f'不支持的模型: {model}'}, ensure_ascii=False)}\n\n"
        return
    
    try:
        # 调用对应的API进行流式响应
        for chunk in api_client.chat(messages, stream=True):
            if "error" in chunk:
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                break
            
            # 处理不同的chunk格式
            if "choices" in chunk:
                # 检查是否是思考阶段
                if chunk.get("thinking_phase"):
                    # 思考过程
                    if "reasoning_content" in chunk["choices"][0]["delta"]:
                        thinking_chunk = {
                            "type": "thinking",
                            "content": chunk["choices"][0]["delta"]["reasoning_content"],
                            "model": model
                        }
                        yield f"data: {json.dumps(thinking_chunk, ensure_ascii=False)}\n\n"
                elif chunk.get("answer_start"):
                    # 开始回答阶段
                    start_chunk = {
                        "type": "answer_start",
                        "model": model
                    }
                    yield f"data: {json.dumps(start_chunk, ensure_ascii=False)}\n\n"
                else:
                    # 正常回答内容
                    if "content" in chunk["choices"][0]["delta"]:
                        content_chunk = {
                            "type": "content",
                            "content": chunk["choices"][0]["delta"]["content"],
                            "model": model
                        }
                        yield f"data: {json.dumps(content_chunk, ensure_ascii=False)}\n\n"
            elif "usage" in chunk:
                # 使用情况统计
                usage_chunk = {
                    "type": "usage",
                    "usage": chunk["usage"],
                    "model": model
                }
                yield f"data: {json.dumps(usage_chunk, ensure_ascii=False)}\n\n"
        
        # 发送结束标记
        end_chunk = {
            "type": "done",
            "model": model
        }
        yield f"data: {json.dumps(end_chunk, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        error_chunk = {
            "type": "error",
            "error": f'处理请求时发生异常: {str(e)}',
            "model": model
        }
        yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"

@app.route('/text-to-image', methods=['POST'])
def text_to_image():
    """处理文生图请求 - 创建任务并返回任务ID"""
    data = request.json
    prompt = data.get('prompt', '')
    style = data.get('style', '<auto>')
    size = data.get('size', '1024*1024')
    
    if not prompt:
        return jsonify({'error': '提示词不能为空'}), 400
    
    try:
        wanx_api = api_clients['wanx']
        # 只创建任务，不等待结果
        result = wanx_api.create_image_task(prompt, style, size)
        
        if result['success']:
            return jsonify({
                'task_id': result['task_id'],
                'status': 'pending',
                'prompt': prompt,
                'style': style,
                'size': size,
                'message': '任务创建成功，请使用task_id查询结果'
            })
        else:
            return jsonify({
                'error': result.get('error', '任务创建失败'),
                'status': 'error',
                'details': result.get('details', '')
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'处理文生图请求时发生异常: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/task-status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """查询任务状态"""
    try:
        wanx_api = api_clients['wanx']
        result = wanx_api.query_task_status(task_id)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'查询任务状态时发生异常: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/image-styles', methods=['GET'])
def get_image_styles():
    """获取图片风格选项"""
    try:
        wanx_api = api_clients['wanx']
        styles_info = wanx_api.get_styles_info()
        return jsonify(styles_info)
    except Exception as e:
        return jsonify({
            'error': f'获取风格信息失败: {str(e)}',
            'styles': ['<auto>'],
            'sizes': ['1024*1024'],
            'default_style': '<auto>',
            'default_size': '1024*1024'
        })

if __name__ == '__main__':
    from config import APP_CONFIG
    print("🚀 多模型AI对话应用启动中...")
    print("📝 支持模型:")
    for key, client in api_clients.items():
        model_info = client.get_model_info()
        print(f"   - {model_info['name']} ({key})")
    print("🌐 访问地址: http://localhost:5000")
    
    app.run(
        host=APP_CONFIG['host'],
        port=APP_CONFIG['port'],
        debug=APP_CONFIG['debug']
    ) 