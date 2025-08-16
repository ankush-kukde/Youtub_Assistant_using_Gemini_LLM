// Configuration file for YouTube AI Chatbot Extension
// 
// This file contains the main configuration options for the extension.
// Modify these values to customize the extension behavior.

const CONFIG = {
    // API Configuration
    API: {
        // Set your AI model API endpoint here
        // Example: 'https://api.openai.com/v1/chat/completions'
        // Example: 'https://your-custom-api.com/chat'
        ENDPOINT: '',
        
        // API timeout in milliseconds
        TIMEOUT: 30000,
        
        // Maximum retries for failed requests
        MAX_RETRIES: 3,
        
        // Additional headers to send with API requests
        HEADERS: {
            // 'Authorization': 'Bearer your-api-key',
            // 'Custom-Header': 'value'
        }
    },

    // Chat Configuration
    CHAT: {
        // Maximum message length
        MAX_MESSAGE_LENGTH: 500,
        
        // Maximum messages to keep in conversation history
        MAX_HISTORY_LENGTH: 10,
        
        // Chat history retention time (in milliseconds)
        // 24 hours = 24 * 60 * 60 * 1000
        HISTORY_RETENTION: 24 * 60 * 60 * 1000,
        
        // Auto-scroll to bottom when new message arrives
        AUTO_SCROLL: true
    },

    // Video Detection Configuration
    VIDEO: {
        // Delay before extracting video information (in milliseconds)
        EXTRACTION_DELAY: 2000,
        
        // Maximum length of video description to include
        MAX_DESCRIPTION_LENGTH: 500,
        
        // Selectors for video information (may need updates if YouTube changes)
        SELECTORS: {
            TITLE: [
                'h1.ytd-watch-metadata yt-formatted-string',
                'h1.title.style-scope.ytd-video-primary-info-renderer',
                'h1 yt-formatted-string[class*="title"]'
            ],
            DESCRIPTION: [
                '#description-text',
                'yt-formatted-string#content.ytd-video-secondary-info-renderer'
            ],
            CHANNEL: [
                '#channel-name a',
                'ytd-channel-name a',
                '.ytd-channel-name a'
            ]
        }
    },

    // UI Configuration
    UI: {
        // Extension popup dimensions
        POPUP_WIDTH: 480,
        POPUP_HEIGHT: 600,
        
        // Animation durations (in milliseconds)
        ANIMATION_DURATION: 300,
        
        // Theme colors
        COLORS: {
            PRIMARY: '#667eea',
            SECONDARY: '#764ba2',
            SUCCESS: '#28a745',
            ERROR: '#dc3545',
            WARNING: '#ffc107'
        }
    },

    // Debug Configuration
    DEBUG: {
        // Enable console logging
        ENABLED: true,
        
        // Log levels: 'error', 'warn', 'info', 'debug'
        LEVEL: 'info'
    }
};

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else if (typeof window !== 'undefined') {
    window.CONFIG = CONFIG;
}

// Usage Examples:
//
// 1. Set your API endpoint:
//    CONFIG.API.ENDPOINT = 'https://your-api.com/chat';
//
// 2. Add API authentication:
//    CONFIG.API.HEADERS['Authorization'] = 'Bearer your-token';
//
// 3. Customize chat behavior:
//    CONFIG.CHAT.MAX_MESSAGE_LENGTH = 1000;
//
// 4. Enable debug mode:
//    CONFIG.DEBUG.ENABLED = true;