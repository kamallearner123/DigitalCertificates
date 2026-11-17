#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "============================================================"
echo " [1.EncryptWithSymKey] Symmetric Encryption & Decryption"
echo "============================================================"

# Pre-generate key if not present
if [ ! -f "secret.key" ]; then
    python3 -c "from cryptography.fernet import Fernet; open('secret.key', 'wb').write(Fernet.generate_key())"
    echo "[start.sh] Generated shared symmetric key in secret.key"
fi

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

# Wait briefly for server to wrap up
sleep 1
wait $SERVER_PID 2>/dev/null || true
trap - EXIT INT TERM

echo "============================================================"
echo " [1.EncryptWithSymKey] Completed successfully!"
echo "============================================================"
