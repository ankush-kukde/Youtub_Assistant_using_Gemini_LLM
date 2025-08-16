// Background script for YouTube AI Chatbot
class BackgroundService {
    constructor() {
        this.currentVideo = null;
        this.apiEndpoint = ''; // Set your API endpoint here
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Listen for video detection from content script
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
            return true; // Keep the message channel open for async responses
        });

        // Handle extension installation
        chrome.runtime.onInstalled.addListener((details) => {
            this.handleInstallation(details);
        });

        // Handle tab updates (when user navigates)
        chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
            this.handleTabUpdate(tabId, changeInfo, tab);
        });

        // Handle tab activation (when user switches tabs)
        chrome.tabs.onActivated.addListener((activeInfo) => {
            this.handleTabActivation(activeInfo);
        });
    }

    async handleMessage(message, sender, sendResponse) {
        try {
            switch (message.type) {
                case 'VIDEO_DETECTED':
                    await this.handleVideoDetected(message.videoInfo, sender);
                    sendResponse({ success: true });
                    break;

                case 'GET_API_STATUS':
                    sendResponse({
                        apiEndpoint: this.apiEndpoint,
                        isConfigured: !!this.apiEndpoint
                    });
                    break;

                case 'SET_API_ENDPOINT':
                    this.apiEndpoint = message.endpoint;
                    await this.saveApiEndpoint(message.endpoint);
                    sendResponse({ success: true });
                    break;

                case 'CHAT_REQUEST':
                    const response = await this.handleChatRequest(message.data);
                    sendResponse(response);
                    break;

                default:
                    sendResponse({ error: 'Unknown message type' });
            }
        } catch (error) {
            console.error('Background script error:', error);
            sendResponse({ error: error.message });
        }
    }

    async handleVideoDetected(videoInfo, sender) {
        if (!videoInfo || !videoInfo.videoId) return;

        // Update current video
        this.currentVideo = videoInfo;

        // Store video info
        await chrome.storage.local.set({
            currentVideo: videoInfo,
            lastDetected: Date.now()
        });

        // Notify popup if it's open
        try {
            chrome.runtime.sendMessage({
                type: 'VIDEO_CHANGED',
                videoInfo: videoInfo
            });
        } catch (error) {
            // Popup might not be open, that's okay
        }

        // Update badge to show video is detected
        if (sender.tab) {
            chrome.action.setBadgeText({
                text: '●',
                tabId: sender.tab.id
            });
            chrome.action.setBadgeBackgroundColor({
                color: '#667eea',
                tabId: sender.tab.id
            });
        }

        console.log('Video detected:', videoInfo);
    }

    async handleChatRequest(data) {
        try {
            if (!this.apiEndpoint) {
                return {
                    success: false,
                    error: 'API endpoint not configured',
                    response: 'Please configure the API endpoint to get AI responses.'
                };
            }

            // Prepare the request
            const requestData = {
                message: data.message,
                video: this.currentVideo,
                context: data.context || {},
                timestamp: Date.now()
            };

            // Make API request
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'YouTube-AI-Chatbot/1.0'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`API request failed: ${response.status} ${response.statusText}`);
            }

            const result = await response.json();
            
            return {
                success: true,
                response: result.response || result.message || 'No response received from API',
                metadata: result.metadata || {}
            };

        } catch (error) {
            console.error('Chat request error:', error);
            return {
                success: false,
                error: error.message,
                response: 'Sorry, I encountered an error while processing your request.'
            };
        }
    }

    async handleInstallation(details) {
        if (details.reason === 'install') {
            // First time installation
            await chrome.storage.local.set({
                installDate: Date.now(),
                version: chrome.runtime.getManifest().version
            });

            // Open welcome page or instructions
            chrome.tabs.create({
                url: 'https://www.youtube.com',
                active: true
            });

            console.log('YouTube AI Chatbot installed successfully');
        } else if (details.reason === 'update') {
            // Extension updated
            console.log('YouTube AI Chatbot updated to version', chrome.runtime.getManifest().version);
        }
    }

    async handleTabUpdate(tabId, changeInfo, tab) {
        if (changeInfo.status === 'complete' && tab.url) {
            if (tab.url.includes('youtube.com/watch')) {
                // User navigated to a YouTube video page
                // Badge will be updated when content script detects the video
            } else {
                // Clear badge for non-YouTube pages
                chrome.action.setBadgeText({
                    text: '',
                    tabId: tabId
                });
            }
        }
    }

    async handleTabActivation(activeInfo) {
        try {
            const tab = await chrome.tabs.get(activeInfo.tabId);
            if (tab.url && tab.url.includes('youtube.com/watch')) {
                // Switched to a YouTube video tab
                // Request current video info from content script
                chrome.tabs.sendMessage(activeInfo.tabId, { type: 'GET_CURRENT_VIDEO' }, (response) => {
                    if (response && response.videoId) {
                        this.handleVideoDetected(response, { tab });
                    }
                });
            }
        } catch (error) {
            // Tab might not be ready or accessible
        }
    }

    async saveApiEndpoint(endpoint) {
        await chrome.storage.local.set({
            apiEndpoint: endpoint,
            apiConfigured: Date.now()
        });
    }

    async loadApiEndpoint() {
        try {
            const result = await chrome.storage.local.get('apiEndpoint');
            if (result.apiEndpoint) {
                this.apiEndpoint = result.apiEndpoint;
            }
        } catch (error) {
            console.error('Error loading API endpoint:', error);
        }
    }

    // Utility method to get current video info
    async getCurrentVideo() {
        return this.currentVideo;
    }

    // Utility method to set API endpoint
    setApiEndpoint(endpoint) {
        this.apiEndpoint = endpoint;
        this.saveApiEndpoint(endpoint);
    }
}

// Initialize background service
const backgroundService = new BackgroundService();

// Load saved API endpoint on startup
backgroundService.loadApiEndpoint();

// Keep service worker alive
chrome.runtime.onStartup.addListener(() => {
    console.log('YouTube AI Chatbot service worker started');
});

// Handle service worker wake up
self.addEventListener('message', (event) => {
    // Handle any wake-up messages
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BackgroundService;
}