// 按钮组交互功能
function initializeButtonGroups() {
    // 为所有按钮组添加点击事件
    document.querySelectorAll('.button-group').forEach(group => {
        group.addEventListener('click', handleButtonGroupClick);
    });
}

function handleButtonGroupClick(event) {
    const clickedButton = event.target.closest('.option-btn');
    if (!clickedButton) return;

    const buttonGroup = clickedButton.parentElement;
    const hiddenInput = buttonGroup.parentElement.querySelector('input[type="hidden"]');
    
    // 移除同组其他按钮的active类
    buttonGroup.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 激活点击的按钮
    clickedButton.classList.add('active');
    
    // 更新对应的隐藏输入框值
    if (hiddenInput) {
        const value = clickedButton.dataset.size || 
                     clickedButton.dataset.quality || 
                     clickedButton.dataset.duration;
        hiddenInput.value = value;
    }
    
    // 添加点击反馈动画
    clickedButton.style.transform = 'scale(0.95)';
    setTimeout(() => {
        clickedButton.style.transform = '';
    }, 150);
}

// 页面切换功能
function showPage(pageId) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // 显示目标页面
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }
    
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
    const modelElement = document.getElementById('chatModel');
    const inputElement = document.getElementById('chatInput');
    const loading = document.getElementById('chatLoading');
    const result = document.getElementById('chatResult');
    const response = document.getElementById('chatResponse');
    
    // 安全检查：确保所有必要元素都存在
    if (!modelElement || !inputElement || !loading || !result || !response) {
        console.error('页面元素不完整，无法执行聊天功能');
        return;
    }
    
    const model = modelElement.value;
    const input = inputElement.value.trim();
    
    if (!input) {
        alert('请输入您的问题');
        return;
    }
    
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

// 图像生成功能（改为异步任务模式）
async function generateImage() {
    const promptElement = document.getElementById('imagePrompt');
    const sizeElement = document.getElementById('imageSize');
    const loading = document.getElementById('imageLoading');
    const result = document.getElementById('imageResult');
    const image = document.getElementById('generatedImage');
    const progressContainer = document.getElementById('imageProgressContainer');
    
    // 安全检查：确保所有必要元素都存在
    if (!promptElement || !sizeElement || !loading || !result || !image) {
        console.error('页面元素不完整，无法执行图像生成功能');
        return;
    }
    
    const prompt = promptElement.value.trim();
    const size = sizeElement.value;
    
    if (!prompt) {
        alert('请输入图像描述');
        return;
    }
    
    loading.style.display = 'block';
    result.classList.add('hidden');
    
    // 显示进度条
    if (progressContainer) {
        progressContainer.style.display = 'block';
        updateImageProgress(0, '正在创建任务...', '准备中...');
    }
    
    try {
        // 创建图像任务
        const res = await fetch('/text-to-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                size: size,
                style: '<auto>'
            })
        });
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        const data = await res.json();
        console.log('图像任务创建响应数据:', data);
        
        if (data.task_id && !data.error) {
            updateImageProgress(10, '任务创建成功，开始生成...', '请稍候...');
            // 轮询检查任务状态
            checkImageProgress(data.task_id);
        } else {
            throw new Error(data.error || '创建图像任务失败');
        }
    } catch (error) {
        console.error('图像生成失败:', error);
        alert('生成失败：' + error.message);
        loading.style.display = 'none';
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    }
}

// 检查图像生成进度
async function checkImageProgress(taskId) {
    const loading = document.getElementById('imageLoading');
    const result = document.getElementById('imageResult');
    const image = document.getElementById('generatedImage');
    const progressContainer = document.getElementById('imageProgressContainer');
    
    try {
        const res = await fetch(`/image-task-progress/${taskId}`);
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        const data = await res.json();
        console.log('图像进度查询响应数据:', data);
        
        if (data.success) {
            if (data.status === 'completed') {
                updateImageProgress(100, '图像生成完成！', '已完成');
                if (data.image_url) {
                    image.src = data.image_url;
                    result.classList.remove('hidden');
                }
                loading.style.display = 'none';
                if (progressContainer) {
                    setTimeout(() => {
                        progressContainer.style.display = 'none';
                    }, 2000);
                }
            } else if (data.status === 'failed') {
                throw new Error(data.error || data.message || '图像生成失败');
            } else if (data.status === 'running') {
                // 更新进度
                const progress = data.progress || {};
                updateImageProgress(
                    progress.percentage || 50,
                    progress.message || '图像生成中...',
                    progress.estimated_time || '请稍候...'
                );
                // 继续轮询
                setTimeout(() => checkImageProgress(taskId), 3000);
            } else {
                // 未知状态，继续轮询
                updateImageProgress(30, '处理中...', '请稍候...');
                setTimeout(() => checkImageProgress(taskId), 5000);
            }
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('图像进度查询失败:', error);
        alert('检查进度失败：' + error.message);
        loading.style.display = 'none';
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    }
}

// 更新图像生成进度
function updateImageProgress(percentage, message, timeInfo) {
    const progressFill = document.getElementById('imageProgressFill');
    const progressPercent = document.getElementById('imageProgressPercent');
    const progressMessage = document.getElementById('imageProgressMessage');
    const progressTime = document.getElementById('imageProgressTime');
    
    if (progressFill) {
        progressFill.style.width = `${percentage}%`;
    }
    if (progressPercent) {
        progressPercent.textContent = `${percentage}%`;
    }
    if (progressMessage) {
        progressMessage.textContent = message;
    }
    if (progressTime) {
        progressTime.textContent = timeInfo;
    }
}

// 视频生成功能（增强进度显示）
async function generateVideo() {
    const promptElement = document.getElementById('videoPrompt');
    const qualityElement = document.getElementById('videoQuality');
    const sizeElement = document.getElementById('videoSize');
    const durationElement = document.getElementById('videoDuration');
    const loading = document.getElementById('videoLoading');
    const result = document.getElementById('videoResult');
    const video = document.getElementById('generatedVideo');
    const progressContainer = document.getElementById('videoProgressContainer');
    
    // 安全检查：确保所有必要元素都存在
    if (!promptElement || !qualityElement || !sizeElement || !durationElement || !loading || !result || !video) {
        console.error('页面元素不完整，无法执行视频生成功能');
        return;
    }
    
    const prompt = promptElement.value.trim();
    const quality = qualityElement.value;
    const size = sizeElement.value;
    const duration = parseInt(durationElement.value);
    
    if (!prompt) {
        alert('请输入视频描述');
        return;
    }
    
    loading.style.display = 'block';
    result.classList.add('hidden');
    
    // 显示进度条
    if (progressContainer) {
        progressContainer.style.display = 'block';
        updateVideoProgress(0, '正在创建视频任务...', '准备中...', '预计时间: 计算中...');
    }
    
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
            updateVideoProgress(15, '视频任务创建成功！', '开始生成...', data.estimated_time || '预计时间: 3-8分钟');
            // 轮询检查任务状态
            checkVideoProgressEnhanced(data.task_id);
        } else {
            throw new Error(data.error || '创建视频任务失败');
        }
    } catch (error) {
        console.error('视频生成失败:', error);
        alert('生成失败：' + error.message);
        loading.style.display = 'none';
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    }
}

// 检查视频生成状态（增强版）
async function checkVideoProgressEnhanced(taskId) {
    const loading = document.getElementById('videoLoading');
    const result = document.getElementById('videoResult');
    const video = document.getElementById('generatedVideo');
    const progressContainer = document.getElementById('videoProgressContainer');
    
    // 安全检查：确保所有必要元素都存在
    if (!loading || !result || !video) {
        console.error('页面元素不完整，无法检查视频状态');
        return;
    }
    
    try {
        const res = await fetch(`/video-task-progress/${taskId}`);
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        const data = await res.json();
        console.log('视频进度查询响应数据:', data);
        
        if (data.success) {
            if (data.status === 'completed') {
                updateVideoProgress(100, '视频生成完成！', '完成', '已完成');
                if (data.video_url) {
                    video.src = data.video_url;
                    result.classList.remove('hidden');
                }
                loading.style.display = 'none';
                if (progressContainer) {
                    setTimeout(() => {
                        progressContainer.style.display = 'none';
                    }, 3000);
                }
            } else if (data.status === 'failed') {
                throw new Error(data.error || data.message || '视频生成失败');
            } else if (data.status === 'processing') {
                // 更新详细进度
                const progress = data.progress || {};
                updateVideoProgress(
                    progress.percentage || 60,
                    progress.message || '视频正在生成中...',
                    progress.current_stage || '视频渲染中',
                    progress.estimated_time || '预计还需2-5分钟'
                );
                // 继续轮询，视频生成时间较长，适当延长轮询间隔
                setTimeout(() => checkVideoProgressEnhanced(taskId), 7000);
            } else {
                // 未知状态，继续轮询
                updateVideoProgress(40, '处理中...', '初始化...', '请稍候...');
                setTimeout(() => checkVideoProgressEnhanced(taskId), 8000);
            }
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('视频状态查询失败:', error);
        alert('检查状态失败：' + error.message);
        loading.style.display = 'none';
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    }
}

// 更新视频生成进度
function updateVideoProgress(percentage, message, stage, timeInfo) {
    const progressFill = document.getElementById('videoProgressFill');
    const progressPercent = document.getElementById('videoProgressPercent');
    const progressMessage = document.getElementById('videoProgressMessage');
    const progressStage = document.getElementById('videoProgressStage');
    const progressTime = document.getElementById('videoProgressTime');
    
    if (progressFill) {
        progressFill.style.width = `${percentage}%`;
    }
    if (progressPercent) {
        progressPercent.textContent = `${percentage}%`;
    }
    if (progressMessage) {
        progressMessage.textContent = message;
    }
    if (progressStage) {
        progressStage.textContent = stage;
    }
    if (progressTime) {
        progressTime.textContent = timeInfo;
    }
}

// 检查视频生成状态（保留旧函数以兼容性）
async function checkVideoStatus(taskId) {
    // 直接调用增强版函数
    return checkVideoProgressEnhanced(taskId);
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
    // 只在有页面容器的时候显示首页（避免在聊天页面出错）
    if (document.getElementById('home')) {
        showPage('home');
    }
    
    // 确保下拉列表正常工作
    ensureChatModelSelect();
    
    // 初始化按钮组
    initializeButtonGroups();
    
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