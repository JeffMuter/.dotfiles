#!/bin/bash

# Check if tmux is already running
if ! tmux has-session 2>/dev/null; then
    # If tmux is not running, start a new server
    tmux start-server
fi

# Create blog session
if ! tmux has-session -t blog 2>/dev/null; then
    tmux new-session -d -s blog
    
    # First window: Run node script
    tmux rename-window -t blog:0 'writing'
    tmux send-keys -t blog:0 'cd repos/go/saorsadev-blog/content/posts' C-m
    tmux send-keys -t blog:0 'node watcher.js' C-m
    
    # Create a second window
    tmux new-window -t blog:1
    
    # This creates a new window, and pulls & pushes to github, to keep things in sync before editing
    tmux rename-window -t blog:1 'terminal'
    tmux send-keys -t blog:1 'cd ~/repos/saorsadev-blog' C-m
    tmux send-keys -t blog:1 'git add .' C-m
    tmux send-keys -t blog:1 'git commit -m "tmux startup commit for pull before editing"' C-m
    tmux send-keys -t blog:1 'git pull origin master' C-m
fi

# Attach to the session
tmux attach-session -t blog
