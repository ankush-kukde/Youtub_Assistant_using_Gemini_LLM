// Content script for YouTube pages
(function() {
    'use strict';

    let currentVideoId = null;
    let currentVideoTitle = null;
    let currentVideoUrl = null;

    // Function to extract video ID from URL
    function getVideoId(url) {
        const urlParams = new URLSearchParams(new URL(url).search);
        return urlParams.get('v');
    }

    // Function to get video title
    function getVideoTitle() {
        const titleElement = document.querySelector('h1.ytd-watch-metadata yt-formatted-string') || 
                           document.querySelector('h1.title.style-scope.ytd-video-primary-info-renderer') ||
                           document.querySelector('h1 yt-formatted-string[class*="title"]');
        return titleElement ? titleElement.textContent.trim() : 'Unknown Title';
    }

    // Function to get video description
    function getVideoDescription() {
        const descElement = document.querySelector('#description-text') ||
                          document.querySelector('yt-formatted-string#content.ytd-video-secondary-info-renderer');
        return descElement ? descElement.textContent.trim().substring(0, 500) : '';
    }

    // Function to get channel name
    function getChannelName() {
        const channelElement = document.querySelector('#channel-name a') ||
                             document.querySelector('ytd-channel-name a') ||
                             document.querySelector('.ytd-channel-name a');
        return channelElement ? channelElement.textContent.trim() : 'Unknown Channel';
    }

    // Function to update video information
    function updateVideoInfo() {
        const videoId = getVideoId(window.location.href);
        
        if (videoId && videoId !== currentVideoId) {
            currentVideoId = videoId;
            currentVideoUrl = window.location.href;
            
            // Wait a bit for the page to load title
            setTimeout(() => {
                currentVideoTitle = getVideoTitle();
                const description = getVideoDescription();
                const channelName = getChannelName();
                
                const videoInfo = {
                    videoId: currentVideoId,
                    url: currentVideoUrl,
                    title: currentVideoTitle,
                    description: description,
                    channel: channelName,
                    timestamp: Date.now()
                };

                // Send video info to background script
                chrome.runtime.sendMessage({
                    type: 'VIDEO_DETECTED',
                    videoInfo: videoInfo
                });

                console.log('YouTube AI Chatbot: Video detected', videoInfo);
            }, 2000);
        }
    }

    // Listen for URL changes (YouTube is a SPA)
    let lastUrl = location.href;
    new MutationObserver(() => {
        const url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            updateVideoInfo();
        }
    }).observe(document, { subtree: true, childList: true });

    // Initial check
    if (window.location.href.includes('/watch')) {
        updateVideoInfo();
    }

    // Listen for messages from popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        try {
            if (request.type === 'GET_CURRENT_VIDEO') {
                const response = {
                    videoId: currentVideoId,
                    url: currentVideoUrl,
                    title: currentVideoTitle || getVideoTitle(),
                    channel: getChannelName(),
                    description: getVideoDescription()
                };
                sendResponse(response);
                return true; // Keep the message channel open
            }
        } catch (error) {
            console.error('Error in content script message handler:', error);
            sendResponse({
                error: error.message,
                videoId: null
            });
        }
        return true; // Keep the message channel open for async responses
    });

})();