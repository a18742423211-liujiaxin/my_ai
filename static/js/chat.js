// 专门的聊天功能JavaScript文件

// 修复后端流式API的数据格式处理
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
                        const jsonStr = line.slice(6);
                        if (jsonStr.trim() === '[DONE]') {
                            loadingElement.style.display = 'none';
                            continue;
                        }
                        
                        const data = JSON.parse(jsonStr);
                        console.log('流式数据:', data);
                        
                        // 处理来自后端的数据格式
                        if (data.choices && data.choices[0] && data.choices[0].delta) {
                            const delta = data.choices[0].delta;
                            
                            // 思考内容
                            if (delta.reasoning) {
                                thinkingContent.innerHTML += delta.reasoning;
                            }
                            
                            // 回答内容
                            if (delta.content) {
                                if (!isAnswering) {
                                    isAnswering = true;
                                    loadingElement.style.display = 'none';
                                }
                                answerContent.innerHTML += delta.content;
                            }
                        } else if (data.phase_change === 'answer_start') {
                            // 从思考阶段转换到回答阶段
                            isAnswering = true;
                        } else if (data.summary) {
                            // 完成时的汇总信息
                            console.log('完成汇总:', data.summary);
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

// 键盘事件处理
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChat();
            }
        });
    }
});

// 导出给全局使用
if (typeof window !== 'undefined') {
    window.sendStreamChat = sendStreamChat;
} 