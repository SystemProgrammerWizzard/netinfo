#!/bin/bash
# Exit on error
set -e

echo "🔧 Building NetInfo..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Build the standalone binary
echo "🚀 Building with PyInstaller..."
pyinstaller --onefile --clean --strip --name netinfo \
  --add-data "src/netinfo:netinfo" \
  --hidden-import=psutil \
  --noconfirm \
  src/netinfo/main.py

echo "✅ Build complete! Binary is in the dist/ folder."
echo "📖 Run './dist/netinfo' to test the binary"

echo "Do you want to copy to your bin directory? (y/n)"
read -r copy_bin

if [ "$copy_bin" = "y" ]; then
  echo "🔧 Copying to /usr/local/bin..."
  sudo cp dist/netinfo /usr/local/bin/
  sudo chmod +x /usr/local/bin/netinfo
  echo "✅ Copied to /usr/local/bin/netinfo"
fi

rm -rf build/ dist/ *.spec venv/