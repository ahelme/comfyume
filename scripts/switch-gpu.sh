#!/bin/bash
# switch-gpu.sh - Switch between inference modes/GPUs
# Usage: ./scripts/switch-gpu.sh [h200|b300|local]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_usage() {
    echo "Usage: $0 [h200|b300|local|status]"
    echo ""
    echo "Commands:"
    echo "  h200   - Switch to H200 serverless ($3.29/hr, 141GB, workshop)"
    echo "  b300   - Switch to B300 serverless ($4.95/hr, 288GB, 4K production)"
    echo "  local  - Switch to local/redis mode (workers poll queue)"
    echo "  status - Show current inference mode"
    echo ""
    echo "Examples:"
    echo "  $0 h200     # For workshop with 20 users"
    echo "  $0 b300     # For boss demo with 4K video"
    echo "  $0 local    # For development/testing"
}

show_status() {
    echo -e "${BLUE}Current inference configuration:${NC}"
    echo ""

    # Read from .env
    if [ -f "$PROJECT_DIR/.env" ]; then
        INFERENCE_MODE=$(grep "^INFERENCE_MODE=" "$PROJECT_DIR/.env" | cut -d'=' -f2)
        SERVERLESS_ACTIVE=$(grep "^SERVERLESS_ACTIVE=" "$PROJECT_DIR/.env" | cut -d'=' -f2)

        echo "  INFERENCE_MODE:    $INFERENCE_MODE"
        echo "  SERVERLESS_ACTIVE: $SERVERLESS_ACTIVE"

        if [ "$INFERENCE_MODE" = "serverless" ]; then
            if [ "$SERVERLESS_ACTIVE" = "h200" ]; then
                echo -e "  Active GPU:        ${GREEN}H200-141GB ($3.29/hr)${NC}"
            elif [ "$SERVERLESS_ACTIVE" = "b300" ]; then
                echo -e "  Active GPU:        ${GREEN}B300-288GB ($4.95/hr)${NC}"
            else
                echo -e "  Active GPU:        ${YELLOW}Default endpoint${NC}"
            fi
        else
            echo -e "  Active GPU:        ${YELLOW}Local/Redis workers${NC}"
        fi
    else
        echo "  .env file not found!"
    fi

    echo ""
    echo "Check live status: curl -s https://comfy.ahelme.net/health | jq"
}

switch_mode() {
    MODE=$1

    case $MODE in
        h200)
            echo -e "${GREEN}Switching to H200 serverless...${NC}"
            sed -i 's/^INFERENCE_MODE=.*/INFERENCE_MODE=serverless/' "$PROJECT_DIR/.env"
            sed -i 's/^SERVERLESS_ACTIVE=.*/SERVERLESS_ACTIVE=h200/' "$PROJECT_DIR/.env"
            echo "  INFERENCE_MODE=serverless"
            echo "  SERVERLESS_ACTIVE=h200"
            echo -e "  GPU: ${GREEN}H200 SXM5 141GB HBM3e - \$3.29/hr${NC}"
            echo "  Best for: Workshop (20 users), 720p/1080p video"
            ;;
        b300)
            echo -e "${GREEN}Switching to B300 serverless...${NC}"
            sed -i 's/^INFERENCE_MODE=.*/INFERENCE_MODE=serverless/' "$PROJECT_DIR/.env"
            sed -i 's/^SERVERLESS_ACTIVE=.*/SERVERLESS_ACTIVE=b300/' "$PROJECT_DIR/.env"
            echo "  INFERENCE_MODE=serverless"
            echo "  SERVERLESS_ACTIVE=b300"
            echo -e "  GPU: ${GREEN}B300 SXM6 288GB HBM3e - \$4.95/hr${NC}"
            echo "  Best for: 4K production, boss demo, native 4K @ 3+ min"
            ;;
        local)
            echo -e "${GREEN}Switching to local/redis mode...${NC}"
            sed -i 's/^INFERENCE_MODE=.*/INFERENCE_MODE=local/' "$PROJECT_DIR/.env"
            sed -i 's/^SERVERLESS_ACTIVE=.*/SERVERLESS_ACTIVE=default/' "$PROJECT_DIR/.env"
            echo "  INFERENCE_MODE=local"
            echo "  SERVERLESS_ACTIVE=default"
            echo -e "  Mode: ${YELLOW}Workers poll Redis queue${NC}"
            echo "  Best for: Development, testing, dedicated GPU"
            ;;
        *)
            echo "Unknown mode: $MODE"
            show_usage
            exit 1
            ;;
    esac

    echo ""
    echo -e "${YELLOW}Restart queue-manager to apply:${NC}"
    echo "  docker compose restart queue-manager"
    echo ""
    echo "Or restart all services:"
    echo "  docker compose down && docker compose up -d"
}

# Main
case "${1:-}" in
    h200|b300|local)
        switch_mode "$1"
        ;;
    status|"")
        show_status
        ;;
    -h|--help|help)
        show_usage
        ;;
    *)
        echo "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
