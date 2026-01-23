# AGENTS.md - Guide for AI Agents Working in This Repository

## Repository Overview

This is a **personal dotfiles repository** for a NixOS/Linux system. The repository contains configuration files for various tools and window managers, with a focus on Hyprland (Wayland compositor), terminal emulators, shell configuration, and development environments.

**Platform**: NixOS on Linux  
**Primary Window Manager**: Hyprland (Wayland)  
**Terminal**: Ghostty  
**Shell**: Zsh (configured via NixOS)  
**Editor**: Neovim (Kickstart-based configuration)  
**Terminal Multiplexer**: tmux  
**Application Launcher**: wofi

## Repository Structure

```
.dotfiles/
├── bashScripts/.bashScripts/    # Bash utility scripts (symlinked to ~/.bashScripts)
├── git/.gitconfig               # Git configuration with custom aliases
├── ghostty/config               # Ghostty terminal emulator config
├── hypr/.config/hypr/           # Hyprland window manager configuration
├── i3/.config/i3/               # i3 window manager config (legacy/alternate)
├── ngrok/.config/ngrok/         # ngrok tunneling config
├── nix/.nix-channels            # Nix channels configuration
├── nvim/.config/nvim/           # Neovim configuration (Kickstart-based)
├── tmux/.tmux.conf              # tmux configuration
├── wallpaper/.config/wallpaper/ # Wallpaper management config
├── wallpapers/                  # Wallpaper image collections
│   ├── dark-mode/               # Dark-themed wallpapers
│   └── light-mode/              # Light-themed wallpapers
├── wofi/.config/wofi/           # wofi application launcher styling
└── zsh/.zshrc                   # Zsh config (placeholder - managed by NixOS)
```

## File Organization Pattern

Dotfiles follow a **nested directory structure** that mirrors their home directory locations:

- Files like `git/.gitconfig` are meant to be symlinked to `~/.gitconfig`
- Files like `hypr/.config/hypr/hyprland.conf` are meant to be symlinked to `~/.config/hypr/hyprland.conf`
- The structure preserves the full path from `$HOME`

**Important**: `bashScripts/.bashScripts/` is symlinked to `~/.bashScripts` for script access.

## Git Workflow

### Custom Git Aliases

The repository owner uses a custom git alias called `saorsa` for streamlined commits:

```bash
git saorsa "commit message"
```

This alias performs:
1. Fetch from origin
2. Show ahead/behind status
3. Stage all changes (`git add .`)
4. Commit with the provided message
5. Pull from origin (aborts if conflicts)
6. Push to origin

**Commit Message Pattern**: Recent commits use casual, short messages like "sync: nixos 21:51", "shtuff", "dangit that nvim repo again."

### Other Git Aliases

- `git ssh-check` - Test SSH connection to GitHub
- `git ssh-generate` - Generate new SSH key and display public key
- `git ssh-print` - Display current SSH public key

### Branch

- Default branch: `master`
- Repository is typically kept clean (recent status shows no uncommitted changes)

## Key Commands & Scripts

### Bash Scripts (in `bashScripts/.bashScripts/`)

All scripts are in `~/.bashScripts/` when properly symlinked.

#### `random-wallpaper.sh`
Selects a random wallpaper from `~/wallpapers` and configures hyprpaper:
```bash
~/.bashScripts/random-wallpaper.sh
```
- Searches for `.jpg`, `.jpeg`, `.png` files
- Generates `~/.config/hypr/hyprpaper.conf`
- Launches hyprpaper
- Called automatically on Hyprland startup (see hyprland.conf line 53)

#### `workTmuxConfig.sh`
Creates two tmux sessions for work:
```bash
~/.bashScripts/workTmuxConfig.sh
```
- **work session**: 
  - Window 0 "watcher": Runs node watcher script
  - Window 1 "webdev": For web development
- **project session**:
  - Window 0 "code": General coding
  - Window 1 "term": Terminal work
  - Window 2 "db": Opens nvim with `:DBUI` for database management
- Prompts to attach to a session

#### `projectTmuxConfig.sh`
Creates a single project-focused tmux session:
```bash
~/.bashScripts/projectTmuxConfig.sh
```
- **project session**:
  - Window 0 "project": cd to repos
  - Window 1 "terminal": cd to repos
  - Window 2 "db": Opens nvim with `:DBUI`
- Auto-attaches to session

#### `blogTmuxConfig.sh`
Creates a tmux session for blogging workflow:
```bash
~/.bashScripts/blogTmuxConfig.sh
```
- **blog session**:
  - Window 0 "writing": Runs node watcher for blog posts
  - Window 1 "terminal": Auto-commits and pulls from git to sync before editing
- Auto-attaches to session

### Tmux Configuration

**Prefix**: `Ctrl+Space` (not the default `Ctrl+b`)

**Vi Mode**: Enabled with vi-style copy keybindings:
- `v` - Begin selection
- `Ctrl+v` - Rectangle toggle
- `y` - Copy selection and cancel

**Tmux Resurrect**:
- `Ctrl+Space Ctrl+s` - Save session
- `Ctrl+Space Ctrl+r` - Restore session

**Colors**: Custom color scheme with cyan/purple highlights

## Configuration Details

### Hyprland Window Manager

**Main Config**: `hypr/.config/hypr/hyprland.conf`

**Key Bindings** (mainMod = SUPER/Windows key):
- `SUPER+Q` - Launch terminal (ghostty)
- `SUPER+C` - Kill active window
- `SUPER+M` - Exit Hyprland
- `SUPER+E` - Launch file manager (dolphin)
- `SUPER+R` - Launch application menu (wofi)
- `SUPER+V` - Toggle floating
- `SUPER+J` - Toggle split (dwindle layout)
- `SUPER+S` - Toggle special workspace (scratchpad)
- `SUPER+[1-0]` - Switch to workspace
- `SUPER+SHIFT+[1-0]` - Move window to workspace
- Arrow keys with SUPER - Move focus
- Multimedia keys - Volume, brightness, media controls

**Autostart Commands**:
```bash
exec-once = systemctl --user import-environment DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP
exec-once = dbus-update-activation-environment --systemd DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP
exec-once = /home/emerald/.bashScripts/wallpaper >> /tmp/hyprland-wallpaper.log 2>&1
exec-once = hyprctl setcursor retrosmart-xcursor-white 33
```

**Cursor Theme**: `retrosmart-xcursor-white` size 33

**Layout**: dwindle (default)

**Appearance**:
- Gaps: 5px inner, 20px outer
- Border: 2px
- Rounding: 10px
- Active border: Cyan to green gradient
- Blur enabled with vibrancy
- Custom animations with bezier curves

### Hyprpaper (Wallpaper)

**Config**: `hypr/.config/hypr/hyprpaper.conf`

Currently set wallpaper: `/home/emerald/.dotfiles/wallpapers/dark-mode/pixel-cabin-forest-night.png`

**Wallpaper Collections**:
- `wallpapers/dark-mode/` - Night/dark themed wallpapers (pixel art, forest scenes, cityscapes)
- `wallpapers/light-mode/` - Day/light themed wallpapers (Pokemon, ocean scenes, nature)

**Wallpaper Management Script Config**: `wallpaper/.config/wallpaper/config`
```
MODE=auto
DEFAULT_LIGHT=/home/emerald/.dotfiles/wallpapers/light-mode/pokemon-emerald.jpg
DEFAULT_DARK=/home/emerald/.dotfiles/wallpapers/dark-mode/forest-night-green-moon.jpg
```

### Ghostty Terminal

**Config**: `ghostty/config`

```
font-family = "scientifica"
font-size = 16
background-opacity = 0.85
```

**Font**: scientifica (bitmap font) at 16pt
**Transparency**: 85% opacity

### Wofi (Application Launcher)

**No config file** - Uses default behavior with custom CSS styling

**Style**: `wofi/.config/wofi/style.css`
- **Theme**: Retro/cyberpunk terminal aesthetic
- **Colors**: Black background (#0a0a0a), green text (#33ff33), red accents
- **Font**: Courier New monospace, 13px
- **Effects**: Green glow, sharp borders (no border-radius), shadow effects

### Neovim

**Base**: Kickstart.nvim configuration

**Location**: `nvim/.config/nvim/`

**Structure**:
- `init.lua` - Main configuration entry point
- `lua/kickstart/plugins/` - Plugin configurations (lint, autopairs, neo-tree, gitsigns, etc.)
- `lua/custom/plugins/` - Custom plugin additions
- `lua/polar/` - Custom modules
- `lua/snippets/` - Language-specific snippets (Go)

**Notable Features**:
- LSP configured (owner has tweaked LSP settings in recent commits)
- SQL database UI plugin (`:DBUI` command used in tmux scripts)
- Git integration (gitsigns)
- Neo-tree file explorer
- Auto-pairs and linting

**Note**: The nvim config is based on Kickstart, which emphasizes readable, modular configuration that users can understand line-by-line.

### Zsh Shell

**Config**: `zsh/.zshrc` contains only:
```bash
# ZSH configuration is managed by NixOS zsh.nix
```

**Important**: Shell configuration is managed by NixOS, not in this dotfiles repo. Look for NixOS configuration files (likely in `/etc/nixos/` based on gitconfig safe.directory) for actual Zsh settings.

### NixOS Configuration

**Nix Channels**: `nix/.nix-channels`
```
https://nixos.org/channels/nixos-24.11 nixos-24.11
https://github.com/nix-community/NUR/archive/main.tar.gz nur
```

**NixOS Version**: 24.11  
**Additional Channels**: NUR (Nix User Repository)

**Note**: The actual NixOS system configuration is not in this repository. Based on gitconfig, it's likely in `/etc/nixos/`.

### i3 Window Manager

**Config**: `i3/.config/i3/config`

**Status**: Legacy/alternate window manager (Hyprland is primary based on recent activity)

### Git Configuration

**User**:
- Email: muterjeffery@gmail.com
- Name: JeffMuter

**Safe Directory**: `/etc/nixos` (for system-wide NixOS config)

## Code Style & Patterns

### Bash Scripts
- Use `#!/usr/bin/env bash` shebang
- Check for tmux session existence before creating: `tmux has-session -t name 2>/dev/null`
- Use `-d` flag for detached tmux session creation
- Rename windows with descriptive names
- Use `C-m` to send carriage return in tmux commands

### Configuration File Style
- Preserve default/example comments in autogenerated configs (see hyprland.conf)
- Use descriptive comments for custom modifications
- Group related settings with header comments (e.g., `### MONITORS ###`)

### Directory Structure
- Keep configs in nested directories matching home directory structure
- Use hidden dotfile naming (`.gitconfig`, `.tmux.conf`) at appropriate nesting level
- Separate collections by theme/category (dark-mode/light-mode wallpapers)

## Important Gotchas

### 1. Symlink Structure
The repository uses a **nested directory structure** that must be understood for proper symlinking:
- `git/.gitconfig` symlinks to `~/.gitconfig`
- `hypr/.config/hypr/hyprland.conf` symlinks to `~/.config/hypr/hyprland.conf`

When adding or modifying files, maintain this structure.

### 2. NixOS Management
- Zsh configuration is NOT in this repo - it's managed by NixOS
- System packages and services are likely managed in `/etc/nixos/`
- Don't add shell configuration to `.zshrc` - it will be overwritten by NixOS

### 3. Wallpaper Script Execution
The `random-wallpaper.sh` script:
- Expects wallpapers in `~/wallpapers` (not `~/.dotfiles/wallpapers`)
- Must be symlinked to `~/.bashScripts/` to work with Hyprland autostart
- Generates `~/.config/hypr/hyprpaper.conf` dynamically
- Uses `exec hyprpaper` (replaces itself with hyprpaper process)

### 4. Tmux Prefix
The tmux prefix is **Ctrl+Space**, not the default Ctrl+b. All tmux commands must use this prefix.

### 5. Hyprland vs i3
- Primary WM is **Hyprland** (Wayland)
- i3 config exists but appears to be legacy/alternate
- Focus Hyprland config for any window manager changes

### 6. Git Workflow
- Owner uses `git saorsa` alias for commits - this is a custom workflow
- Commits are casual and descriptive rather than formal
- Branch is `master` (not `main`)

### 7. Duplicate Workspace Bindings
In `hyprland.conf`, there are duplicate keybindings for workspaces 4, 5, and 6 (lines 250-255). This is likely a copy-paste error that should be cleaned up if editing.

### 8. Tmux DBUI Workflow
Multiple tmux scripts launch nvim and immediately send `:DBUI` command. This assumes:
- Neovim has a database UI plugin installed
- The plugin responds to `:DBUI` command
- No other plugins interfere with startup

### 9. Blog Workflow Auto-commit
`blogTmuxConfig.sh` automatically commits and pulls on session creation. This assumes:
- Blog repo is clean or changes are always wanted
- Origin is always available
- Conflicts are rare

## Common Tasks

### Adding a New Config File
1. Create file in appropriate nested directory structure
2. Mirror the home directory path (e.g., `app/.config/app/config`)
3. Update symlinks (likely managed outside this repo via NixOS or GNU Stow)
4. Test the config
5. Commit with casual, descriptive message

### Changing Wallpapers
**Add new wallpaper**:
1. Place image in `wallpapers/dark-mode/` or `wallpapers/light-mode/`
2. Supported formats: `.jpg`, `.jpeg`, `.png`
3. Script will randomly select from collection

**Set specific wallpaper**:
Edit `hypr/.config/hypr/hyprpaper.conf`:
```
preload = /path/to/wallpaper.png
wallpaper = ,/path/to/wallpaper.png
```

**Set default wallpapers**:
Edit `wallpaper/.config/wallpaper/config` to change DEFAULT_LIGHT and DEFAULT_DARK

### Creating a New Tmux Session Script
Follow the pattern in existing scripts:
1. Use `#!/bin/bash` or `#!/usr/bin/env bash`
2. Check if tmux is running: `tmux has-session 2>/dev/null`
3. Start tmux server if needed: `tmux start-server`
4. Check if session exists before creating: `tmux has-session -t name 2>/dev/null`
5. Create detached session: `tmux new-session -d -s name`
6. Rename windows: `tmux rename-window -t session:0 'name'`
7. Send keys: `tmux send-keys -t session:0 'command' C-m`
8. Attach: `tmux attach-session -t name`

### Updating Neovim Configuration
1. Navigate to `nvim/.config/nvim/`
2. Edit `init.lua` for core settings
3. Add plugins in `lua/custom/plugins/` or `lua/kickstart/plugins/`
4. Follow Kickstart.nvim patterns (modular, readable, well-commented)
5. Test thoroughly - owner has made multiple LSP-related commits

### Syncing Dotfiles
Using the owner's workflow:
```bash
git saorsa "descriptive message about changes"
```

Or manually:
```bash
git add .
git commit -m "message"
git pull origin master
git push origin master
```

## Testing & Verification

### After Hyprland Config Changes
1. Reload Hyprland: `SUPER+SHIFT+R` or restart Hyprland
2. Check wallpaper loaded: Look for `/tmp/hyprland-wallpaper.log`
3. Test keybindings
4. Verify cursor theme: `hyprctl setcursor retrosmart-xcursor-white 33`

### After Tmux Config Changes
1. Kill tmux server: `tmux kill-server`
2. Start new session to test config
3. Verify prefix changed to Ctrl+Space
4. Test vi-mode copy bindings

### After Bash Script Changes
1. Test script in isolation: `bash ~/.bashScripts/script.sh`
2. Check for command availability (tmux, hyprpaper, etc.)
3. Verify paths are correct (especially `~/repos` vs absolute paths)
4. Test error cases (missing directories, already-running sessions)

### After Neovim Config Changes
1. Launch nvim and check for errors: `:checkhealth`
2. Test LSP functionality: `:LspInfo`
3. Verify plugins loaded
4. Test DBUI if modified: `:DBUI`

## Project Context

This is a personal configuration repository for a developer who:
- Uses NixOS as primary OS
- Prefers Hyprland (Wayland) over i3
- Works with Go (snippets present)
- Uses databases frequently (DBUI integration)
- Runs node.js file watchers for development
- Maintains a blog (Hugo or similar)
- Prefers retro/cyberpunk aesthetics (green terminals, pixel art wallpapers)
- Values tmux for session management
- Uses Neovim as primary editor
- Has SSH keys for GitHub

## Resources & References

- **Hyprland Wiki**: https://wiki.hyprland.org/
- **Kickstart.nvim**: Neovim config is based on this
- **Tmux Manual**: `man tmux` or https://github.com/tmux/tmux/wiki
- **NixOS Manual**: https://nixos.org/manual/nixos/stable/
- **Wofi**: Wayland-native application launcher (rofi replacement)

## Commit Message Conventions

Based on git history analysis:
- **Casual, descriptive style** - "shtuff", "who knows my brother"
- **Prefixes for sync commits** - "sync: nixos 21:51"
- **Descriptive for changes** - "Add hypr, wofi, wallpaper, ghostty configs"
- **Honest/frustrated** - "dangit that nvim repo again"
- **Task-focused** - "editing of a few things, especially nvim for better lsp stuff"

**Do NOT enforce conventional commits** (feat:, fix:, etc.) - owner uses casual style.

## File Permissions

Standard permissions for dotfiles:
- **Config files**: `644` (rw-r--r--)
- **Bash scripts**: `755` (rwxr-xr-x) - must be executable
- **Directories**: `755` (rwxr-xr-x)

## Dependencies

Based on configs, the following tools are expected:
- **hyprland** - Window manager
- **hyprpaper** - Wallpaper daemon
- **ghostty** - Terminal emulator
- **wofi** - Application launcher
- **tmux** - Terminal multiplexer
- **neovim** - Text editor
- **zsh** - Shell
- **git** - Version control
- **node.js** - For watcher scripts
- **dolphin** - File manager
- **playerctl** - Media control
- **brightnessctl** - Brightness control
- **wpctl** (WirePlumber) - Audio control

These are likely managed by NixOS configuration, not in this repo.

## Notes for Future Agents

1. **Respect the casual style** - This is a personal repo, not a corporate project
2. **NixOS integration** - Many configs are supplemental to NixOS system config
3. **Test before committing** - Owner has made iterative fixes (multiple LSP commits)
4. **Understand symlink structure** - Files aren't in their final locations in this repo
5. **Check tmux prefix** - It's Ctrl+Space, easy to forget
6. **Wallpaper paths** - Scripts reference `~/wallpapers`, not `~/.dotfiles/wallpapers`
7. **Duplicate bindings** - Hyprland config has some duplicate workspace bindings
8. **Path assumptions** - Many scripts assume `~/repos` exists
9. **Auto-commit behavior** - Blog tmux script commits automatically on startup

---

**Last Updated**: Generated automatically by AI agent analysis  
**Repository Owner**: JeffMuter (muterjeffery@gmail.com)
