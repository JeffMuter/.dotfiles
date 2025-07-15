#!/bin/bash

# Kill any existing air processes
pkill air || true

# Initialize tailwind if not already done
if [ ! -f "tailwind.config.js" ]; then
    npx tailwindcss init
fi

# Start air in the background
air &

# Watch for changes in templates and static files
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch 