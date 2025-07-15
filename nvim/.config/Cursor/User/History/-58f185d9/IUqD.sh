#!/usr/bin/env bash

# Air build script for goDial with templ support
set -e

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

# Build the Go application
echo "🔨 Building Go application..."
go build -o ./tmp/main ./cmd/main.go 