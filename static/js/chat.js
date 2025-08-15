// 新聊天界面的JavaScript功能

// 全局变量
let currentModel = 'qwen_normal';
let conversationHistory = [];
let isTyping = false;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM内容已加载，开始初始化...');
    initModelSelector();
    initMessageInput();
    initSendButton();
    initSettingsPanel();
    console.log('所有初始化函数已调用');
    
    // 自动调整聊天容器高度
    adjustChatHeight();
    window.addEventListener('resize', adjustChatHeight);
});

// 调整聊天容器高度
function adjustChatHeight() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        // 强制重新计算布局
        chatMessages.style.height = 'auto';
        requestAnimationFrame(() => {
            const windowHeight = window.innerHeight;
            const header = document.querySelector('.chat-header');
            const inputArea = document.querySelector('.input-area');
            
            const headerHeight = header ? header.offsetHeight : 0;
            const inputHeight = inputArea ? inputArea.offsetHeight : 0;
            const padding = 32; // 上下padding
            
            const availableHeight = windowHeight - headerHeight - inputHeight - padding;
            chatMessages.style.height = `${Math.max(200, availableHeight)}px`;
        });
    }
}

// 初始化消息输入
function initMessageInput() {
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        // 自动调整高度
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            adjustChatHeight(); // 重新调整聊天区域高度
        });
        
        // 按键处理
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                const sendMode = localStorage.getItem('sendMode') || 'enter';
                
                if (sendMode === 'enter') {
                    // Enter发送模式：Enter发送，Shift+Enter换行
                    if (!e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                    }
                } else {
                    // Ctrl+Enter发送模式：Ctrl+Enter发送，Enter换行
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        sendMessage();
                    }
                }
            }
        });
    }
}

// 初始化发送按钮
function initSendButton() {
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
}

// 发送消息函数
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    if (!messageInput) return;
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // 清空输入框并重置高度
    messageInput.value = '';
    messageInput.style.height = 'auto';
    adjustChatHeight();
    
    // 添加用户消息
    addUserMessage(message);
    
    // 根据选择的模型发送消息
    sendStreamMessage(message, '/chat');
}

// 模型选择器初始化
function initModelSelector() {
    const modelChips = document.querySelectorAll('.model-chip');
    const thinkingModeInfo = document.getElementById('thinkingModeInfo');
    
    modelChips.forEach(chip => {
        chip.addEventListener('click', function() {
            // 移除所有active类
            modelChips.forEach(c => c.classList.remove('active'));
            
            // 添加active到当前选择
            this.classList.add('active');
            currentModel = this.dataset.model;
            
            // 显示或隐藏深度思考模式说明
            if (thinkingModeInfo) {
                if (currentModel === 'qwen_thinking') {
                    thinkingModeInfo.style.display = 'block';
                    // 添加渐入动画
                    thinkingModeInfo.style.opacity = '0';
                    thinkingModeInfo.style.transform = 'translateY(10px)';
                    setTimeout(() => {
                        thinkingModeInfo.style.transition = 'all 0.3s ease';
                        thinkingModeInfo.style.opacity = '1';
                        thinkingModeInfo.style.transform = 'translateY(0)';
                    }, 10);
                } else {
                    thinkingModeInfo.style.display = 'none';
                }
            }
            
            // 添加点击动画
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // 显示模型切换消息
            const modelName = this.querySelector('span').textContent.trim();
            addSystemMessage(`已切换到 ${modelName} 模型`);
        });
    });
}

// 设置下拉菜单初始化
function initSettingsPanel() {
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsMenu = document.getElementById('settingsMenu');
    
    console.log('初始化设置面板 - settingsBtn:', settingsBtn);
    console.log('初始化设置面板 - settingsMenu:', settingsMenu);
    
    if (settingsBtn && settingsMenu) {
        console.log('设置按钮和菜单元素找到，绑定事件监听器...');
        
        // 点击设置按钮切换菜单显示
        settingsBtn.addEventListener('click', function(e) {
            console.log('设置按钮被点击！');
            e.stopPropagation();
            settingsMenu.classList.toggle('hidden');
            console.log('菜单hidden状态:', settingsMenu.classList.contains('hidden'));
        });
        
        // 点击其他地方关闭菜单
        document.addEventListener('click', function(e) {
            if (!settingsMenu.contains(e.target) && !settingsBtn.contains(e.target)) {
                settingsMenu.classList.add('hidden');
            }
        });
        
        // 阻止菜单内部点击事件冒泡
        settingsMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
        
        // 初始化设置项
        initSettingsItems();
    }
}

// 初始化设置项
function initSettingsItems() {
    const fontSizeSelect = document.getElementById('fontSizeSelect');
    const autoScrollCheck = document.getElementById('autoScrollCheck');
    const sendModeSelect = document.getElementById('sendModeSelect');
            
    // 字体大小设置
    if (fontSizeSelect) {
        const savedFontSize = localStorage.getItem('chatFontSize') || 'normal';
        fontSizeSelect.value = savedFontSize;
        applyFontSize(savedFontSize);
        
        fontSizeSelect.addEventListener('change', function() {
            const fontSize = this.value;
            localStorage.setItem('chatFontSize', fontSize);
            applyFontSize(fontSize);
        });
    }
    
    // 自动滚动设置
    if (autoScrollCheck) {
        const savedAutoScroll = localStorage.getItem('autoScroll') !== 'false';
        autoScrollCheck.checked = savedAutoScroll;
        
        autoScrollCheck.addEventListener('change', function() {
            localStorage.setItem('autoScroll', this.checked);
        });
    }
    
    // 发送方式设置
    if (sendModeSelect) {
        const savedSendMode = localStorage.getItem('sendMode') || 'enter';
        sendModeSelect.value = savedSendMode;
        
        sendModeSelect.addEventListener('change', function() {
            localStorage.setItem('sendMode', this.value);
            updateSendModeHint();
        });
        
        updateSendModeHint();
    }
}

// 应用字体大小
function applyFontSize(size) {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.classList.remove('font-small', 'font-normal', 'font-large');
        chatMessages.classList.add(`font-${size}`);
    }
}

// 更新发送方式提示
function updateSendModeHint() {
    const sendMode = localStorage.getItem('sendMode') || 'enter';
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        const placeholder = sendMode === 'enter' ? 
            '输入消息... (Enter发送，Shift+Enter换行)' : 
            '输入消息... (Ctrl+Enter发送)';
        messageInput.placeholder = placeholder;
    }
}

// 关闭设置面板 (保持向后兼容)
function closeSettings() {
    const settingsMenu = document.getElementById('settingsMenu');
    if (settingsMenu) {
        settingsMenu.classList.add('hidden');
    }
}

// 清空聊天
function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    conversationHistory = [];
    
    // 保留欢迎消息
    chatMessages.innerHTML = `
        <div class="message-group">
            <div class="message ai-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p>👋 您好！我是您的AI智能助手，有什么可以帮助您的吗？</p>
                    </div>
                    <div class="message-time">刚刚</div>
                </div>
            </div>
        </div>
    `;
    
    scrollToBottom();
    addSystemMessage('聊天记录已清空');
}

// 添加系统消息
function addSystemMessage(text) {
    const chatMessages = document.getElementById('chatMessages');
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group';
    messageGroup.innerHTML = `
        <div class="system-message" style="text-align: center; margin: 1rem 0;">
            <span style="
                background: rgba(255, 255, 255, 0.1);
                padding: 0.5rem 1rem;
                border-radius: 15px;
                font-size: 0.8rem;
                color: rgba(255, 255, 255, 0.7);
            ">${text}</span>
        </div>
    `;
    
    chatMessages.appendChild(messageGroup);
    scrollToBottom();
}

// 添加用户消息
function addUserMessage(text) {
    const chatMessages = document.getElementById('chatMessages');
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group';
    
    messageGroup.innerHTML = `
        <div class="message user-message">
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <p>${escapeHtml(text)}</p>
                </div>
                <div class="message-time">${getCurrentTime()}</div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageGroup);
    scrollToBottom();
    
    // 添加到历史记录
    conversationHistory.push({
        role: 'user',
        content: text,
        timestamp: new Date().toISOString()
    });
}

// 添加AI消息
function addAIMessage(content, thinking = null) {
    const chatMessages = document.getElementById('chatMessages');
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group';
    
    let thinkingSection = '';
    if (thinking && currentModel === 'qwen_thinking') {
        thinkingSection = `
            <div class="thinking-section" style="margin-bottom: 0.5rem;">
                <button class="thinking-toggle" onclick="toggleThinking(this)" style="
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid var(--glass-border);
                    border-radius: 8px;
                    color: var(--text-color);
                    padding: 0.5rem 1rem;
                    cursor: pointer;
                    font-size: 0.8rem;
                    transition: all 0.3s ease;
                ">
                    <i class="fas fa-brain"></i> 查看思考过程
                </button>
                <div class="thinking-content" style="
                    display: none;
                    margin-top: 0.5rem;
                    padding: 1rem;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 8px;
                    font-size: 0.9rem;
                    line-height: 1.4;
                    color: rgba(255, 255, 255, 0.8);
                    border-left: 3px solid var(--primary-color);
                ">${escapeHtml(thinking)}</div>
            </div>
        `;
    }
    
    messageGroup.innerHTML = `
        <div class="message ai-message">
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                ${thinkingSection}
                <div class="message-bubble">
                    <div class="ai-response">${formatAIResponse(content)}</div>
                </div>
                <div class="message-time">${getCurrentTime()}</div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageGroup);
    scrollToBottom();
    
    // 添加到历史记录
    conversationHistory.push({
        role: 'assistant',
        content: content,
        thinking: thinking,
        timestamp: new Date().toISOString()
    });
}

// 显示输入中状态
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.classList.remove('hidden');
    isTyping = true;
    scrollToBottom();
}

// 隐藏输入中状态
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.classList.add('hidden');
    isTyping = false;
}

// 发送流式消息（深度思考模式）
async function sendStreamMessage(message, endpoint) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: currentModel,
                message: message,
                history: conversationHistory,
                stream: true
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // 创建AI消息容器，用于实时更新
        const chatMessages = document.getElementById('chatMessages');
        const messageGroup = document.createElement('div');
        messageGroup.className = 'message-group';
        
        // 初始化消息结构
        messageGroup.innerHTML = `
            <div class="message ai-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="thinking-section" style="margin-bottom: 0.5rem; display: none;">
                        <div class="thinking-header" style="
                            background: rgba(255, 255, 255, 0.1);
                            border: 1px solid var(--glass-border);
                            border-radius: 8px;
                            color: var(--text-color);
                            padding: 0.5rem 1rem;
                            font-size: 0.8rem;
                            margin-bottom: 0.5rem;
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                        ">
                            <i class="fas fa-brain"></i>
                            <span>思考中...</span>
                            <div class="thinking-dots" style="margin-left: auto;">
                                <span style="animation: blink 1.4s infinite both; animation-delay: 0s;">.</span>
                                <span style="animation: blink 1.4s infinite both; animation-delay: 0.2s;">.</span>
                                <span style="animation: blink 1.4s infinite both; animation-delay: 0.4s;">.</span>
                            </div>
                        </div>
                        <div class="thinking-content" style="
                            padding: 1rem;
                            background: rgba(255, 255, 255, 0.05);
                            border-radius: 8px;
                            font-size: 0.9rem;
                            line-height: 1.4;
                            color: rgba(255, 255, 255, 0.8);
                            border-left: 3px solid var(--primary-color);
                            white-space: pre-wrap;
                            max-height: 300px;
                            overflow-y: auto;
                        "></div>
                    </div>
                    <div class="message-bubble">
                        <div class="ai-response" style="white-space: pre-wrap;"></div>
                        <div class="typing-cursor" style="display: none; margin-top: 0.5rem;">
                            <span style="
                                background: var(--primary-color);
                                width: 2px;
                                height: 1.2em;
                                display: inline-block;
                                animation: blink 1s infinite;
                                vertical-align: middle;
                            "></span>
                        </div>
                    </div>
                    <div class="message-time">${getCurrentTime()}</div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageGroup);
        hideTypingIndicator();
        scrollToBottom();
        
        // 获取实时更新的元素
        const thinkingSection = messageGroup.querySelector('.thinking-section');
        const thinkingHeader = messageGroup.querySelector('.thinking-header span');
        const thinkingContent = messageGroup.querySelector('.thinking-content');
        const aiResponse = messageGroup.querySelector('.ai-response');
        const typingCursor = messageGroup.querySelector('.typing-cursor');
        
        let isThinking = false;
        let isAnswering = false;
        let thinkingText = '';
        let answerText = '';
        
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) break;
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const jsonStr = line.slice(6);
                        if (jsonStr.trim() === '[DONE]') continue;
                        
                        const data = JSON.parse(jsonStr);
                        console.log('[DEBUG] 实时流式数据:', data);
                        
                        // 处理思考内容
                        if (data.type === 'thinking') {
                            if (!isThinking) {
                                isThinking = true;
                                thinkingSection.style.display = 'block';
                                scrollToBottom();
                            }
                            
                            thinkingText += data.content;
                            thinkingContent.textContent = thinkingText;
                            
                            // 自动滚动思考内容到底部
                            thinkingContent.scrollTop = thinkingContent.scrollHeight;
                            scrollToBottom();
                        }
                        // 处理思考阶段结束
                        else if (data.type === 'thinking_end') {
                            if (isThinking) {
                                thinkingHeader.innerHTML = '<i class="fas fa-brain"></i> 思考完成';
                                thinkingHeader.style.opacity = '0.7';
                                console.log('[DEBUG] 思考阶段结束，准备开始回答');
                            }
                        }
                        // 处理回答内容
                        else if (data.type === 'content') {
                            if (!isAnswering) {
                                isAnswering = true;
                                // 如果还没有标记思考完成，现在标记
                                if (isThinking && thinkingHeader.innerHTML.includes('思考中')) {
                                    thinkingHeader.innerHTML = '<i class="fas fa-brain"></i> 思考完成';
                                    thinkingHeader.style.opacity = '0.7';
                                }
                                typingCursor.style.display = 'inline-block';
                                scrollToBottom();
                            }
                            
                            answerText += data.content;
                            aiResponse.innerHTML = formatAIResponse(answerText);
                            scrollToBottom();
                        }
                        // 处理完成信号
                        else if (data.type === 'done') {
                            typingCursor.style.display = 'none';
                            
                            // 如果有思考内容，添加切换按钮
                            if (thinkingText) {
                                const toggleButton = document.createElement('button');
                                toggleButton.className = 'thinking-toggle';
                                toggleButton.innerHTML = '<i class="fas fa-eye-slash"></i> 隐藏思考过程';
                                toggleButton.style.cssText = `
                                    background: rgba(255, 255, 255, 0.1);
                                    border: 1px solid var(--glass-border);
                                    border-radius: 8px;
                                    color: var(--text-color);
                                    padding: 0.5rem 1rem;
                                    cursor: pointer;
                                    font-size: 0.8rem;
                                    transition: all 0.3s ease;
                                    margin-top: 0.5rem;
                                `;
                                
                                toggleButton.onclick = function() {
                                    const content = this.parentElement.querySelector('.thinking-content');
                                    const icon = this.querySelector('i');
                                    
                                    if (content.style.display === 'none') {
                                        content.style.display = 'block';
                                        this.innerHTML = '<i class="fas fa-eye-slash"></i> 隐藏思考过程';
                                    } else {
                                        content.style.display = 'none';
                                        this.innerHTML = '<i class="fas fa-eye"></i> 查看思考过程';
                                    }
                                };
                                
                                thinkingSection.appendChild(toggleButton);
                            }
                            
                            // 添加到历史记录
                            conversationHistory.push({
                                role: 'assistant',
                                content: answerText,
                                thinking: thinkingText || null,
                                timestamp: new Date().toISOString()
                            });
                            
                            console.log('[DEBUG] 流式显示完成 - 思考:', thinkingText.length, '字符, 回答:', answerText.length, '字符');
                            
                            // 如果没有收到任何内容，显示错误信息
                            if (!answerText && !thinkingText) {
                                aiResponse.innerHTML = '<span style="color: rgba(255, 255, 255, 0.6); font-style: italic;">抱歉，没有收到有效回复，请重试。</span>';
                            }
                            break;
                        }
                        // 处理错误
                        else if (data.type === 'error') {
                            typingCursor.style.display = 'none';
                            aiResponse.innerHTML = `<span style="color: #ff6b6b; font-style: italic;">❌ 错误: ${data.error}</span>`;
                            console.error('[ERROR] 服务器错误:', data.error);
                            break;
                        }
                        
                        // 兼容旧格式
                        if (data.choices && data.choices[0] && data.choices[0].delta) {
                            const delta = data.choices[0].delta;
                            
                            if (delta.reasoning_content) {
                                if (!isThinking) {
                                    isThinking = true;
                                    thinkingSection.style.display = 'block';
                                    scrollToBottom();
                                }
                                
                                thinkingText += delta.reasoning_content;
                                thinkingContent.textContent = thinkingText;
                                thinkingContent.scrollTop = thinkingContent.scrollHeight;
                                scrollToBottom();
                            }
                            
                            if (delta.content) {
                                if (!isAnswering) {
                                    isAnswering = true;
                                    if (isThinking) {
                                        thinkingHeader.innerHTML = '<i class="fas fa-brain"></i> 思考完成';
                                        thinkingHeader.style.opacity = '0.7';
                                    }
                                    typingCursor.style.display = 'inline-block';
                                    scrollToBottom();
                                }
                                
                                answerText += delta.content;
                                aiResponse.innerHTML = formatAIResponse(answerText);
                                scrollToBottom();
                            }
                        }
                    } catch (e) {
                        console.error('解析流式数据失败:', e);
                    }
                }
            }
        }
        
    } catch (error) {
        hideTypingIndicator();
        throw error;
    }
}

// 切换思考过程显示
function toggleThinking(button) {
    const thinkingContent = button.parentElement.querySelector('.thinking-content');
    const icon = button.querySelector('i');
    
    if (thinkingContent.style.display === 'none') {
        thinkingContent.style.display = 'block';
        button.innerHTML = '<i class="fas fa-brain"></i> 隐藏思考过程';
    } else {
        thinkingContent.style.display = 'none';
        button.innerHTML = '<i class="fas fa-brain"></i> 查看思考过程';
    }
}

// 工具函数
function getCurrentTime() {
    return new Date().toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatAIResponse(text) {
    // 简单的markdown格式化
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
}

function scrollToBottom() {
    const autoScroll = localStorage.getItem('autoScroll') !== 'false';
    if (!autoScroll) return;
    
    const chatMessages = document.getElementById('chatMessages');
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// 导出全局函数
window.sendMessage = sendMessage;
window.clearChat = clearChat;
window.closeSettings = closeSettings;
window.toggleThinking = toggleThinking; 