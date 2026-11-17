#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "[generate_certs.sh] Generating self-signed X.509 SSL/TLS certificate and private key..."

openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout server.key \
    -out server.crt \
    -days 365 \
    -subj "/C=US/ST=CA/L=SanFrancisco/O=DevSec/OU=TLS/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

echo "[generate_certs.sh] Certificate (server.crt) and private key (server.key) created successfully."
