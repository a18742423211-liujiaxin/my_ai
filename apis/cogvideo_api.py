import requests
import json
import time
import uuid
from config import COGVIDEO_CONFIG

class CogVideoAPI:
    """CogVideoX 视频生成 API 类"""
    
    def __init__(self):
        """初始化 CogVideoX API"""
        from config import COGVIDEO_CONFIG
        self.config = COGVIDEO_CONFIG
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "name": "CogVideoX 视频生成",
            "description": "CogVideoX 视频生成服务 - AI 视频生成",
            "type": "video"
        }
    
    def create_video_task(self, prompt=None, image_url=None, quality="speed", 
                         with_audio=False, size="1920x1080", fps=30, duration=5, 
                         request_id=None, user_id=None):
        """
        创建视频生成任务（异步）
        
        Args:
            prompt (str): 视频的文本描述，最多1500字符
            image_url (str): 基于图像生成视频的图片URL或Base64
            quality (str): 输出模式，"speed" 或 "quality"，默认 "speed"
            with_audio (bool): 是否生成AI音效，默认 False
            size (str): 视频分辨率，默认 "1920x1080"
            fps (int): 视频帧率，30 或 60，默认 30
            duration (int): 视频时长，5 或 10 秒，默认 5
            request_id (str): 客户端请求ID，可选
            user_id (str): 终端用户ID，可选
        
        Returns:
            dict: 包含任务ID和状态信息
        """
        
        api_key = self.config['api_key']
        if not api_key:
            return {
                "success": False,
                "error": "CogVideo API KEY 未配置"
            }
        
        # 验证输入参数
        if not prompt and not image_url:
            return {
                "success": False,
                "error": "prompt 和 image_url 必须至少提供一个"
            }
        
        if prompt and len(prompt) > 1500:
            return {
                "success": False,
                "error": "prompt 长度不能超过1500个字符"
            }
        
        # 生成请求ID（如果未提供）
        if not request_id:
            request_id = str(uuid.uuid4())
        
        create_url = "https://api.minimaxi.chat/paas/v4/videos/generations"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建请求数据
        data = {
            "model": "cogvideox-3",
            "quality": quality,
            "with_audio": with_audio,
            "size": size,
            "fps": fps,
            "duration": duration,
            "request_id": request_id
        }
        
        # 添加文本描述
        if prompt:
            data["prompt"] = prompt
        
        # 添加图像URL
        if image_url:
            data["image_url"] = image_url
        
        # 添加用户ID
        if user_id:
            data["user_id"] = user_id
        
        try:
            print(f"🎬 创建 CogVideoX 视频生成任务...")
            if prompt:
                print(f"📝 文本描述: {prompt}")
            if image_url:
                print(f"🖼️  基础图像: {image_url[:100]}...")
            print(f"⚡ 质量模式: {quality}")
            print(f"📐 分辨率: {size}")
            print(f"🎞️  帧率: {fps} FPS")
            print(f"⏱️  时长: {duration} 秒")
            
            response = requests.post(create_url, headers=headers, json=data, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ 创建任务失败: HTTP {response.status_code}")
                print(f"📄 响应内容: {response.text}")
                return {
                    "success": False,
                    "error": f"创建任务失败: HTTP {response.status_code}, {response.text}"
                }
            
            result = response.json()
            print(f"✅ 任务创建成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 提取任务信息
            task_id = result.get("id")
            task_status = result.get("task_status", "PROCESSING")
            model = result.get("model", "cogvideox-3")
            
            if not task_id:
                return {
                    "success": False,
                    "error": "创建任务响应格式错误，缺少任务ID"
                }
            
            print(f"📋 任务ID: {task_id}")
            print(f"📊 任务状态: {task_status}")
            
            return {
                "success": True,
                "task_id": task_id,
                "status": task_status.lower(),
                "model": model,
                "request_id": result.get("request_id", request_id)
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "请求超时，请稍后重试"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"网络请求失败: {str(e)}"
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "API响应格式错误"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"未知错误: {str(e)}"
            }
    
    def query_task_status(self, task_id):
        """
        查询视频生成任务状态
        
        Args:
            task_id (str): 任务ID
        
        Returns:
            dict: 包含任务状态和结果信息
        """
        api_key = self.config['api_key']
        
        # 使用查询异步结果的公共API
        query_url = f"https://api.minimaxi.chat/query/{task_id}"
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        try:
            response = requests.get(query_url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ 查询任务失败: HTTP {response.status_code}")
                return {
                    "success": False,
                    "error": f"查询任务失败: HTTP {response.status_code}",
                    "status": "error"
                }
            
            result = response.json()
            task_status = result.get("task_status", "UNKNOWN")
            
            print(f"📊 任务状态: {task_status}")
            
            if task_status == "SUCCESS":
                # 任务成功完成
                print("✅ 视频生成成功！")
                
                # 提取视频URL
                video_url = result.get("file_url") or result.get("video_url")
                if not video_url:
                    return {
                        "success": False,
                        "error": "任务成功但未返回视频URL",
                        "status": "error"
                    }
                
                print(f"🎬 视频URL: {video_url}")
                
                return {
                    "success": True,
                    "status": "completed",
                    "video_url": video_url,
                    "task_id": task_id,
                    "model": result.get("model", "cogvideox-3"),
                    "request_id": result.get("request_id"),
                    "duration": result.get("duration"),
                    "size": result.get("size"),
                    "fps": result.get("fps")
                }
            
            elif task_status == "FAIL":
                # 任务失败
                print("❌ 视频生成失败")
                error_msg = result.get("error_message", "视频生成失败")
                return {
                    "success": False,
                    "error": f"视频生成失败: {error_msg}",
                    "status": "failed"
                }
            
            elif task_status == "PROCESSING":
                # 任务进行中
                return {
                    "success": True,
                    "status": "processing",
                    "task_id": task_id,
                    "message": "视频正在生成中，请稍后再查询"
                }
            
            else:
                # 未知状态
                return {
                    "success": False,
                    "error": f"未知任务状态: {task_status}",
                    "status": "unknown"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "查询请求超时",
                "status": "error"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"网络请求失败: {str(e)}",
                "status": "error"
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "API响应格式错误",
                "status": "error"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"未知错误: {str(e)}",
                "status": "error"
            }
    
    def get_supported_options(self):
        """获取支持的配置选项"""
        return {
            "models": ["cogvideox-3"],
            "qualities": ["speed", "quality"],
            "sizes": [
                "1280x720", "720x1280", "1024x1024", 
                "1920x1080", "1080x1920", "2048x1080", "3840x2160"
            ],
            "fps_options": [30, 60],
            "durations": [5, 10],
            "default_quality": "speed",
            "default_size": "1920x1080",
            "default_fps": 30,
            "default_duration": 5
        }
    
    def chat(self, messages, **kwargs):
        """
        为了兼容统一接口，提供chat方法
        从消息中提取prompt并生成视频
        """
        # 从消息中提取最后一条用户消息作为prompt
        prompt = "生成一个视频"
        
        for msg in reversed(messages):
            if msg.get("role") == "user":
                prompt = msg.get("content", prompt)
                break
        
        # 提取其他参数
        quality = kwargs.get('quality', 'speed')
        size = kwargs.get('size', '1920x1080')
        duration = kwargs.get('duration', 5)
        
        # 创建视频生成任务
        result = self.create_video_task(
            prompt=prompt,
            quality=quality,
            size=size,
            duration=duration
        )
        
        # 转换为chat格式的响应
        if result.get("success"):
            task_id = result["task_id"]
            return {
                "choices": [{
                    "message": {
                        "content": f"已为您创建视频生成任务！\n\n📋 任务ID: {task_id}\n📝 描述: {prompt}\n⚡ 质量: {quality}\n📐 分辨率: {size}\n⏱️  时长: {duration}秒\n\n请使用任务ID查询生成结果。",
                        "role": "assistant"
                    },
                    "finish_reason": "stop"
                }],
                "task_id": task_id,
                "status": result.get("status", "processing")
            }
        else:
            error_msg = result.get("error", "视频生成任务创建失败")
            return {
                "choices": [{
                    "message": {
                        "content": f"视频生成任务创建失败：{error_msg}",
                        "role": "assistant"
                    },
                    "finish_reason": "stop"
                }],
                "error": error_msg
            }

def get_available_video_sizes():
    """
    获取支持的视频尺寸列表
    
    Returns:
        list: 尺寸列表
    """
    return [
        {"value": "1920x1080", "label": "1920×1080（全高清横屏）"},
        {"value": "1080x1920", "label": "1080×1920（全高清竖屏）"},
        {"value": "1280x720", "label": "1280×720（高清横屏）"},
        {"value": "720x1280", "label": "720×1280（高清竖屏）"},
        {"value": "1024x1024", "label": "1024×1024（方形）"},
        {"value": "2048x1080", "label": "2048×1080（超宽屏）"},
        {"value": "3840x2160", "label": "3840×2160（4K超高清）"}
    ]

def get_available_qualities():
    """
    获取支持的质量模式列表
    
    Returns:
        list: 质量模式列表
    """
    return [
        {"value": "speed", "label": "速度优先（生成更快，质量稍低）"},
        {"value": "quality", "label": "质量优先（生成质量高，时间较长）"}
    ]

if __name__ == "__main__":
    # 测试代码
    test_prompt = "一只可爱的猫咪在花园里追蝴蝶，阳光明媚，画面温馨"
    print("🧪 测试 CogVideoX 视频生成 API...")
    
    api = CogVideoAPI()
    result = api.create_video_task(
        prompt=test_prompt,
        quality="speed",
        size="1920x1080",
        duration=5
    )
    print(f"🔍 测试结果: {json.dumps(result, ensure_ascii=False, indent=2)}") 