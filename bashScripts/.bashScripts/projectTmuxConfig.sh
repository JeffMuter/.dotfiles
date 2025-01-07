#!/bin/bash

# Check if tmux is already running
if ! tmux has-session 2>/dev/null; then
    # If tmux is not running, start a new server
    tmux start-server
fi

# Create project session
if ! tmux has-session -t project 2>/dev/null; then
    tmux new-session -d -s project
    
    # First window: Run node script
    tmux rename-window -t project:0 'project'
    tmux send-keys -t project:0 'cd repos' C-m
    
    # Create a second window
    tmux new-window -t project:1
    
    # Navigate to a specific directory in the second window
    tmux rename-window -t project:1 'terminal'
    tmux send-keys -t project:1 'cd repos' C-m

    # Create a third window
    tmux new-window -t project:2
    
    # Navigate to a specific directory in the second window
    tmux rename-window -t project:2 'db'
    tmux send-keys -t project:2 'cd repos/' C-m
    tmux send-keys -t project:2 'nvim' C-m
    tmux send-keys -t project:2 ':DBUI' C-m
fi

# Attach to the session
tmux attach-session -t project
