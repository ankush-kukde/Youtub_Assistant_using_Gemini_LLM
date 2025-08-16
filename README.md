# YouTube AI Chatbot Chrome Extension

A powerful Chrome extension that adds an AI chatbot to your YouTube experience. Chat with an AI assistant about any video you're watching!

## 🚀 Features

- **Smart Video Detection**: Automatically detects when you're watching a YouTube video
- **Beautiful Chat Interface**: Modern, responsive chatbot UI with smooth animations
- **Video Context Awareness**: The AI knows which video you're watching
- **Chat History**: Saves conversation history per video (24-hour retention)
- **Real-time Updates**: Updates when you switch between videos
- **API Ready**: Easy integration with your AI model API
- **Privacy Focused**: All data stays local except for API calls to your configured endpoint

## 📦 Installation

### Method 1: Load as Unpacked Extension (Recommended for Development)

1. **Download/Clone** this repository to your local machine
2. **Open Chrome** and navigate to `chrome://extensions/`
3. **Enable Developer Mode** by clicking the toggle in the top-right corner
4. **Click "Load unpacked"** and select the extension folder
5. **Pin the extension** by clicking the puzzle piece icon and pinning "YouTube AI Chatbot"

### Method 2: Package and Install

1. Navigate to `chrome://extensions/`
2. Enable Developer Mode
3. Click "Pack extension" and select the extension folder
4. Install the generated `.crx` file

## ⚙️ Configuration

### Setting up Your AI API

The extension is designed to work with your own AI model API. To configure it:

1. **Open the extension popup** on any YouTube video page
2. **Locate the API configuration** in the `popup.js` file
3. **Update the API endpoint**:

```javascript
// In popup.js, around line 10:
this.apiEndpoint = 'https://your-api-endpoint.com/chat';

// Or set it dynamically:
window.chatbot.setApiEndpoint('https://your-api-endpoint.com/chat');
```

### API Endpoint Requirements

Your API should accept POST requests with this format:

```json
{
  "message": "User's question about the video",
  "video": {
    "videoId": "dQw4w9WgXcQ",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Video Title",
    "description": "Video description...",
    "channel": "Channel Name",
    "timestamp": 1645123456789
  },
  "conversationHistory": [
    {"text": "Previous message", "sender": "user", "timestamp": 1645123456789},
    {"text": "Previous response", "sender": "bot", "timestamp": 1645123456790}
  ]
}
```

And return responses in this format:

```json
{
  "response": "AI's response to the user",
  "metadata": {
    "confidence": 0.95,
    "processing_time": 1.2
  }
}
```

## 🎯 Usage

1. **Open a YouTube video** in any tab
2. **Click the extension icon** to open the chatbot
3. **Start chatting!** Ask questions about the video content
4. **Switch videos** and the chatbot will automatically update context

### Example Conversations

- "What is this video about?"
- "Can you summarize the main points?"
- "What did they say about [specific topic]?"
- "Explain this concept in simpler terms"
- "What are the key takeaways?"

## 🛠️ Development

### Project Structure

```
youtube-ai-chatbot/
├── manifest.json          # Extension configuration
├── content.js            # YouTube page content script
├── background.js         # Service worker for API handling
├── popup.html           # Chat interface HTML
├── popup.css            # Modern UI styling
├── popup.js             # Chat functionality
├── icons/               # Extension icons
└── README.md           # This file
```

### Key Components

- **Content Script**: Detects YouTube videos and extracts metadata
- **Background Script**: Handles API communication and state management
- **Popup Interface**: Modern chat UI with animations and responsive design
- **Storage System**: Saves chat history and video context locally

### Customization

#### Changing the UI Theme

Edit `popup.css` to customize colors, fonts, and animations:

```css
/* Update the main gradient */
.header {
    background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}
```

#### Adding New Features

The extension is built with modularity in mind. Key extension points:

- **Message Processing**: Add custom handlers in `popup.js`
- **Video Detection**: Enhance selectors in `content.js`
- **API Integration**: Modify request/response handling in `background.js`

## 🔒 Privacy & Security

- **Local Storage**: Chat history is stored locally in Chrome's storage
- **No Tracking**: The extension doesn't track or collect personal data
- **API Communication**: Only configured API endpoint receives data
- **Permissions**: Minimal permissions for YouTube pages only

## 🐛 Troubleshooting

### Extension Not Detecting Videos

1. **Refresh the YouTube page** after installing
2. **Check if the video URL contains `/watch`**
3. **Look for console errors** in Developer Tools

### Chat Not Working

1. **Verify API endpoint** is configured correctly
2. **Check network tab** for failed API requests
3. **Ensure CORS is enabled** on your API server

### UI Issues

1. **Try refreshing** the extension popup
2. **Check browser console** for JavaScript errors
3. **Verify all files** are loaded correctly

## 🔧 Advanced Configuration

### Custom API Headers

Modify the API request in `background.js`:

```javascript
const response = await fetch(this.apiEndpoint, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your-api-key',
        'Custom-Header': 'value'
    },
    body: JSON.stringify(requestData)
});
```

### Video Data Enhancement

Add more video metadata in `content.js`:

```javascript
// Get video duration, view count, etc.
function getVideoMetadata() {
    return {
        duration: document.querySelector('.ytp-time-duration')?.textContent,
        views: document.querySelector('#info-text')?.textContent,
        likes: document.querySelector('like-button')?.textContent
    };
}
```

## 📈 Performance

- **Lightweight**: Minimal resource usage
- **Efficient**: Smart caching and debounced API calls
- **Responsive**: Optimized for smooth animations
- **Scalable**: Designed to handle multiple video sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## 🆘 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the browser console for errors
3. Ensure your API endpoint is properly configured
4. Test with a simple API endpoint first

---

**Made with ❤️ for the YouTube and AI community**
