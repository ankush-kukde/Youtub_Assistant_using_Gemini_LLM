// Popup script for YouTube AI Chatbot
class YouTubeChatbot {
    constructor() {
        this.currentVideo = null;
        this.messages = [];
        this.isLoading = false;
        this.apiEndpoint = ''; // TODO: Set your API endpoint here

        this.initializeElements();
        this.setupEventListeners();
        this.loadCurrentVideo();
        this.loadChatHistory();
    }

    initializeElements() {
        this.chatContainer = document.getElementById('chatContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.clearBtn = document.getElementById('clearChat');
        this.videoInfo = document.getElementById('videoInfo');
        this.videoTitle = document.getElementById('videoTitle');
        this.videoChannel = document.getElementById('videoChannel');
        this.charCount = document.getElementById('charCount');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.apiStatus = document.getElementById('apiStatus');
        this.connectionStatus = document.getElementById('connectionStatus');
    }

    setupEventListeners() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        // Enter key press
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Input change
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.updateSendButton();
        });

        // Clear chat button
        this.clearBtn.addEventListener('click', () => this.clearChat());

        // Listen for video changes
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            if (message.type === 'VIDEO_CHANGED') {
                this.updateVideoInfo(message.videoInfo);
            }
        });
    }

    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = count;
        
        if (count > 450) {
            this.charCount.style.color = '#dc3545';
        } else if (count > 350) {
            this.charCount.style.color = '#ffc107';
        } else {
            this.charCount.style.color = '#6c757d';
        }
    }

    updateSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendBtn.disabled = !hasText || this.isLoading;
    }

    async loadCurrentVideo() {
        try {
            // Get current tab
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            
            if (tab && tab.url && tab.url.includes('youtube.com/watch')) {
                // Send message to content script
                chrome.tabs.sendMessage(tab.id, { type: 'GET_CURRENT_VIDEO' }, (response) => {
                    if (response && response.videoId) {
                        this.updateVideoInfo(response);
                    } else {
                        this.showNoVideoMessage();
                    }
                });
            } else {
                this.showNoVideoMessage();
            }
        } catch (error) {
            console.error('Error loading current video:', error);
            this.showNoVideoMessage();
        }
    }

    updateVideoInfo(videoInfo) {
        if (videoInfo && videoInfo.videoId) {
            this.currentVideo = videoInfo;
            this.videoTitle.textContent = videoInfo.title || 'Unknown Title';
            this.videoChannel.textContent = videoInfo.channel || 'Unknown Channel';
            this.videoInfo.style.display = 'block';
            this.connectionStatus.textContent = 'Connected to video';
            
            // Update placeholder
            this.messageInput.placeholder = `Ask about "${videoInfo.title}"...`;
        } else {
            this.showNoVideoMessage();
        }
    }

    showNoVideoMessage() {
        this.videoInfo.style.display = 'none';
        this.connectionStatus.textContent = 'No YouTube video detected';
        this.messageInput.placeholder = 'Please open a YouTube video first...';
        this.messageInput.disabled = true;
        this.sendBtn.disabled = true;
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.updateCharCount();
        this.updateSendButton();

        // Show loading
        this.setLoading(true);

        try {
            // Get AI response
            const response = await this.getAIResponse(message);
            this.addMessage(response, 'bot');
        } catch (error) {
            console.error('Error getting AI response:', error);
            this.addMessage(
                'Sorry, I encountered an error while processing your request. Please try again.',
                'bot',
                'error'
            );
        } finally {
            this.setLoading(false);
        }

        // Save chat history
        this.saveChatHistory();
    }

    async getAIResponse(userMessage) {
        // If no API endpoint is set, return a mock response
        if (!this.apiEndpoint) {
            return this.getMockResponse(userMessage);
        }

        // Prepare context
        const context = {
            message: userMessage,
            video: this.currentVideo,
            conversationHistory: this.messages.slice(-10) // Last 10 messages for context
        };

        // Make API call
        const response = await fetch(this.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(context)
        });

        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }

        const data = await response.json();
        return data.response || data.message || 'Sorry, I couldn\'t generate a response.';
    }

    getMockResponse(userMessage) {
        const responses = [
            "I'd be happy to help you with that! However, I need to be connected to an AI service to provide detailed responses about this video.",
            "That's an interesting question about this video. Once the API endpoint is configured, I'll be able to analyze the video content and provide detailed answers.",
            "I can see you're asking about the video, but I'm currently running in demo mode. Please configure the API endpoint to get AI-powered responses.",
            "Great question! To provide accurate information about this specific video, I need access to an AI service. The API endpoint is currently not configured.",
            "I understand you want to know more about this video. Once connected to an AI service, I'll be able to discuss the content, context, and answer your questions in detail."
        ];

        // Add some delay to simulate API call
        return new Promise(resolve => {
            setTimeout(() => {
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                resolve(randomResponse);
            }, 1000 + Math.random() * 2000);
        });
    }

    addMessage(text, sender, type = 'normal') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${sender}-message`;

        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${sender === 'user' ? '👤' : '🤖'}</div>
            <div class="message-content">
                <div class="message-text ${type}">${this.escapeHtml(text)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;

        // Remove welcome message if it exists
        const welcomeMessage = this.chatContainer.querySelector('.welcome-message');
        if (welcomeMessage && this.messages.length === 0) {
            welcomeMessage.remove();
        }

        this.chatContainer.appendChild(messageDiv);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;

        // Store message
        this.messages.push({
            text,
            sender,
            timestamp: Date.now(),
            type
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    setLoading(loading) {
        this.isLoading = loading;
        this.loadingOverlay.style.display = loading ? 'flex' : 'none';
        this.updateSendButton();
        
        if (loading) {
            this.messageInput.disabled = true;
        } else {
            this.messageInput.disabled = !this.currentVideo;
        }
    }

    clearChat() {
        // Remove all messages except welcome
        const messages = this.chatContainer.querySelectorAll('.user-message, .bot-message:not(.welcome-message .bot-message)');
        messages.forEach(msg => msg.remove());
        
        // Reset messages array
        this.messages = [];
        
        // Clear storage
        chrome.storage.local.remove('chatHistory');
        
        // Add welcome message back if it doesn't exist
        if (!this.chatContainer.querySelector('.welcome-message')) {
            this.addWelcomeMessage();
        }
    }

    addWelcomeMessage() {
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message';
        welcomeDiv.innerHTML = `
            <div class="bot-message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-text">
                        Hi! I'm your YouTube AI assistant. I can help you with questions about the video you're watching. What would you like to know?
                    </div>
                    <div class="message-time">Now</div>
                </div>
            </div>
        `;
        this.chatContainer.insertBefore(welcomeDiv, this.chatContainer.firstChild);
    }

    saveChatHistory() {
        if (this.currentVideo) {
            const historyKey = `chat_${this.currentVideo.videoId}`;
            chrome.storage.local.set({
                [historyKey]: {
                    messages: this.messages,
                    videoInfo: this.currentVideo,
                    lastUpdated: Date.now()
                }
            });
        }
    }

    async loadChatHistory() {
        if (this.currentVideo) {
            const historyKey = `chat_${this.currentVideo.videoId}`;
            const result = await chrome.storage.local.get(historyKey);
            
            if (result[historyKey] && result[historyKey].messages) {
                const history = result[historyKey];
                
                // Load messages if they're recent (within 24 hours)
                const dayAgo = Date.now() - (24 * 60 * 60 * 1000);
                if (history.lastUpdated > dayAgo) {
                    // Remove welcome message
                    const welcomeMessage = this.chatContainer.querySelector('.welcome-message');
                    if (welcomeMessage) {
                        welcomeMessage.remove();
                    }
                    
                    // Add stored messages
                    history.messages.forEach(msg => {
                        this.addMessage(msg.text, msg.sender, msg.type);
                    });
                }
            }
        }
    }

    // Public method to update API endpoint
    setApiEndpoint(endpoint) {
        this.apiEndpoint = endpoint;
        this.updateApiStatus();
    }

    updateApiStatus() {
        const statusDot = this.apiStatus.querySelector('.status-dot');
        const statusText = this.apiStatus.querySelector('span:last-child');
        
        if (this.apiEndpoint) {
            statusDot.className = 'status-dot';
            statusText.textContent = 'API Connected';
        } else {
            statusDot.className = 'status-dot warning';
            statusText.textContent = 'API Not Configured';
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new YouTubeChatbot();
    
    // You can set the API endpoint here:
    // window.chatbot.setApiEndpoint('https://your-api-endpoint.com/chat');
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = YouTubeChatbot;
}