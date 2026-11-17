#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

# ANSI Colors
BOLD="\033[1m"
BLUE="\033[1;34m"
GREEN="\033[1;32m"
RESET="\033[0m"

echo -e "${BLUE}============================================================${RESET}"
echo -e "${BLUE}${BOLD} [0.PlainText] Simple TCP Connection & Data Exchange${RESET}"
echo -e "${BLUE}============================================================${RESET}"

# Start server in background
python3 server.py &
SERVER_PID=$!

# Ensure server process is terminated on exit
cleanup() {
    kill $SERVER_PID 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Wait briefly for server to bind and listen
sleep 0.5

# Run client
python3 client.py

# Wait briefly for clean shutdown
wait $SERVER_PID 2>/dev/null || true
trap - EXIT INT TERM

echo -e "${GREEN}============================================================${RESET}"
echo -e "${GREEN}${BOLD} [0.PlainText] Completed successfully!${RESET}"
echo -e "${GREEN}============================================================${RESET}"
