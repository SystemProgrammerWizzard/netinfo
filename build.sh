#!/bin/bash
# This script builds the project using Poetry and PyInstaller.

# Exit on error
set -e

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  echo "🔧 Activating virtual environment..."
  source venv/bin/activate
else
  echo "⚠️  No virtual environment found. You may want to run: python -m venv venv"
fi

# Install dependencies
echo "📦 Installing dependencies with Poetry..."
poetry install

# Build the standalone binary
echo "🚀 Building with PyInstaller..."
poetry run pyinstaller --onefile src/netinfo/main.py --name netinfo

echo "✅ Build complete! Binary is in the dist/ folder."