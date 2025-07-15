#!/bin/bash

echo "🚀 Starting goDial development environment..."

# Check if we're in nix-shell, if not, enter it
if [ -z "$IN_NIX_SHELL" ]; then
    echo "📦 Entering nix-shell environment..."
    exec nix-shell --run "$0"
fi

# Kill any existing air processes
echo "🧹 Cleaning up any existing processes..."
pkill air || true

# Generate templates first
echo "🔧 Generating templates..."
templ generate

# Build Tailwind CSS
echo "🎨 Building Tailwind CSS..."
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

echo "🔥 Starting hot reload with Air..."
# Start air in the background
air &

# Watch for changes in CSS
echo "👀 Watching for CSS changes..."
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch 