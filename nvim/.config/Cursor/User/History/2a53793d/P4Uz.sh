#!/usr/bin/env bash

# goDial Development Environment Manager

set -e

echo "🚀 goDial Development Environment"
echo "=================================="

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function: Check if we're in nix-shell
check_environment() {
    if [ -z "$IN_NIX_SHELL" ]; then
        echo -e "${YELLOW} Entering nix-shell environment...${NC}"
        exec nix-shell --run "$0 $*"
    fi
    echo -e "${GREEN}✓ Running in nix-shell environment${NC}"
}

# Function: Check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $port is in use${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Port $port is available${NC}"
        return 0
    fi
}

# Function: Kill processes using specific port
kill_port_processes() {
    local port=$1
    echo -e "${BLUE} Checking for processes using port $port...${NC}"
    
    # Find and kill processes using the port
    local pids=$(lsof -ti:$port 2>/dev/null || true)
    if [ -n "$pids" ]; then
        echo -e "${YELLOW} Found processes using port $port: $pids${NC}"
        echo "$pids" | xargs kill -TERM 2>/dev/null || true
        sleep 2
        
        # Force kill if still running
        local remaining_pids=$(lsof -ti:$port 2>/dev/null || true)
        if [ -n "$remaining_pids" ]; then
            echo -e "${RED} Force killing remaining processes: $remaining_pids${NC}"
            echo "$remaining_pids" | xargs kill -9 2>/dev/null || true
            sleep 1
        fi
    fi
}

# Function: Clean up existing processes
cleanup() {
    echo -e "${BLUE} Cleaning up existing processes...${NC}"
    
    # Kill air processes
    pkill -f "air" 2>/dev/null || true
    
    # Kill tailwindcss processes
    pkill -f "tailwindcss" 2>/dev/null || true
    
    # Kill any Go processes that might be our app
    pkill -f "./tmp/main" 2>/dev/null || true
    pkill -f "goDial" 2>/dev/null || true
    
    # Kill processes using port 8080
    kill_port_processes 8080
    
    # Wait for cleanup to complete
    sleep 3
    
    # Verify port is free
    if ! check_port 8080; then
        echo -e "${RED}✗ Port 8080 is still in use after cleanup${NC}"
        echo -e "${YELLOW} You may need to manually kill processes or wait longer${NC}"
        lsof -i :8080 2>/dev/null || true
        exit 1
    fi
    
    echo -e "${GREEN}✓ Cleanup complete${NC}"
}

# Function: Generate templates
generate_templates() {
    echo -e "${BLUE} Generating templates...${NC}"
    if templ generate; then
        echo -e "${GREEN}✓ Templates generated successfully${NC}"
    else
        echo -e "${RED}✗ Template generation failed${NC}"
        exit 1
    fi
}

# Function: Build CSS
build_css() {
    echo -e "${BLUE} Building Tailwind CSS...${NC}"
    if npm run build:css; then
        echo -e "${GREEN}✓ CSS built successfully${NC}"
    else
        echo -e "${RED}✗ CSS build failed${NC}"
        exit 1
    fi
}

# Function: Start development server
start_dev_server() {
    echo -e "${BLUE} Starting development server with Air...${NC}"
    
    # Start air in background
    air &
    AIR_PID=$!
    
    # Give air time to start
    sleep 2
    
    # Start CSS watcher
    echo -e "${BLUE} Starting CSS watcher...${NC}"
    npm run watch:css &
    CSS_PID=$!
    
    echo -e "${GREEN}✓ Development environment ready!${NC}"
    echo -e "${YELLOW}✓ Server running at: http://localhost:8080${NC}"
    echo -e "${YELLOW} Air process ID: $AIR_PID${NC}"
    echo -e "${YELLOW} CSS watcher ID: $CSS_PID${NC}"
    echo ""
    echo -e "${BLUE} Press Ctrl+C to stop all processes${NC}"
    
    # Wait for interrupt
    trap "cleanup; exit 0" INT TERM
    wait
}

# Main execution
main() {
    check_environment
    cleanup
    generate_templates
    build_css
    start_dev_server
}

# Run main function
main "$@" 
