#!/bin/bash

# Package Chrome Extension Script
# This script creates a clean package of the Chrome extension without Python files

echo "🚀 Packaging YouTube AI Chatbot Extension..."

# Create a temporary directory for packaging
TEMP_DIR="extension-package"
ZIP_NAME="youtube-ai-chatbot-extension.zip"

# Remove existing package directory and zip file
rm -rf "$TEMP_DIR"
rm -f "$ZIP_NAME"

# Create package directory
mkdir "$TEMP_DIR"

echo "📁 Copying extension files..."

# Copy only the necessary extension files
cp manifest.json "$TEMP_DIR/"
cp popup.html "$TEMP_DIR/"
cp popup.css "$TEMP_DIR/"
cp popup.js "$TEMP_DIR/"
cp background.js "$TEMP_DIR/"
cp content.js "$TEMP_DIR/"
cp config.js "$TEMP_DIR/"

# Copy icons directory if it exists
if [ -d "icons" ]; then
    cp -r icons "$TEMP_DIR/"
fi

echo "🗜️  Creating ZIP file..."

# Create ZIP file
cd "$TEMP_DIR"
zip -r "../$ZIP_NAME" .
cd ..

# Clean up temporary directory
rm -rf "$TEMP_DIR"

echo "✅ Extension packaged successfully!"
echo "📦 Package created: $ZIP_NAME"
echo ""
echo "🔧 To install in Chrome:"
echo "1. Go to chrome://extensions/"
echo "2. Enable Developer mode"
echo "3. Click 'Load unpacked' and select the extracted folder"
echo "   OR click 'Developer mode' > 'Pack extension' to create a .crx file"
echo ""
echo "⚠️  Note: This package excludes Python files (__pycache__, *.py) which are not needed for the Chrome extension."