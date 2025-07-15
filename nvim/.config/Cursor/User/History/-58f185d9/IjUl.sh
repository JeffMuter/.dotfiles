#!/usr/bin/env bash

# Air build script for goDial with templ support and CSS rebuilding
set -e

# Set environment variables for development
export GO_ENV="development"
export AIR_ENABLED="1"

# Only run templ generate if .templ files are newer than generated files
NEED_GENERATE=false

# Check if any .templ file is newer than its corresponding _templ.go file
for templ_file in $(find . -name "*.templ" -not -path "./tmp/*" -not -path "./node_modules/*"); do
    generated_file="${templ_file%.*}_templ.go"
    if [[ ! -f "$generated_file" ]] || [[ "$templ_file" -nt "$generated_file" ]]; then
        NEED_GENERATE=true
        break
    fi
done

# Only generate if needed
if [ "$NEED_GENERATE" = true ]; then
    echo "🔧 Generating templates..."
    templ generate
else
    echo "✓ Templates are up to date"
fi

# Check if we need to rebuild CSS
NEED_CSS_BUILD=false

# Check if any template files are newer than the output CSS
if [[ ! -f "./static/css/output.css" ]]; then
    NEED_CSS_BUILD=true
elif [[ "./static/css/input.css" -nt "./static/css/output.css" ]]; then
    NEED_CSS_BUILD=true
else
    # Check if any template files are newer than output.css
    for template_file in $(find ./internal/templates -name "*.templ" 2>/dev/null || true); do
        if [[ "$template_file" -nt "./static/css/output.css" ]]; then
            NEED_CSS_BUILD=true
            break
        fi
    done
    
    # Also check generated template files
    for template_file in $(find . -name "*_templ.go" -not -path "./tmp/*" 2>/dev/null || true); do
        if [[ "$template_file" -nt "./static/css/output.css" ]]; then
            NEED_CSS_BUILD=true
            break
        fi
    done
fi

# Rebuild CSS if needed
if [ "$NEED_CSS_BUILD" = true ]; then
    echo "🎨 Rebuilding Tailwind CSS..."
    npm run build:css
else
    echo "✓ CSS is up to date"
fi

# Build the Go application
echo "🔨 Building Go application..."
GO_ENV="development" AIR_ENABLED="1" go build -o ./tmp/main ./cmd/main.go 