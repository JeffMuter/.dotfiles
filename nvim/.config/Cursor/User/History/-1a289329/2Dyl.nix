{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Go development
    go
    gopls
    gotools
    go-tools
    
    # Database tools
    sqlite
    sqlc
    goose
    
    # Development tools
    git
    curl
    jq
    
    # Build tools
    gnumake

    # Web development
    nodejs
    nodePackages.tailwindcss
    air
  ];

  shellHook = ''
    echo "🚀 Welcome to goDial development environment!"
    echo ""
    echo "📋 Available commands:"
    echo "  • Run application:     ./buildAir.sh"
    echo "  • Run tests:          go test ./..."
    echo "  • Database migration: goose -dir db/migrations sqlite3 goDial.db up"
    echo "  • Generate SQL code:   sqlc generate"
    echo "  • Build application:   go build -o bin/goDial cmd/main.go"
    echo ""
    echo "📁 Project structure:"
    echo "  • cmd/           - Application entry point"
    echo "  • internal/      - Internal packages"
    echo "  • db/            - Database schemas and migrations"
    echo "  • static/        - Static web assets"
    echo "  • templates/     - HTML templates"
    echo ""
    echo "🔧 Setup steps (if first time):"
    echo "  1. Initialize database: go run cmd/main.go"
    echo "  2. Run migrations: goose -dir db/migrations sqlite3 goDial.db up"
    echo "  3. Generate SQL code: sqlc generate"
    echo "  4. Initialize Tailwind: npx tailwindcss init"
    echo ""
    echo "Happy coding! 🎉"
    echo ""
  '';

  # Set environment variables
  CGO_ENABLED = "1";
  GOPROXY = "https://proxy.golang.org,direct";
}
