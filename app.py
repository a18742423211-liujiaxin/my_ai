from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import json
import time
from apis.qwen_normal_api import QwenNormalAPI
from apis.qwen_thinking_api import QwenThinkingAPI
from apis.hunyuan_new_api import HunyuanAPI
from apis.wanx_image_api import WanxImageAPI
from apis.cogvideo_api import CogVideoAPI

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 初始化API客户端
api_clients = {
    'qwen_normal': QwenNormalAPI(),
    'qwen_thinking': QwenThinkingAPI(),
    'hunyuan': HunyuanAPI(),
    'wanx': WanxImageAPI(),
    'cogvideo': CogVideoAPI()
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
                delta = chunk["choices"][0].get("delta", {})
                
                # 检查是否有思考内容
                if "reasoning_content" in delta:
                    thinking_chunk = {
                        "type": "thinking",
                        "content": delta["reasoning_content"],
                        "model": model
                    }
                    yield f"data: {json.dumps(thinking_chunk, ensure_ascii=False)}\n\n"
                
                # 检查是否有回答内容
                if "content" in delta:
                    content_chunk = {
                        "type": "content",
                        "content": delta["content"],
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

@app.route('/create-video', methods=['POST'])
def create_video():
    """创建视频生成任务"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': '请求数据为空',
                'status': 'error'
            }), 400
            
        prompt = data.get('prompt', '').strip()
        image_url = data.get('image_url', '').strip()
        quality = data.get('quality', 'speed')
        size = data.get('size', '1920x1080')
        duration = data.get('duration', 5)
        fps = data.get('fps', 30)
        with_audio = data.get('with_audio', False)
        
        print(f"🎬 接收到视频生成请求:")
        print(f"   - 提示词: {prompt}")
        print(f"   - 图片URL: {image_url}")
        print(f"   - 质量: {quality}")
        print(f"   - 尺寸: {size}")
        print(f"   - 时长: {duration}秒")
        print(f"   - 帧率: {fps}")
        print(f"   - 音频: {with_audio}")
        
        # 参数验证
        if not prompt and not image_url:
            return jsonify({
                'error': '请提供视频描述文本或基础图片',
                'status': 'error'
            }), 400
        
        if prompt and len(prompt) > 1500:
            return jsonify({
                'error': f'视频描述过长（{len(prompt)}字符），最多支持1500字符',
                'status': 'error'
            }), 400
        
        # 验证质量、尺寸等参数
        cogvideo_api = api_clients['cogvideo']
        supported_options = cogvideo_api.get_supported_options()
        
        if quality not in supported_options["qualities"]:
            return jsonify({
                'error': f'不支持的质量模式: {quality}，支持的模式: {supported_options["qualities"]}',
                'status': 'error'
            }), 400
        
        if size not in supported_options["sizes"]:
            return jsonify({
                'error': f'不支持的分辨率: {size}，支持的分辨率: {supported_options["sizes"]}',
                'status': 'error'
            }), 400
        
        if fps not in supported_options["fps_options"]:
            return jsonify({
                'error': f'不支持的帧率: {fps}，支持的帧率: {supported_options["fps_options"]}',
                'status': 'error'
            }), 400
        
        if duration not in supported_options["durations"]:
            return jsonify({
                'error': f'不支持的时长: {duration}，支持的时长: {supported_options["durations"]}',
                'status': 'error'
            }), 400
        
        print(f"📡 调用 GLM CogVideo API...")
        
        result = cogvideo_api.create_video_task(
            prompt=prompt,
            image_url=image_url,
            quality=quality,
            size=size,
            fps=fps,
            duration=duration,
            with_audio=with_audio
        )
        
        print(f"🔄 API 调用结果: {result}")
        
        if result['success']:
            print(f"✅ 任务创建成功: {result['task_id']}")
            
            response_data = {
                'task_id': result['task_id'],
                'status': result.get('status', 'processing'),
                'prompt': prompt,
                'image_url': image_url,
                'quality': quality,
                'size': size,
                'duration': duration,
                'fps': fps,
                'with_audio': with_audio,
                'model': result.get('model', 'cogvideox-3'),
                'request_id': result.get('request_id'),
                'task_status': result.get('task_status', 'PROCESSING'),
                'message': '视频生成任务创建成功，请使用task_id查询结果',
                'estimated_time': f"预计生成时间: {duration * 10}-{duration * 20}秒"  # 估算时间
            }
            
            return jsonify(response_data)
        else:
            error_msg = result.get('error', '视频生成任务创建失败')
            status_code = result.get('status_code', 500)
            error_code = result.get('error_code', 'unknown')
            
            print(f"❌ 任务创建失败: {error_msg}")
            
            return jsonify({
                'error': error_msg,
                'status': 'error',
                'error_code': error_code,
                'status_code': status_code
            }), status_code
            
    except Exception as e:
        error_msg = f'处理视频生成请求时发生异常: {str(e)}'
        print(f"❌ 异常: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': error_msg,
            'status': 'error'
        }), 500

@app.route('/video-task-status/<task_id>', methods=['GET'])
def get_video_task_status(task_id):
    """查询视频生成任务状态"""
    try:
        if not task_id or not task_id.strip():
            return jsonify({
                'error': '任务ID不能为空',
                'status': 'error'
            }), 400
        
        print(f"📊 查询视频任务状态: {task_id}")
        cogvideo_api = api_clients['cogvideo']
        result = cogvideo_api.query_task_status(task_id)
        
        print(f"📋 任务状态查询结果: {result}")
        
        # 添加额外信息
        if result.get('success') and result.get('status') == 'completed':
            # 任务完成，添加一些统计信息
            result['completion_time'] = time.time()
            result['download_ready'] = True
        elif result.get('success') and result.get('status') == 'processing':
            # 处理中，添加进度估算
            result['progress_message'] = '正在生成视频，请耐心等待...'
        
        return jsonify(result)
        
    except Exception as e:
        error_msg = f'查询视频任务状态时发生异常: {str(e)}'
        print(f"❌ 状态查询异常: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': error_msg,
            'status': 'error'
        }), 500

@app.route('/video-options', methods=['GET'])
def get_video_options():
    """获取视频生成选项"""
    try:
        from apis.cogvideo_api import get_available_video_sizes, get_available_qualities
        return jsonify({
            'sizes': get_available_video_sizes(),
            'qualities': get_available_qualities(),
            'fps_options': [30, 60],
            'durations': [5, 10],
            'default_quality': 'speed',
            'default_size': '1920x1080',
            'default_fps': 30,
            'default_duration': 5
        })
    except Exception as e:
        return jsonify({
            'error': f'获取视频选项失败: {str(e)}',
            'sizes': [{'value': '1920x1080', 'label': '1920×1080（全高清横屏）'}],
            'qualities': [{'value': 'speed', 'label': '速度优先'}],
            'fps_options': [30],
            'durations': [5],
            'default_quality': 'speed',
            'default_size': '1920x1080',
            'default_fps': 30,
            'default_duration': 5
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