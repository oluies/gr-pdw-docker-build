#!/bin/bash

# gr-pdw Docker Environment Management Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build       Build the Docker image"
    echo "  run         Run the container interactively"
    echo "  start       Start the container in background"
    echo "  stop        Stop the container"
    echo "  shell       Open a shell in running container"
    echo "  grc         Launch GNU Radio Companion"
    echo "  clean       Remove container and image"
    echo "  logs        Show container logs"
    echo "  help        Show this help message"
    echo ""
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
}

build_image() {
    echo -e "${GREEN}Building gr-pdw Docker image...${NC}"
    if command -v docker-compose &> /dev/null; then
        docker-compose build
    else
        docker build -t gr-pdw:latest .
    fi
    echo -e "${GREEN}Build complete!${NC}"
}

run_container() {
    echo -e "${GREEN}Running gr-pdw container...${NC}"
    
    # Create workspace directory if it doesn't exist
    mkdir -p workspace
    
    # Enable X11 forwarding on Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xhost +local:docker 2>/dev/null || echo -e "${YELLOW}Warning: Could not enable X11 forwarding${NC}"
    fi
    
    if command -v docker-compose &> /dev/null; then
        docker-compose run --rm gr-pdw
    else
        docker run -it --rm \
            --name gr-pdw \
            -v "$SCRIPT_DIR/workspace:/workspace" \
            -e DISPLAY="$DISPLAY" \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            --device=/dev/bus/usb:/dev/bus/usb \
            --network host \
            gr-pdw:latest
    fi
}

start_container() {
    echo -e "${GREEN}Starting gr-pdw container in background...${NC}"
    mkdir -p workspace
    
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
        echo -e "${GREEN}Container started. Use '$0 shell' to access it.${NC}"
    else
        docker run -d \
            --name gr-pdw \
            -v "$SCRIPT_DIR/workspace:/workspace" \
            -e DISPLAY="$DISPLAY" \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            --device=/dev/bus/usb:/dev/bus/usb \
            --network host \
            gr-pdw:latest \
            tail -f /dev/null
        echo -e "${GREEN}Container started. Use '$0 shell' to access it.${NC}"
    fi
}

stop_container() {
    echo -e "${YELLOW}Stopping gr-pdw container...${NC}"
    if command -v docker-compose &> /dev/null; then
        docker-compose down
    else
        docker stop gr-pdw 2>/dev/null || true
        docker rm gr-pdw 2>/dev/null || true
    fi
    echo -e "${GREEN}Container stopped${NC}"
}

open_shell() {
    if command -v docker-compose &> /dev/null; then
        docker-compose exec gr-pdw bash
    else
        docker exec -it gr-pdw bash
    fi
}

launch_grc() {
    echo -e "${GREEN}Launching GNU Radio Companion...${NC}"
    
    # Enable X11 forwarding on Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xhost +local:docker 2>/dev/null || echo -e "${YELLOW}Warning: Could not enable X11 forwarding${NC}"
    fi
    
    if docker ps --format '{{.Names}}' | grep -q "^gr-pdw$"; then
        docker exec -it gr-pdw gnuradio-companion
    else
        echo -e "${YELLOW}Container not running. Starting it now...${NC}"
        start_container
        sleep 2
        docker exec -it gr-pdw gnuradio-companion
    fi
}

clean_all() {
    echo -e "${YELLOW}Cleaning up gr-pdw Docker resources...${NC}"
    stop_container
    docker rmi gr-pdw:latest 2>/dev/null || true
    echo -e "${GREEN}Cleanup complete${NC}"
}

show_logs() {
    if command -v docker-compose &> /dev/null; then
        docker-compose logs -f
    else
        docker logs -f gr-pdw
    fi
}

# Main script logic
check_docker

case "${1:-help}" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    start)
        start_container
        ;;
    stop)
        stop_container
        ;;
    shell)
        open_shell
        ;;
    grc)
        launch_grc
        ;;
    clean)
        clean_all
        ;;
    logs)
        show_logs
        ;;
    help|*)
        print_usage
        ;;
esac
