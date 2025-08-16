# 📥 Install YouTube AI Chatbot Extension

## 🎯 Quick Installation (5 minutes)

### Step 1: Download/Access Extension Files
Make sure you have all these files in your folder:
- ✅ `manifest.json`
- ✅ `content.js`
- ✅ `background.js`
- ✅ `popup.html`
- ✅ `popup.css`
- ✅ `popup.js`
- ✅ `config.js`
- ✅ `icons/` folder

**⚠️ Important:** If you see Python files (`.py`, `__pycache__/`) in the folder, these are NOT needed for the Chrome extension and may cause packaging issues. You can:
- Use the provided `package-extension.sh` script to create a clean package
- Or manually exclude these files when loading the extension

### Step 1.5: Optional - Use Packaging Script
If you have Python files in the directory, run this command to create a clean extension package:
```bash
./package-extension.sh
```
This will create a `youtube-ai-chatbot-extension.zip` with only the necessary extension files.

### Step 2: Open Chrome Extensions
1. **Open Google Chrome**
2. **Copy and paste this in address bar:** `chrome://extensions/`
3. **Press Enter**

### Step 3: Enable Developer Mode
1. **Look for "Developer mode" toggle** (top-right corner)
2. **Click to turn it ON** (should turn blue/enabled)
3. **You'll see new buttons appear:** "Load unpacked", "Pack extension", etc.

### Step 4: Load Your Extension
1. **Click "Load unpacked" button**
2. **Navigate to your extension folder** (the `/workspace` folder with all the files)
3. **Select the folder** and click "Select Folder" or "Open"
4. **Your extension should appear** in the list with the name "YouTube AI Chatbot"

### Step 5: Pin the Extension
1. **Look for the puzzle piece icon** (🧩) in your Chrome toolbar
2. **Click it** to see all extensions
3. **Find "YouTube AI Chatbot"** and click the pin icon to pin it
4. **The extension icon should now appear** directly in your toolbar

## 🧪 Test Your Extension

1. **Go to YouTube:** `https://youtube.com/watch?v=dQw4w9WgXcQ`
2. **Wait for page to load completely**
3. **Click your extension icon** in the toolbar
4. **You should see:** A beautiful chatbot interface with video information
5. **Try typing a message** and sending it

## 🔧 Configure API (Optional)

If you want to connect your AI model:

1. **Open `config.js` file**
2. **Find this line:** `ENDPOINT: '',`
3. **Add your API URL:** `ENDPOINT: 'https://your-api.com/chat',`
4. **Save the file**
5. **Reload the extension:** Go to `chrome://extensions/` → Click reload icon next to your extension

## ✅ Success Indicators

**Extension Loaded Successfully:**
- ✅ Appears in `chrome://extensions/` without errors
- ✅ Icon visible in toolbar (after pinning)
- ✅ No red error messages

**Working on YouTube:**
- ✅ Popup opens when clicking extension icon
- ✅ Shows video title and channel name
- ✅ Chat interface is responsive
- ✅ Can send messages (will show demo responses without API)

## 🚨 Troubleshooting

### Extension Won't Load
- **Check all files are present** in the folder
- **Make sure `manifest.json` is in the root** of the folder
- **Look for error messages** in `chrome://extensions/`

### Can't See Extension Icon
- **Click the puzzle piece** (🧩) in toolbar
- **Pin the extension** by clicking the pin icon
- **Check if extension is enabled** in `chrome://extensions/`

### Not Working on YouTube
- **Refresh the YouTube page** after installing
- **Make sure URL contains `/watch`** (video page)
- **Check browser console** for errors (F12 → Console tab)

### Chat Not Responding
- **This is normal without API** - extension shows demo responses
- **Check `config.js`** if you set up an API endpoint
- **Verify API endpoint** is accessible and returns proper format

## 🎉 You're All Set!

Your YouTube AI Chatbot extension is now installed and ready to use. Open any YouTube video and start chatting!