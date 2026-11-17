#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "============================================================"
echo " [0.PlainText] Simple TCP Connection & Data Exchange"
echo "============================================================"

# Start server in background
python3 server.py &
SERVER_PID=$!

# Ensure server process is terminated on exit
cleanup() {
    kill $SERVER_PID 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Wait for server to bind and listen
sleep 1

# Run client
python3 client.py

# Wait briefly for clean shutdown
sleep 1
wait $SERVER_PID 2>/dev/null || true
trap - EXIT INT TERM

echo "============================================================"
echo " [0.PlainText] Completed successfully!"
echo "============================================================"
