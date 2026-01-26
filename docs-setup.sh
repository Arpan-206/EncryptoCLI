#!/bin/bash
# Setup and manage documentation for EncryptoCLI using uv

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
show_help() {
    echo "EncryptoCLI Documentation Management"
    echo ""
    echo "Usage: ./docs-setup.sh [command]"
    echo ""
    echo "Commands:"
    echo "  install    Install documentation dependencies with uv"
    echo "  serve      Start local documentation server"
    echo "  build      Build static documentation site"
    echo "  deploy     Deploy documentation to GitHub Pages"
    echo "  clean      Clean build artifacts"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./docs-setup.sh install"
    echo "  ./docs-setup.sh serve"
    echo "  ./docs-setup.sh build"
}

install_deps() {
    echo -e "${BLUE}Installing documentation dependencies...${NC}"
    uv pip install -e ".[docs]"
    echo -e "${GREEN}✓ Documentation dependencies installed${NC}"
}

serve_docs() {
    echo -e "${BLUE}Starting documentation server...${NC}"
    echo -e "${GREEN}Documentation available at: http://localhost:8000${NC}"
    echo "Press Ctrl+C to stop the server"
    uv run mkdocs serve
}

build_docs() {
    echo -e "${BLUE}Building documentation...${NC}"
    uv run mkdocs build
    echo -e "${GREEN}✓ Documentation built successfully${NC}"
    echo "Output directory: site/"
}

deploy_docs() {
    echo -e "${BLUE}Deploying documentation to GitHub Pages...${NC}"
    uv run mkdocs gh-deploy
    echo -e "${GREEN}✓ Documentation deployed${NC}"
}

clean_docs() {
    echo -e "${BLUE}Cleaning build artifacts...${NC}"
    rm -rf site/
    find docs -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    echo -e "${GREEN}✓ Clean complete${NC}"
}

# Main
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    install)
        install_deps
        ;;
    serve)
        install_deps
        serve_docs
        ;;
    build)
        install_deps
        build_docs
        ;;
    deploy)
        install_deps
        deploy_docs
        ;;
    clean)
        clean_docs
        ;;
    help)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Run './docs-setup.sh help' for usage information"
        exit 1
        ;;
esac
