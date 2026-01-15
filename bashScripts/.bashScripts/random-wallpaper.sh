#!/usr/bin/env bash
# Random wallpaper selector for Hyprland + hyprpaper

WALLPAPER_DIR="$HOME/wallpapers"
HYPRPAPER_CONF="$HOME/.config/hypr/hyprpaper.conf"

# Find a random image from the wallpapers directory
RANDOM_WALLPAPER=$(find "$WALLPAPER_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | shuf -n 1)

# Check if we found a wallpaper
if [ -z "$RANDOM_WALLPAPER" ]; then
    echo "Error: No wallpapers found in $WALLPAPER_DIR"
    exit 1
fi

echo "Selected wallpaper: $RANDOM_WALLPAPER"

# Generate hyprpaper.conf with the random wallpaper
cat > "$HYPRPAPER_CONF" << EOF
preload = $RANDOM_WALLPAPER
wallpaper = ,$RANDOM_WALLPAPER
EOF

# Launch hyprpaper
exec hyprpaper
