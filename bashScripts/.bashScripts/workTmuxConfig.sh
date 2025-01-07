#!/usr/bin/env bash

# Check if tmux is already running
if ! tmux has-session 2>/dev/null; then
    # If tmux is not running, start a new server
    tmux start-server
fi

# Create work session
if ! tmux has-session -t work 2>/dev/null; then
    tmux new-session -d -s work
    # First window: Run node script
    tmux send-keys -t work:0 'tmux rename-window watcher' C-m
    tmux send-keys -t work:0 'cd ~/repos/cloudinaryFileSync/src/watcher' C-m
    tmux send-keys -t work:0 'node ~/repos/cloudinaryFileSync/src/watcher/watcher.js' C-m
    # Create a second window
    tmux new-window -t work:1
    # Navigate to a specific directory in the second window
    tmux send-keys -t work:1 'tmux rename-window webdev' C-m
    tmux send-keys -t work:1 'cd ~/repos/cloudinaryFileSync/src/cloudinary-sync-files/templates' C-m
fi

# Create project session
if ! tmux has-session -t project 2>/dev/null; then
    tmux new-session -d -s project
    # First window
    tmux send-keys -t project:0 'tmux rename-window code' C-m
    tmux send-keys -t project:0 'cd ~/repos' C-m
    # Second window
    tmux new-window -t project:1
    tmux send-keys -t project:1 'tmux rename-window term' C-m
    tmux send-keys -t project:1 'cd ~/repos' C-m
    # Third window
    tmux new-window -t project:2
    tmux send-keys -t project:2 'tmux rename-window db' C-m
    tmux send-keys -t project:2 'nvim' C-m
    tmux send-keys -t project:2 ':DBUI' C-m
fi

# Display available sessions
echo "Available tmux sessions:"
tmux list-sessions

# Prompt user to choose a session
echo "Enter the name of the session you want to attach to (work/project), or press Enter to not attach:"
read session_name

if [ -n "$session_name" ]; then
    tmux attach-session -t "$session_name"
else
    echo "No session attached. You can manually attach using 'tmux attach-session -t <session_name>'"
fi
