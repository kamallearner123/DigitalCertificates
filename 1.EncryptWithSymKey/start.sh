#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

# ANSI Colors
BOLD="\033[1m"
MAGENTA="\033[1;35m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo -e "${MAGENTA}======================================================================${RESET}"
echo -e "${MAGENTA}${BOLD} [1.EncryptWithSymKey] Symmetric Encryption & Decryption Demo${RESET}"
echo -e "${MAGENTA}======================================================================${RESET}"

# Pre-generate key if not present
if [ ! -f "secret.key" ]; then
    python3 -c "from cryptography.fernet import Fernet; open('secret.key', 'wb').write(Fernet.generate_key())"
    echo -e "${YELLOW}[start.sh] Generated shared symmetric key in secret.key${RESET}"
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
echo -e "${GREEN}${BOLD} [1.EncryptWithSymKey] Completed successfully!${RESET}"
echo -e "${GREEN}======================================================================${RESET}"
