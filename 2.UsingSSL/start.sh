#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

# ANSI Colors
BOLD="\033[1m"
CYAN="\033[1;36m"
GREEN="\033[1;32m"
RESET="\033[0m"

echo -e "${CYAN}======================================================================${RESET}"
echo -e "${CYAN}${BOLD} [2.UsingSSL] SSL/TLS Encrypted Connection & Data Exchange${RESET}"
echo -e "${CYAN}======================================================================${RESET}"

# Ensure certs exist
if [ ! -f "server.crt" ] || [ ! -f "server.key" ]; then
    bash generate_certs.sh
fi

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

# Wait briefly for server to wrap up
wait $SERVER_PID 2>/dev/null || true
trap - EXIT INT TERM

echo -e "${GREEN}======================================================================${RESET}"
echo -e "${GREEN}${BOLD} [2.UsingSSL] Completed successfully!${RESET}"
echo -e "${GREEN}======================================================================${RESET}"
