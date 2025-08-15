// 页面切换功能
function showPage(pageId) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // 显示目标页面
    document.getElementById(pageId).classList.add('active');
    
    // 更新导航状态
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // 根据pageId找到对应的导航链接并激活
    const pageToNavMap = {
        'home': '首页',
        'chat': 'AI对话', 
        'image': '文生图',
        'video': '视频生成'
    };
    
    document.querySelectorAll('.nav-link').forEach(link => {
        const linkText = link.textContent.trim();
        if (linkText.includes(pageToNavMap[pageId])) {
            link.classList.add('active');
        }
    });
    
    // 关闭移动端菜单
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.remove('active');
    }
    
    // 确保当前页面的下拉列表正常工作
    if (pageId === 'chat') {
        ensureChatModelSelect();
    }
}

// 确保聊天模型选择器正常工作
function ensureChatModelSelect() {
    const chatModelSelect = document.getElementById('chatModel');
    if (chatModelSelect) {
        // 清除可能存在的重复选项
        const options = chatModelSelect.querySelectorAll('option');
        const seenValues = new Set();
        const seenTexts = new Set();
        
        options.forEach(option => {
            if (seenValues.has(option.value) || seenTexts.has(option.textContent)) {
                option.remove();
            } else {
                seenValues.add(option.value);
                seenTexts.add(option.textContent);
            }
        });
        
        // 确保有默认选择
        if (chatModelSelect.value === '') {
            chatModelSelect.value = 'qwen_normal';
        }
    }
}

// 移动端菜单切换
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// AI对话功能 - 支持流式和非流式
async function sendChat() {
    const model = document.getElementById('chatModel').value;
    const input = document.getElementById('chatInput').value.trim();
    
    if (!input) {
        alert('请输入您的问题');
        return;
    }
    
    const loading = document.getElementById('chatLoading');
    const result = document.getElementById('chatResult');
    const response = document.getElementById('chatResponse');
    
    loading.style.display = 'block';
    result.classList.add('hidden');
    
    // 清空之前的响应内容
    response.innerHTML = '';
    
    try {
        // 对深度思考模式使用流式响应
        if (model === 'qwen_thinking') {
            await sendStreamChat(model, input, response, result, loading);
        } else {
            // 非深度思考模式使用普通响应
            await sendNormalChat(model, input, response, result, loading);
        }
    } catch (error) {
        console.error('聊天请求失败:', error);
        alert('发送失败：' + error.message);
        loading.style.display = 'none';
    }
}

// 普通聊天（非流式）
async function sendNormalChat(model, input, responseElement, resultElement, loadingElement) {
    const res = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: model,
            message: input,
            stream: false
        })
    });
    
    if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    const data = await res.json();
    console.log('聊天响应数据:', data);
    
    if (data.status === 'success') {
        responseElement.innerHTML = data.response.replace(/\n/g, '<br>');
        resultElement.classList.remove('hidden');
    } else {
        alert('发送失败：' + (data.error || '未知错误'));
    }
    loadingElement.style.display = 'none';
}

// 流式聊天（用于深度思考模式）
async function sendStreamChat(model, input, responseElement, resultElement, loadingElement) {
    const res = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: model,
            message: input,
            stream: true
        })
    });
    
    if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    // 创建思考过程和回答内容的容器
    const thinkingSection = document.createElement('div');
    thinkingSection.className = 'thinking-section';
    thinkingSection.innerHTML = `
        <div class="thinking-header">
            <h4><i class="fas fa-brain"></i> 思考过程</h4>
            <button class="toggle-thinking" onclick="toggleThinking(this)">
                <i class="fas fa-eye"></i> 显示
            </button>
        </div>
        <div class="thinking-content" style="display: none;"></div>
    `;
    
    const answerSection = document.createElement('div');
    answerSection.className = 'answer-section';
    answerSection.innerHTML = `
        <div class="answer-header">
            <h4><i class="fas fa-comment-dots"></i> 回答内容</h4>
        </div>
        <div class="answer-content"></div>
    `;
    
    responseElement.appendChild(thinkingSection);
    responseElement.appendChild(answerSection);
    
    const thinkingContent = thinkingSection.querySelector('.thinking-content');
    const answerContent = answerSection.querySelector('.answer-content');
    
    resultElement.classList.remove('hidden');
    
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let isAnswering = false;
    
    try {
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
                loadingElement.style.display = 'none';
                break;
            }
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); // 保留最后一个不完整的行
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        console.log('流式数据:', data);
                        
                        if (data.type === 'thinking') {
                            // 思考内容
                            thinkingContent.innerHTML += data.content;
                        } else if (data.type === 'content') {
                            // 回答内容
                            if (!isAnswering) {
                                isAnswering = true;
                                loadingElement.style.display = 'none';
                            }
                            answerContent.innerHTML += data.content;
                        } else if (data.type === 'done') {
                            // 完成
                            loadingElement.style.display = 'none';
                        } else if (data.error) {
                            throw new Error(data.error);
                        }
                    } catch (e) {
                        console.error('解析流式数据失败:', e, line);
                    }
                }
            }
        }
    } catch (error) {
        console.error('流式读取失败:', error);
        throw error;
    }
}

// 切换思考过程显示/隐藏
function toggleThinking(button) {
    const thinkingContent = button.closest('.thinking-section').querySelector('.thinking-content');
    const icon = button.querySelector('i');
    
    if (thinkingContent.style.display === 'none') {
        thinkingContent.style.display = 'block';
        button.innerHTML = '<i class="fas fa-eye-slash"></i> 隐藏';
    } else {
        thinkingContent.style.display = 'none';
        button.innerHTML = '<i class="fas fa-eye"></i> 显示';
    }
}

// 图像生成功能
async function generateImage() {
    const prompt = document.getElementById('imagePrompt').value.trim();
    const size = document.getElementById('imageSize').value;
    
    if (!prompt) {
        alert('请输入图像描述');
        return;
    }
    
    const loading = document.getElementById('imageLoading');
    const result = document.getElementById('imageResult');
    const image = document.getElementById('generatedImage');
    
    loading.style.display = 'block';
    result.classList.add('hidden');
    
    try {
        const res = await fetch('/generate-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                size: size
            })
        });
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        const data = await res.json();
        console.log('图像生成响应数据:', data);
        
        if (data.success) {
            image.src = data.image_url;
            result.classList.remove('hidden');
        } else {
            alert('生成失败：' + data.error);
        }
    } catch (error) {
        console.error('图像生成失败:', error);
        alert('生成失败：' + error.message);
    } finally {
        loading.style.display = 'none';
    }
}

// 视频生成功能
async function generateVideo() {
    const prompt = document.getElementById('videoPrompt').value.trim();
    const quality = document.getElementById('videoQuality').value;
    const size = document.getElementById('videoSize').value;
    const duration = parseInt(document.getElementById('videoDuration').value);
    
    if (!prompt) {
        alert('请输入视频描述');
        return;
    }
    
    const loading = document.getElementById('videoLoading');
    const result = document.getElementById('videoResult');
    const video = document.getElementById('generatedVideo');
    
    loading.style.display = 'block';
    result.classList.add('hidden');
    
    try {
        // 创建视频任务
        const res = await fetch('/create-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                quality: quality,
                size: size,
                duration: duration,
                fps: 30,
                with_audio: false
            })
        });
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        const data = await res.json();
        console.log('视频任务创建响应数据:', data);
        
        if (data.task_id && !data.error) {
            // 轮询检查任务状态
            checkVideoStatus(data.task_id);
        } else {
            throw new Error(data.error || '创建视频任务失败');
        }
    } catch (error) {
        console.error('视频生成失败:', error);
        alert('生成失败：' + error.message);
        loading.style.display = 'none';
    }
}

// 检查视频生成状态
async function checkVideoStatus(taskId) {
    const loading = document.getElementById('videoLoading');
    const result = document.getElementById('videoResult');
    const video = document.getElementById('generatedVideo');
    
    try {
        const res = await fetch(`/video-task-status/${taskId}`);
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        const data = await res.json();
        console.log('视频状态查询响应数据:', data);
        
        if (data.success) {
            if (data.status === 'completed') {
                video.src = data.video_url;
                result.classList.remove('hidden');
                loading.style.display = 'none';
            } else if (data.status === 'failed') {
                throw new Error(data.error || data.message || '视频生成失败');
            } else {
                // 继续轮询
                setTimeout(() => checkVideoStatus(taskId), 5000);
            }
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('视频状态查询失败:', error);
        alert('检查状态失败：' + error.message);
        loading.style.display = 'none';
    }
}

// 响应式处理
function handleResize() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu && window.innerWidth > 768) {
        navMenu.classList.remove('active');
    }
}

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    // 默认显示首页
    showPage('home');
    
    // 确保下拉列表正常工作
    ensureChatModelSelect();
    
    // 添加响应式处理
    window.addEventListener('resize', handleResize);
});

// 导出全局函数供HTML调用
window.showPage = showPage;
window.toggleMobileMenu = toggleMobileMenu;
window.sendChat = sendChat;
window.toggleThinking = toggleThinking;
window.generateImage = generateImage;
window.generateVideo = generateVideo; 