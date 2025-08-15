import requests
import json
import time
from config import WANX_CONFIG

class WanxImageAPI:
    """万象文生图API类 - 兼容原有接口"""
    
    def __init__(self):
        self.config = WANX_CONFIG
        self.api_key = self.config['api_key']
        self.base_url = self.config['api_base']
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "name": "万象文生图",
            "description": "阿里云万象文生图服务 - AI图像生成",
            "type": "image"
        }
    
    def get_styles_info(self):
        """获取图片风格和尺寸选项信息"""
        styles = get_available_styles()
        sizes = get_available_sizes()
        
        return {
            "styles": [style["value"] for style in styles],
            "sizes": [size["value"] for size in sizes],
            "default_style": self.config.get('default_style', '<auto>'),
            "default_size": self.config.get('default_size', '1024*1024'),
            "style_names": {style["value"]: style["label"] for style in styles},
            "size_names": {size["value"]: size["label"] for size in sizes}
        }
    
    def generate_image(self, prompt, style="<auto>", size="1024*1024", n=1):
        """
        生成图片 - 兼容原有接口
        """
        result = generate_image_with_wanx(
            prompt=prompt,
            style=style,
            size=size,
            n=n
        )
        
        if result["success"]:
            # 转换为兼容格式
            image_urls = result.get("image_urls", [])
            if image_urls:
                return {
                    "success": True,
                    "image_url": image_urls[0],  # 第一张图片的URL
                    "data": [{"url": url} for url in image_urls],
                    "usage": result.get("usage", {}),
                    "task_id": result.get("task_id", "")
                }
        
        return result
    
    def chat(self, messages, **kwargs):
        """
        为了兼容统一接口，提供chat方法
        从消息中提取prompt并生成图片
        """
        # 从消息中提取最后一条用户消息作为prompt
        prompt = "生成一张图片"
        style = kwargs.get('style', '<auto>')
        size = kwargs.get('size', '1024*1024')
        
        for msg in reversed(messages):
            if msg.get("role") == "user":
                prompt = msg.get("content", prompt)
                break
        
        # 生成图片
        result = self.generate_image(
            prompt=prompt,
            style=style,
            size=size
        )
        
        # 转换为chat格式的响应
        if result.get("success") and result.get("data"):
            image_url = result["data"][0]["url"]
            return {
                "choices": [{
                    "message": {
                        "content": f"已为您生成图片：\n![生成的图片]({image_url})\n\n提示词：{prompt}",
                        "role": "assistant"
                    },
                    "finish_reason": "stop"
                }],
                "image_url": image_url,
                "usage": result.get("usage", {})
            }
        else:
            error_msg = result.get("error", "图片生成失败")
            return {
                "choices": [{
                    "message": {
                        "content": f"图片生成失败：{error_msg}",
                        "role": "assistant"
                    },
                    "finish_reason": "stop"
                }],
                "error": error_msg
            }

def generate_image_with_wanx(prompt, style="<auto>", size="1024*1024", n=1, negative_prompt=None):
    """
    使用通义万相wanx-v1模型生成图片（官方API v1版本）
    
    Args:
        prompt (str): 正向提示词
        style (str): 图片风格，默认 "<auto>"
        size (str): 图片尺寸，默认 "1024*1024"
        n (int): 生成图片数量，1-4张，默认1
        negative_prompt (str): 反向提示词，可选
    
    Returns:
        dict: 包含成功状态和图片URL或错误信息
    """
    
    api_key = WANX_CONFIG['api_key']
    if not api_key:
        return {
            "success": False,
            "error": "WANX API KEY 未配置"
        }
    
    # 步骤1：创建任务
    create_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable"  # 必须设置为异步模式
    }
    
    # 构建请求数据
    data = {
        "model": "wanx-v1",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "style": style,
            "size": size,
            "n": n
        }
    }
    
    # 添加反向提示词（如果提供）
    if negative_prompt:
        data["input"]["negative_prompt"] = negative_prompt
    
    try:
        # 发送创建任务请求
        print(f"🎨 创建万象文生图任务...")
        print(f"📝 提示词: {prompt}")
        print(f"🎭 风格: {style}")
        print(f"📐 尺寸: {size}")
        
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
        
        if "output" not in result or "task_id" not in result["output"]:
            return {
                "success": False,
                "error": "创建任务响应格式错误，缺少task_id"
            }
        
        task_id = result["output"]["task_id"]
        print(f"📋 任务ID: {task_id}")
        
        # 步骤2：轮询任务结果
        return poll_task_result(task_id)
        
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

def poll_task_result(task_id, max_wait_time=300, poll_interval=5):
    """
    轮询任务结果
    
    Args:
        task_id (str): 任务ID
        max_wait_time (int): 最大等待时间（秒），默认300秒
        poll_interval (int): 轮询间隔（秒），默认5秒
    
    Returns:
        dict: 包含成功状态和图片URL或错误信息
    """
    api_key = WANX_CONFIG['api_key']
    query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    start_time = time.time()
    
    print(f"⏳ 开始轮询任务结果，最大等待时间: {max_wait_time}秒")
    
    while time.time() - start_time < max_wait_time:
        try:
            response = requests.get(query_url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ 查询任务失败: HTTP {response.status_code}")
                return {
                    "success": False,
                    "error": f"查询任务失败: HTTP {response.status_code}"
                }
            
            result = response.json()
            task_status = result.get("output", {}).get("task_status", "UNKNOWN")
            
            print(f"📊 任务状态: {task_status}")
            
            if task_status == "SUCCEEDED":
                # 任务成功完成
                print("✅ 任务执行成功！")
                
                results = result.get("output", {}).get("results", [])
                if not results:
                    return {
                        "success": False,
                        "error": "任务成功但未返回图片"
                    }
                
                # 提取图片URL
                image_urls = []
                for item in results:
                    if "url" in item:
                        image_urls.append(item["url"])
                
                if not image_urls:
                    return {
                        "success": False,
                        "error": "任务成功但图片URL格式错误"
                    }
                
                usage = result.get("usage", {})
                print(f"📈 使用统计: {json.dumps(usage, ensure_ascii=False)}")
                
                return {
                    "success": True,
                    "image_urls": image_urls,
                    "task_id": task_id,
                    "usage": usage
                }
            
            elif task_status == "FAILED":
                # 任务失败
                print("❌ 任务执行失败")
                error_msg = result.get("output", {}).get("message", "任务执行失败")
                return {
                    "success": False,
                    "error": f"任务执行失败: {error_msg}"
                }
            
            elif task_status in ["PENDING", "RUNNING"]:
                # 任务进行中，继续等待
                elapsed = int(time.time() - start_time)
                print(f"⏱️  任务进行中... 已等待 {elapsed} 秒")
                time.sleep(poll_interval)
                continue
            
            else:
                # 未知状态
                return {
                    "success": False,
                    "error": f"任务状态未知: {task_status}"
                }
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 查询请求失败: {str(e)}")
            time.sleep(poll_interval)
            continue
        except json.JSONDecodeError as e:
            print(f"❌ 响应解析失败: {str(e)}")
            time.sleep(poll_interval)
            continue
        except Exception as e:
            print(f"❌ 查询出错: {str(e)}")
            time.sleep(poll_interval)
            continue
    
    # 超时
    elapsed = int(time.time() - start_time)
    return {
        "success": False,
        "error": f"任务执行超时，等待了 {elapsed} 秒"
    }

def get_available_styles():
    """
    获取支持的图片风格列表
    
    Returns:
        list: 风格列表
    """
    return [
        {"value": "<auto>", "label": "自动选择（推荐）"},
        {"value": "<photography>", "label": "摄影"},
        {"value": "<portrait>", "label": "人像写真"},
        {"value": "<3d cartoon>", "label": "3D卡通"},
        {"value": "<anime>", "label": "动画"},
        {"value": "<oil painting>", "label": "油画"},
        {"value": "<watercolor>", "label": "水彩"},
        {"value": "<sketch>", "label": "素描"},
        {"value": "<chinese painting>", "label": "中国画"},
        {"value": "<flat illustration>", "label": "扁平插画"}
    ]

def get_available_sizes():
    """
    获取支持的图片尺寸列表
    
    Returns:
        list: 尺寸列表
    """
    return [
        {"value": "1024*1024", "label": "1024×1024（方形）"},
        {"value": "720*1280", "label": "720×1280（竖屏）"},
        {"value": "768*1152", "label": "768×1152（竖屏）"},
        {"value": "1280*720", "label": "1280×720（横屏）"}
    ]

if __name__ == "__main__":
    # 测试代码
    test_prompt = "一只可爱的橘猫在阳光下打盹，毛茸茸的，非常温馨"
    print("🧪 测试万象文生图API...")
    result = generate_image_with_wanx(
        prompt=test_prompt,
        style="<photography>",
        size="1024*1024",
        n=1
    )
    print(f"🔍 测试结果: {json.dumps(result, ensure_ascii=False, indent=2)}") 