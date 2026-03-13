document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const systemPromptInput = document.getElementById('system-prompt');
    const sendBtn = chatForm.querySelector('.send-btn');
    const robotWidget = document.getElementById('robot-widget');
    const robotSettingsBtn = document.getElementById('robot-settings-btn');
    const robotSettingsPanel = document.getElementById('robot-settings-panel');
    const robotFaceColorInput = document.getElementById('robot-face-color');
    const robotEyeColorInput = document.getElementById('robot-eye-color');
    const robotStyleSelect = document.getElementById('robot-style-select');
    const robotSizeRange = document.getElementById('robot-size-range');

    const pageRoot = document.documentElement;

    function hexToRgba(hex, alpha = 0.92) {
        const value = hex.replace('#', '');
        const intValue = parseInt(value, 16);
        const r = (intValue >> 16) & 255;
        const g = (intValue >> 8) & 255;
        const b = intValue & 255;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    function darkenHex(hex, factor = 0.7) {
        const value = hex.replace('#', '');
        const intValue = parseInt(value, 16);
        const r = Math.max(0, Math.floor(((intValue >> 16) & 255) * factor));
        const g = Math.max(0, Math.floor(((intValue >> 8) & 255) * factor));
        const b = Math.max(0, Math.floor((intValue & 255) * factor));
        return `rgb(${r}, ${g}, ${b})`;
    }

    function setRobotState(state) {
        if (!robotWidget) return;
        robotWidget.setAttribute('data-state', state);
    }

    function applyRobotFaceColor(hex) {
        pageRoot.style.setProperty('--robot-face-color', hexToRgba(hex, 0.96));
        pageRoot.style.setProperty('--robot-face-color-2', darkenHex(hex, 0.55));
    }

    function applyRobotEyeColor(hex) {
        pageRoot.style.setProperty('--robot-eye-color', hexToRgba(hex, 1));
        pageRoot.style.setProperty('--robot-core-color', hexToRgba(hex, 0.92));
    }

    function applyRobotStyle(styleName) {
        if (!robotWidget) return;
        robotWidget.setAttribute('data-style', styleName || 'neo');
    }

    function applyRobotSize(value) {
        const numericSize = Number(value) / 100;
        pageRoot.style.setProperty('--robot-size', `${numericSize}`);
    }

    let robotResetTimer;

    function setRobotTemporaryState(state, duration = 1200) {
        setRobotState(state);
        clearTimeout(robotResetTimer);
        robotResetTimer = setTimeout(() => setRobotState('idle'), duration);
    }

    function initializeRobotSettings() {
        if (!robotWidget) return;

        applyRobotStyle(robotStyleSelect?.value || 'neo');
        if (robotFaceColorInput) applyRobotFaceColor(robotFaceColorInput.value);
        if (robotEyeColorInput) applyRobotEyeColor(robotEyeColorInput.value);
        if (robotSizeRange) applyRobotSize(robotSizeRange.value);

        if (robotSettingsBtn && robotSettingsPanel) {
            robotSettingsBtn.addEventListener('click', () => {
                const isHidden = robotSettingsPanel.hasAttribute('hidden');
                if (isHidden) {
                    robotSettingsPanel.removeAttribute('hidden');
                } else {
                    robotSettingsPanel.setAttribute('hidden', '');
                }
            });

            document.addEventListener('click', (event) => {
                const clickedInsidePanel = robotSettingsPanel.contains(event.target);
                const clickedOnButton = robotSettingsBtn.contains(event.target);
                if (!clickedInsidePanel && !clickedOnButton) {
                    robotSettingsPanel.setAttribute('hidden', '');
                }
            });
        }

        robotFaceColorInput?.addEventListener('input', (e) => applyRobotFaceColor(e.target.value));
        robotEyeColorInput?.addEventListener('input', (e) => applyRobotEyeColor(e.target.value));
        robotStyleSelect?.addEventListener('change', (e) => applyRobotStyle(e.target.value));
        robotSizeRange?.addEventListener('input', (e) => applyRobotSize(e.target.value));
    }

    function enableRobotDrag() {
        if (!robotWidget) return;

        let dragging = false;
        let startX = 0;
        let startY = 0;
        let originX = 0;
        let originY = 0;

        const setPosition = (x, y) => {
            robotWidget.style.left = `${x}px`;
            robotWidget.style.top = `${y}px`;
            robotWidget.style.right = 'auto';
        };

        const onPointerDown = (e) => {
            dragging = true;
            robotWidget.classList.add('dragging');

            const rect = robotWidget.getBoundingClientRect();
            const containerRect = chatForm.closest('.chat-container').getBoundingClientRect();

            originX = rect.left - containerRect.left;
            originY = rect.top - containerRect.top;

            startX = e.clientX;
            startY = e.clientY;

            if (robotWidget.setPointerCapture) {
                robotWidget.setPointerCapture(e.pointerId);
            }
        };

        const onPointerMove = (e) => {
            if (!dragging) return;

            const containerRect = chatForm.closest('.chat-container').getBoundingClientRect();
            const robotRect = robotWidget.getBoundingClientRect();

            const dx = e.clientX - startX;
            const dy = e.clientY - startY;

            let nextX = originX + dx;
            let nextY = originY + dy;

            const maxX = containerRect.width - robotRect.width;
            const maxY = containerRect.height - robotRect.height;

            nextX = Math.max(0, Math.min(nextX, maxX));
            nextY = Math.max(0, Math.min(nextY, maxY));

            setPosition(nextX, nextY);
        };

        const onPointerUp = (e) => {
            if (!dragging) return;

            dragging = false;
            robotWidget.classList.remove('dragging');

            if (robotWidget.releasePointerCapture) {
                robotWidget.releasePointerCapture(e.pointerId);
            }
        };

        robotWidget.addEventListener('pointerdown', onPointerDown);
        robotWidget.addEventListener('pointermove', onPointerMove);
        robotWidget.addEventListener('pointerup', onPointerUp);
        robotWidget.addEventListener('pointercancel', onPointerUp);
    }

    enableRobotDrag();
    initializeRobotSettings();

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';

        if (this.value.trim() === '') {
            setRobotState('idle');
        } else {
            setRobotState('typing');
        }
        
        // Enable/disable send button
        if(this.value.trim() === '') {
            sendBtn.disabled = true;
        } else {
            sendBtn.disabled = false;
        }
    });

    // Handle Enter key (Shift+Enter for new line, Enter to send)
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if(this.value.trim() !== '') {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });

    // Configure marked.js with Highlight.js
    marked.setOptions({
        highlight: function(code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
        },
        langPrefix: 'hljs language-',
        breaks: true,
        gfm: true
    });

    // Form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        const systemPrompt = systemPromptInput.value.trim();
        
        if (!message) return;

        // Reset input
        userInput.value = '';
        userInput.style.height = 'auto';
        sendBtn.disabled = true;

        // Append User Message
        appendMessage('user', message, false);

        // Show Typing Indicator
        const typingId = appendTypingIndicator();
        setRobotState('thinking');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    system_prompt: systemPrompt
                })
            });

            const data = await response.json();
            
            // Remove Typing Indicator
            removeMessage(typingId);

            if (response.ok && data.choices && data.choices.length > 0) {
                const aiResponse = data.choices[0].message.content;
                appendMessage('ai', aiResponse, true);
                setRobotTemporaryState('happy', 1400);
            } else {
                appendMessage('ai', 'Error: ' + (data.error || 'Failed to generate response.'), false);
                setRobotTemporaryState('error', 1800);
            }

        } catch (error) {
            console.error('Error:', error);
            removeMessage(typingId);
            appendMessage('ai', 'Connection error. Please ensure the backend is running.', false);
            setRobotTemporaryState('error', 1800);
        }
    });

    function appendMessage(sender, text, isMarkdown) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (isMarkdown && sender === 'ai') {
            contentDiv.innerHTML = marked.parse(text);
            // Apply highlighting to any code blocks created
            contentDiv.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        } else {
            contentDiv.textContent = text;
        }
        
        msgDiv.appendChild(contentDiv);
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ai-message`;
        msgDiv.id = id;
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        msgDiv.appendChild(indicator);
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) {
            el.remove();
        }
    }

    function scrollToBottom() {
        chatHistory.scrollTo({
            top: chatHistory.scrollHeight,
            behavior: 'smooth'
        });
    }
});
