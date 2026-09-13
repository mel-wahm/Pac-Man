#!/usr/bin/env bash
set -e

echo "=== [1/4] Cleaning previous build artifacts ==="
rm -rf build dist pacman-linux pacman-linux.zip Pacman.spec

echo "=== [2/4] Building the game with PyInstaller via uv ==="
uv run pyinstaller \
    --name "Pacman" \
    --onedir \
    pac-man.py

echo "=== [3/4] Copying assets and configuration files ==="
PACKAGE_DIR="dist/Pacman"

cp -r fonts gums photos sounds wallpaper "$PACKAGE_DIR/"

mkdir -p "$PACKAGE_DIR/src/config"
cp src/config/keys.json "$PACKAGE_DIR/src/config/" 2>/dev/null || true

cp config.json "$PACKAGE_DIR/"
cp INSTRUCTIONS.txt "$PACKAGE_DIR/" 2>/dev/null || true

echo "=== [4/4] Creating the final ZIP archive ==="
cd dist
zip -r ../pacman-linux.zip Pacman
cd ..

echo "============================================="
echo "Build completed successfully!"
echo "Package directory: dist/Pacman/"
echo "ZIP archive: pacman-linux.zip"
echo "============================================="
