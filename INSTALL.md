# Quick Installation Guide

## 📦 Install the Extension

### Step 1: Load the Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked"
4. Select this folder containing the extension files
5. The extension icon should appear in your toolbar

### Step 2: Configure Your API (Optional)
To connect your own AI model:

1. Open `config.js`
2. Set your API endpoint:
   ```javascript
   CONFIG.API.ENDPOINT = 'https://your-api-endpoint.com/chat';
   ```
3. Add authentication if needed:
   ```javascript
   CONFIG.API.HEADERS['Authorization'] = 'Bearer your-api-key';
   ```

### Step 3: Test the Extension
1. Go to any YouTube video (e.g., https://youtube.com/watch?v=dQw4w9WgXcQ)
2. Click the extension icon in your toolbar
3. You should see the chatbot interface
4. Try sending a message!

## 🔧 API Setup

### Expected API Format

**Request (POST):**
```json
{
  "message": "What is this video about?",
  "video": {
    "videoId": "dQw4w9WgXcQ",
    "title": "Video Title",
    "url": "https://youtube.com/watch?v=...",
    "description": "Video description...",
    "channel": "Channel Name"
  },
  "conversationHistory": [...]
}
```

**Response:**
```json
{
  "response": "This video is about...",
  "metadata": {
    "confidence": 0.95
  }
}
```

### No API? No Problem!
The extension works without an API - it will show demo responses to test the interface.

## 🐛 Troubleshooting

- **Extension not loading?** Check for errors in `chrome://extensions/`
- **Not detecting videos?** Refresh the YouTube page
- **Chat not working?** Check the browser console for errors

## 🎉 You're Ready!

The extension is now installed and ready to use. Open any YouTube video and start chatting!