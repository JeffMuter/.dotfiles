# Development Port 8080 Fix

## Problem
When running the `dev` command, Air (the Go hot reload tool) sometimes fails to properly kill the previous Go process before starting a new one. This results in "bind: address already in use" errors on port 8080.

## Root Cause
This is a known issue with Air on Linux systems where:
- Air detects file changes and tries to restart the Go application
- The old process doesn't release port 8080 quickly enough
- The new process fails to bind to port 8080

## Solutions Implemented

### 1. Enhanced Air Configuration (`.air.toml`)
- Increased `delay` to 2000ms (2 seconds) before rebuilding
- Increased `kill_delay` to 5 seconds to wait longer after killing processes
- Added `send_interrupt = true` to send SIGINT before SIGKILL
- Added `rerun = false` to prevent multiple simultaneous builds

### 2. Enhanced Cleanup in Dev Script (`scripts/dev.sh`)
- More aggressive process killing with pattern matching
- Specific port cleanup using `lsof` and `kill`
- Port availability verification before starting
- Graceful termination (SIGTERM) followed by force kill (SIGKILL) if needed
- Longer wait times for cleanup to complete

### 3. Manual Cleanup Script (`scripts/cleanup-port.sh`)
- Standalone script to clean up port 8080 issues
- Can be run manually if the dev script fails
- Available as npm script: `npm run cleanup-port`

## Usage

### Normal Development
```bash
npm run dev
```

### If Port Issues Occur
```bash
# Option 1: Use npm script
npm run cleanup-port

# Option 2: Run script directly
./scripts/cleanup-port.sh

# Option 3: Manual cleanup
lsof -ti:8080 | xargs kill -9
```

### Debugging Port Issues
```bash
# Check what's using port 8080
lsof -i :8080

# Kill specific process by PID
kill -9 <PID>

# Kill all processes using port 8080
lsof -ti:8080 | xargs kill -9
```

## Configuration Details

### Air Configuration Changes
```toml
[build]
delay = 2000          # Wait 2 seconds before rebuilding
kill_delay = "5s"     # Wait 5 seconds after killing process
send_interrupt = true # Send SIGINT before SIGKILL
rerun = false        # Prevent multiple simultaneous builds
```

### Dev Script Enhancements
- Port availability checking
- Multiple process killing strategies
- Verification steps
- Better error handling and reporting

## Troubleshooting

### If the issue persists:
1. Try increasing the delays in `.air.toml`
2. Run the cleanup script manually
3. Check for other applications using port 8080
4. Consider changing the application port temporarily

### Common causes:
- Previous Air processes not fully terminated
- Other applications using port 8080
- OS taking time to release TCP sockets
- Multiple Air instances running simultaneously

## Prevention
- Always use the provided dev script instead of running `air` directly
- Don't run multiple dev environments simultaneously
- Use the cleanup script if you interrupt the dev process unexpectedly 